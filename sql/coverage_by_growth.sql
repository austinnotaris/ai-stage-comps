SELECT
    "Growth Bucket",
    COUNT(*) AS Num_Observations
FROM panel
WHERE "Growth Bucket" IS NOT NULL
    AND (:Growth_Bucket IS NULL OR "Growth Bucket" = :Growth_Bucket)
GROUP BY "Growth Bucket"
ORDER BY Num_Observations DESC;