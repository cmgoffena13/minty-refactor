-- FUNCTION: public.select_rolling_sum_time_periods()

-- DROP FUNCTION IF EXISTS public.select_rolling_sum_time_periods();

CREATE OR REPLACE FUNCTION public.select_rolling_sum_time_periods(
	)
    RETURNS TABLE(date_actual date, pay_period_id integer, rolling_transactions_amounts_p1 numeric, rolling_transactions_amounts_p2 numeric) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN

	REFRESH MATERIALIZED VIEW income_time_frames;

	DROP TABLE IF EXISTS temp_income_time_frame_dates;
	CREATE TEMP TABLE temp_income_time_frame_dates AS
	SELECT
	c.date_actual,
	CAST(f.pay_period_id AS INT) AS pay_period_id,
	f.local_pay_period
	FROM public.calendar AS c
	INNER JOIN (SELECT 
				i.start_date, 
				i.end_date,
				i.pay_period_id,
				ROW_NUMBER() OVER (ORDER BY i.pay_period_id DESC) AS local_pay_period
				FROM income_time_frames AS i
				ORDER BY i.pay_period_id DESC
				LIMIT 2) AS f
		ON f.start_date <= c.date_actual
		AND f.end_date >= c.date_actual
	WHERE c.date_actual <= CURRENT_DATE;
	
	DROP TABLE IF EXISTS temp_transactions_by_day;
	CREATE TEMP TABLE temp_transactions_by_day AS 
	SELECT
	t.transaction_date,
	SUM(t.transaction_amount) AS transaction_amounts,
	LEAD(t.transaction_date) OVER (ORDER BY t.transaction_date) AS next_day_transaction_date
	FROM public.transactions AS t
	INNER JOIN public.accounts AS a
		ON a.account_id = t.account_id
	WHERE a.is_operation_account = true
	GROUP BY transaction_date;

	DROP TABLE IF EXISTS temp_income_time_frame_dates_p1;
	CREATE TEMP TABLE temp_income_time_frame_dates_p1 AS
	SELECT
	d.date_actual,
	CAST(d.pay_period_id AS INT) AS pay_period_id,
	SUM(t.transaction_amounts) OVER (PARTITION BY d.pay_period_id ORDER BY d.date_actual) AS rolling_transactions_amounts_p1,
	ROW_NUMBER() OVER (PARTITION BY d.pay_period_id ORDER BY d.date_actual) AS day_num
	FROM temp_income_time_frame_dates AS d
	INNER JOIN temp_transactions_by_day AS t
		ON d.date_actual BETWEEN t.transaction_date 
		AND COALESCE((CAST(next_day_transaction_date - INTERVAL '1 day' AS DATE)), t.transaction_date) /* fills in missing days */
	WHERE d.local_pay_period = 1
	ORDER BY d.date_actual DESC;
	
	DROP TABLE IF EXISTS temp_income_time_frame_dates_p2;
	CREATE TEMP TABLE temp_income_time_frame_dates_p2 AS
	SELECT
	d.date_actual,
	d.pay_period_id,
	SUM(t.transaction_amounts) OVER (PARTITION BY d.pay_period_id ORDER BY d.date_actual) AS rolling_transactions_amounts_p2,
	ROW_NUMBER() OVER (PARTITION BY d.pay_period_id ORDER BY d.date_actual) AS day_num
	FROM temp_income_time_frame_dates AS d
	INNER JOIN temp_transactions_by_day AS t
		ON d.date_actual BETWEEN t.transaction_date 
		AND COALESCE((CAST(next_day_transaction_date - INTERVAL '1 day' AS DATE)), t.transaction_date) /* fills in missing days */
	WHERE d.local_pay_period = 2
	ORDER BY d.date_actual DESC;

	RETURN QUERY
	SELECT
	d.date_actual,
	d.pay_period_id,
	CAST(d.rolling_transactions_amounts_p1 AS NUMERIC) AS rolling_transactions_amounts_p1,
	CAST(d2.rolling_transactions_amounts_p2 AS NUMERIC) AS rolling_transactions_amounts_p2
	FROM temp_income_time_frame_dates_p1 AS d
	LEFT JOIN temp_income_time_frame_dates_p2 AS d2
		ON d2.day_num = d.day_num
	ORDER BY d.date_actual DESC;

END;
$BODY$;

ALTER FUNCTION public.select_rolling_sum_time_periods()
    OWNER TO postgres;
