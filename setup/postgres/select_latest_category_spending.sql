-- FUNCTION: public.select_latest_category_spending()

-- DROP FUNCTION IF EXISTS public.select_latest_category_spending();

CREATE OR REPLACE FUNCTION public.select_latest_category_spending(
	)
    RETURNS TABLE(custom_category_name character varying, total_transaction_amount_p1 numeric, total_transaction_amount_p2 numeric) 
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
	
	DROP TABLE IF EXISTS temp_category_spending_p1;
	CREATE TEMP TABLE temp_category_spending_p1 AS
	SELECT
	cc.custom_category_name,
	SUM(t.transaction_amount) AS total_transaction_amount
	FROM public.transactions AS t
	INNER JOIN temp_income_time_frame_dates AS ti
		ON ti.date_actual = t.transaction_date
	INNER JOIN public.custom_categories AS cc
		ON cc.custom_category_id = t.custom_category_id
	WHERE cc.custom_category_id != -1
		AND t.transaction_amount < 0
		AND ti.local_pay_period = 1
	GROUP BY cc.custom_category_name
	ORDER BY SUM(t.transaction_amount) ASC;
	
	DROP TABLE IF EXISTS temp_category_spending_p2;
	CREATE TEMP TABLE temp_category_spending_p2 AS
	SELECT
	cc.custom_category_name,
	SUM(t.transaction_amount) AS total_transaction_amount
	FROM public.transactions AS t
	INNER JOIN temp_income_time_frame_dates AS ti
		ON ti.date_actual = t.transaction_date
	INNER JOIN public.custom_categories AS cc
		ON cc.custom_category_id = t.custom_category_id
	WHERE cc.custom_category_id != -1
		AND t.transaction_amount < 0
		AND ti.local_pay_period = 2
	GROUP BY cc.custom_category_name
	ORDER BY SUM(t.transaction_amount) ASC;

	RETURN QUERY
	SELECT
	COALESCE(tcs.custom_category_name, tcs2.custom_category_name) AS custom_category_name,
	COALESCE(tcs.total_transaction_amount, 0) AS total_transaction_amount_p1,
	COALESCE(tcs2.total_transaction_amount, 0) AS total_transaction_amount_p2
	FROM temp_category_spending_p1 AS tcs
	FULL OUTER JOIN temp_category_spending_p2 AS tcs2
		ON tcs2.custom_category_name = tcs.custom_category_name;
	
	
END;
$BODY$;

ALTER FUNCTION public.select_latest_category_spending()
    OWNER TO postgres;
