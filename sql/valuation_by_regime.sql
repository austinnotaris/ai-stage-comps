SELECT
    "Growth Bucket",
    "Capex Bucket",
    "Margin Bucket",
    "Revenue Bucket",
    AVG("EV/Rev") AS Mean_EV_Rev,
    MIN("EV/Rev") AS Min_EV_Rev,
    MAX("EV/Rev") AS Max_EV_Rev
FROM panel
WHERE "Growth Bucket" IS NOT NULL
    AND "Capex Bucket" IS NOT NULL
    AND "Margin Bucket" IS NOT NULL
    AND "Revenue Bucket" IS NOT NULL
    AND (:Growth_Bucket IS NULL OR "Growth Bucket" = :Growth_Bucket)
    AND (:Capex_Bucket IS NULL OR "Capex Bucket" = :Capex_Bucket)
    AND (:Margin_Bucket IS NULL OR "Margin Bucket"  = :Margin_Bucket)
    AND (:Revenue_Bucket IS NULL OR "Revenue Bucket" = :Revenue_Bucket)
GROUP BY "Growth Bucket", "Capex Bucket", "Margin Bucket", "Revenue Bucket"
HAVING (:Min_EV_Rev IS NULL OR AVG("EV/Rev") >= :Min_EV_Rev)
    AND (:Max_EV_Rev IS NULL OR AVG("EV/Rev") <= :Max_EV_Rev)
ORDER BY Mean_EV_Rev DESC;