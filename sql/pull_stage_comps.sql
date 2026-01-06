SELECT
    "Company Name",
    "Exchange",
    "Ticker",
    "Year",
    "EV/Rev",
    "Margin Bucket"
FROM panel
WHERE "Growth Bucket" = :Growth_Bucket
    AND "Revenue Bucket" = :Revenue_Bucket;