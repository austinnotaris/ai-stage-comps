import numpy as np

def revenue_yoy(df):
    df["Revenue YoY"] = np.nan
    mask = (df["Year"] != 2018)
    df.loc[mask, "Revenue YoY"] = df["Total Revenue ($USDmm)"] / df["Total Revenue ($USDmm)"].shift(1) - 1
    df["Revenue YoY"] = df["Revenue YoY"].round(4)
    return df

def capex_yoy(df):
    df["Capex YoY"] = np.nan
    mask = (df["Year"] != 2018)
    df.loc[mask, "Capex YoY"] = df["Capital Expenditure ($USDmm)"] / df["Capital Expenditure ($USDmm)"].shift(1) - 1
    df["Capex YoY"] = df["Capex YoY"].round(4)
    return df