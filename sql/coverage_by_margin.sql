SELECT
    "Margin Bucket",
    COUNT(*) AS Num_Observations
FROM panel
WHERE "Margin Bucket" IS NOT NULL
    AND (:Margin_Bucket IS NULL OR "Margin Bucket" = :Margin_Bucket)
GROUP BY "Margin Bucket"
ORDER BY Num_Observations DESC;