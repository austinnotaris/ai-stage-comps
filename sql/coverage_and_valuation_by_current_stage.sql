SELECT
    "Growth Bucket",
    "Revenue Bucket",
    COUNT(*) AS Num_Observations,
    AVG("EV/Rev") AS Mean_EV_Rev
FROM panel
WHERE "Growth Bucket" IS NOT NULL
    AND "Revenue Bucket" IS NOT NULL
    AND (:Growth_Bucket IS NULL OR "Growth Bucket" = :Growth_Bucket)
    AND (:Revenue_Bucket IS NULL OR "Revenue Bucket" = :Revenue_Bucket)
GROUP BY "Growth Bucket", "Revenue Bucket"
ORDER BY
    CASE "Growth Bucket"
        WHEN 'Declining' THEN 1
        WHEN 'Low Growth' THEN 2
        WHEN 'Moderate Growth' THEN 3
        WHEN 'High Growth' THEN 4
        WHEN 'Hypergrowth' THEN 5
    END,
    CASE "Revenue Bucket"
        WHEN '<50M' THEN 1
        WHEN '$50-100M' THEN 2
        WHEN '$100-250M' THEN 3
        WHEN '$250-500M' THEN 4
        WHEN '$500M-1B' THEN 5
        WHEN '$1B+' THEN 6
    END;