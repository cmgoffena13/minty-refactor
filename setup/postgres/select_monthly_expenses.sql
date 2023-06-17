-- FUNCTION: public.select_rolling_sum_time_periods()

-- DROP FUNCTION IF EXISTS public.select_rolling_sum_time_periods();

CREATE OR REPLACE FUNCTION public.select_monthly_expenses(date_filter DATE)
    RETURNS TABLE(last_date_of_month date,
					monthly_expenses NUMERIC(17,2)
				 ) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN

	

	RETURN QUERY
	SELECT
	c.last_date_of_month,
	SUM(transaction_amount) AS monthly_expenses
	FROM public.transactions AS t
	INNER JOIN public.accounts AS a
		ON a.account_id = t.account_id
	INNER JOIN public.calendar AS c
		ON c.date_actual = t.transaction_date
	WHERE c.last_date_of_month >= date_filter
	AND a.is_operation_account = true
	AND t.transaction_amount < 0
    AND t.custom_category_id NOT IN (-2, -3)
	GROUP BY c.last_date_of_month
	ORDER BY c.last_date_of_month;

END;
$BODY$;
