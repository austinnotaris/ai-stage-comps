import numpy as np
def stage_classifier(df):
    df["Growth Bucket"] = np.select(
    [
        df["Revenue YoY"].isna(),
        df["Revenue YoY"] < 0,
        df["Revenue YoY"] < .10,
        df["Revenue YoY"] < .25,
        df["Revenue YoY"] < .40,
        df["Revenue YoY"] < .60,
        df["Revenue YoY"] >= .60
    ],
    [
        None,
        "Declining",
        "Low Growth",
        "Moderate Growth",
        "High Growth",
        "Very High Growth",
        "Hypergrowth"
    ]
    )
    df["Capex Bucket"] = np.select(
    [
        df["Capex to Rev"].isna(),
        df["Capex to Rev"] < .05,
        df["Capex to Rev"] < .15,
        df["Capex to Rev"] < .25,
        df["Capex to Rev"] < .40,
        df["Capex to Rev"] >= .40
    ],
    [
        None,
        "Asset Light",
        "Moderate Capital Intensity",
        "High Capital Intensity",
        "Very High Capital Intensity",
        "Extreme Capital Intensity"
    ]
    )
    df["Margin Bucket"] = np.select(
    [
        df["Gross Margin %"].isna(),
        df["Gross Margin %"] < 20.0,
        df["Gross Margin %"] < 35.0,
        df["Gross Margin %"] < 50.0,
        df["Gross Margin %"] < 65.0,
        df["Gross Margin %"] < 80.0,
        df["Gross Margin %"] >= 80.0,
    ],
    [
        None,
        "Very Low Margin",
        "Low Margin",
        "Low Mid Margin",
        "High Mid margin",
        "High Margin",
        "Very High Margin"
    ]
    )
    df["Revenue Bucket"] = np.select(
    [
        df["Total Revenue ($USDmm)"].isna(),
        df["Total Revenue ($USDmm)"] < 50,
        df["Total Revenue ($USDmm)"] < 100,
        df["Total Revenue ($USDmm)"] < 250,
        df["Total Revenue ($USDmm)"] < 500,
        df["Total Revenue ($USDmm)"] < 1000,
        df["Total Revenue ($USDmm)"] >= 1000
    ],
    [
        None,
        "< $50M",
        "$50-100M",
        "$100-250M",
        "$250-500M",
        "$500M-1B",
        "$1B+"
    ]
    )
    return df