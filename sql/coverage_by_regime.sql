SELECT
    "Growth Bucket",
    "Capex Bucket",
    "Margin Bucket",
    "Revenue Bucket",
    COUNT(*) AS Num_Observations
FROM panel
WHERE "Growth Bucket" IS NOT NULL
    AND "Capex Bucket" IS NOT NULL
    AND "Margin Bucket" IS NOT NULL
    AND "Revenue Bucket" IS NOT NULL
    AND (:Growth_Bucket IS NULL OR "Growth Bucket" = :Growth_Bucket)
    AND (:Capex_Bucket IS NULL OR "Capex Bucket" = :Capex_Bucket)
    AND (:Margin_Bucket IS NULL OR "Margin Bucket" = :Margin_Bucket)
    AND (:Revenue_Bucket IS NULL OR "Revenue Bucket" = :Revenue_Bucket)
GROUP BY "Growth Bucket", "Capex Bucket", "Margin Bucket", "Revenue Bucket"
HAVING (:Min_Observations IS NULL OR Num_Observations >= :Min_Observations)
    AND (:Max_Observations IS NULL OR Num_Observations <= :Max_Observations)
ORDER BY Num_Observations DESC;