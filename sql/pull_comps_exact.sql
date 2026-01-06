SELECT
    "Company Name",
    "Exchange",
    "Ticker",
    "Year",
    "EV/Rev"
FROM panel
WHERE "Growth Bucket" = :Growth_Bucket
    AND "Capex Bucket" = :Capex_Bucket
    AND "Margin Bucket" = :Margin_Bucket
    AND "Revenue Bucket" = :Revenue_Bucket;