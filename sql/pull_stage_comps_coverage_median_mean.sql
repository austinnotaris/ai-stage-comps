WITH ranked AS (
    SELECT
        "Growth Bucket",
        "Revenue Bucket",
        "EV/Rev",
        ROW_NUMBER() OVER (
            PARTITION BY "Growth Bucket", "Revenue Bucket"
            ORDER BY "EV/Rev"
        ) AS rn,
        COUNT(*) OVER (
            PARTITION BY "Growth Bucket", "Revenue Bucket"
        ) AS cnt,
        AVG("EV/Rev") OVER (
            PARTITION BY "Growth Bucket", "Revenue Bucket"
        ) AS mean_ev_rev
    FROM panel
    WHERE "Growth Bucket" IS NOT NULL
        AND "Revenue Bucket" IS NOT NULL
        AND (:Growth_Bucket IS NULL OR "Growth Bucket" = :Growth_Bucket)
        AND (:Revenue_Bucket IS NULL OR "Revenue Bucket" = :Revenue_Bucket)
),
middles AS (
    SELECT *
    FROM ranked
    WHERE rn IN ((cnt + 1) / 2, (cnt + 2) / 2)
)
SELECT
    "Growth Bucket",
    "Revenue Bucket",
    MAX(cnt) AS Num_Observations,
    CASE
        WHEN MAX(cnt) % 2 = 1 THEN MAX("EV/Rev")
        ELSE SUM("EV/Rev") / 2.0
    END AS Median_EV_Rev,
    MAX(mean_ev_rev) AS Mean_EV_Rev
FROM middles
WHERE
    "Growth Bucket" = :Growth_Bucket
    AND "Revenue Bucket" = :Revenue_Bucket
GROUP BY "Growth Bucket", "Revenue Bucket";