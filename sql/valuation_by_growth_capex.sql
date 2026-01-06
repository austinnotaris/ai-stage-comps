SELECT
    "Growth Bucket",
    "Capex Bucket",
    AVG("EV/Rev") AS Mean_EV_Rev
FROM panel
WHERE "Growth Bucket" IS NOT NULL
    AND "Capex Bucket" IS NOT NULL
GROUP BY "Growth Bucket", "Capex Bucket";