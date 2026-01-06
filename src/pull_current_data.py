import pandas as pd

df_lq_val = pd.read_csv("../data/processed/fundamentals_clean_val_lq_only.csv")
df_lq_financials = pd.read_csv("../data/processed/fundamentals_clean_lq.csv")
df_lq_full_panel = pd.merge(df_lq_financials, df_lq_val["Total Enterprise Value ($USDmm, Historical rate)"], on="Company Name", how="left")
df_lq_full_panel = df_lq_full_panel.rename(columns={"Total Revenue ($USDmm, Historical rate)":"Current Day Rev",
                                                    "Gross Margin %":"Current Day Gross Margin %",
                                                    "Capital Expenditure ($USDmm, Historical rate)":"Current Day Capex",
                                                    "Total Enterprise Value ($USDmm, Historical rate)":"Current Day TEV"})
df_lq_full_panel["Current Day EV/Rev"] = df_lq_full_panel["Current Day TEV"]/df_lq_full_panel["Current Day Rev"]

def add_current_rev(df){
    df = pd.merge(df, df_full_panel["Current Day Rev"], on="Company Name", how="left")
    return df

def add_current_tev(df){
    df = pd.merge(df, df_full_panel["Current Day TEV"], on="Company Name", how="left")
    return df

def add_current_ev_to_rev(df){
    df = pd.merge(df, df_full_panel["Current Day EV/Rev"], on="Company Name", how="left")
    return df