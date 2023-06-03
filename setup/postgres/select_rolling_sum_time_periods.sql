CREATE OR REPLACE FUNCTION select_rolling_sum_time_periods()
RETURNS TABLE (date_actual DATE, pay_period_id INT, rolling_transactions_amounts NUMERIC)
AS
$$
BEGIN

	REFRESH MATERIALIZED VIEW income_time_frames;

	DROP TABLE IF EXISTS temp_income_time_frame_dates;
	CREATE TEMP TABLE temp_income_time_frame_dates AS
	SELECT
	c.date_actual,
	CAST(f.pay_period_id AS INT) AS pay_period_id
	FROM public.calendar AS c
	INNER JOIN (SELECT 
				i.start_date, 
				i.end_date,
				i.pay_period_id
				FROM income_time_frames AS i
				ORDER BY pay_period_id DESC
				LIMIT 1) AS f
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

	RETURN QUERY
	SELECT
	d.date_actual,
	d.pay_period_id,
	SUM(t.transaction_amounts) OVER (PARTITION BY d.pay_period_id ORDER BY d.date_actual) AS rolling_transactions_amounts
	FROM temp_income_time_frame_dates AS d
	INNER JOIN temp_transactions_by_day AS t
		ON d.date_actual BETWEEN t.transaction_date 
		AND COALESCE((CAST(next_day_transaction_date - INTERVAL '1 day' AS DATE)), t.transaction_date) /* fills in missing days */
	ORDER BY d.date_actual DESC;


END;
$$
LANGUAGE plpgsql;