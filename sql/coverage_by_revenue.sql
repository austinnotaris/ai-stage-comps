SELECT
    "Revenue Bucket",
    COUNT(*) AS Num_Observations
FROM panel
WHERE "Revenue Bucket" IS NOT NULL
    AND (:Revenue_Bucket IS NULL OR "Revenue Bucket" = :Revenue_Bucket)
GROUP BY "Revenue Bucket"
ORDER BY Num_Observations DESC;