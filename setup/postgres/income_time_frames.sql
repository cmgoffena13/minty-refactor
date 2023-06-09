-- View: public.income_time_frames

-- DROP MATERIALIZED VIEW IF EXISTS public.income_time_frames;

CREATE MATERIALIZED VIEW IF NOT EXISTS public.income_time_frames
TABLESPACE pg_default
AS
 SELECT row_number() OVER (ORDER BY transactions.transaction_date) AS pay_period_id,
    transactions.transaction_date AS start_date,
    (lead(transactions.transaction_date, 1, '9999-12-31'::date) OVER (ORDER BY transactions.transaction_date) - '1 day'::interval)::date AS end_date
   FROM transactions
  WHERE transactions.custom_category_id = 1
  GROUP BY transactions.transaction_date
  ORDER BY transactions.transaction_date DESC
WITH DATA;

ALTER TABLE IF EXISTS public.income_time_frames
    OWNER TO postgres;