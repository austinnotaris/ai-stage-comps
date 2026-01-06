SELECT
    "Growth Bucket",
    "Margin Bucket",
    AVG("EV/Rev") AS Mean_EV_Rev
FROM panel
WHERE "Growth Bucket" IS NOT NULL
    AND "Margin Bucket" IS NOT NULL
GROUP BY "Growth Bucket", "Margin Bucket";