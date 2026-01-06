SELECT
    "Company Name",
    "Exchange",
    "Ticker",
    "Year",
    "EV/Rev",
    "Growth Bucket",
    "Margin Bucket",
    "Revenue Bucket"
FROM panel
WHERE ("Growth Bucket"=:Growth_Bucket AND "Margin Bucket"=:Margin_Bucket AND "Revenue Bucket"=:Revenue_Bucket)
    OR (("Growth Bucket"=:Growth_Bucket_Less OR "Growth Bucket"=:Growth_Bucket_More) AND "Margin Bucket"=:Margin_Bucket AND "Revenue Bucket"=:Revenue_Bucket)
    OR (("Margin Bucket"=:Margin_Bucket_Less OR "Margin Bucket"=:Margin_Bucket_More) AND "Growth Bucket"=:Growth_Bucket AND "Revenue Bucket"=:Revenue_Bucket)
    OR (("Revenue Bucket"=:Revenue_Bucket_Less OR "Revenue Bucket"=:Revenue_Bucket_More) AND "Growth Bucket"=:Growth_Bucket AND "Margin Bucket"=:Margin_Bucket)
ORDER BY "EV/Rev" DESC;