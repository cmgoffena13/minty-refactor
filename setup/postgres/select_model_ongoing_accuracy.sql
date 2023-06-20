
CREATE OR REPLACE FUNCTION public.select_model_ongoing_accuracy()
    RETURNS TABLE(classifier_name VARCHAR(100),
				  ongoing_accuracy NUMERIC(20,4)
				 ) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN

	RETURN QUERY
	SELECT
	c.classifier_name,
	ROUND(SUM(CASE WHEN accurate=1 THEN 1 ELSE 0 END) / CAST(COUNT(*) AS NUMERIC), 4) AS ongoing_accuracy
	FROM public.classifier_history AS ch
	INNER JOIN public.classifiers AS c
		ON c.classifier_id = ch.classifier_id
	GROUP BY c.classifier_name;

END;
$BODY$;
