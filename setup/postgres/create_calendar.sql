CREATE OR REPLACE PROCEDURE create_calendar()
AS
$$
BEGIN
	DROP TABLE IF EXISTS calendar;
	
  	CREATE TABLE calendar AS
    SELECT
      TO_CHAR(date_actual, 'yyyymmdd')::INT AS date_id,
      date_actual,
      TO_CHAR(date_actual, 'TMDay') AS day_name,
      CASE WHEN TO_CHAR(date_actual, 'TMDay') IN ('Saturday', 'Sunday') THEN 1 ELSE 0 END AS is_weekend,
      EXTRACT(MONTH FROM date_actual) AS month_id,
      TO_CHAR(date_actual, 'TMMonth') AS month_name,
      EXTRACT(YEAR FROM date_actual) AS year_actual,
      TO_CHAR(date_actual, 'YYYYMM') AS month_year,
      CAST(date_actual - INTERVAL '1 year' AS DATE) AS previous_year_date_actual,
      TO_CHAR(date_actual - INTERVAL '1 year', 'YYYYMM') AS previous_year_month_year
    FROM (
      SELECT '2015-06-24'::DATE + SEQUENCE.DAY AS date_actual /* replace 2015-06-24 with your first transaction date */
      FROM GENERATE_SERIES(0, 5304) AS SEQUENCE (DAY)
      GROUP BY SEQUENCE.DAY
    ) AS DQ
    ORDER BY 1;
	
END;
$$
LANGUAGE plpgsql;