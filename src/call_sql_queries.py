import pandas as pd
from pathlib import Path

import sys
sys.path.append("../src")
from check_bucket_params import *
from bucket_orders import *

import sqlite3

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "analysis.db"
conn = sqlite3.connect(DB_PATH)
PANEL_PATH = PROJECT_ROOT / "data" / "processed" / "full_panel.csv"

df_panel = pd.read_csv(PANEL_PATH)
df_panel.to_sql("panel", conn, if_exists="replace", index=False)

def coverage_by_growth(GB):
    CB = None
    MB = None
    RB = None
    sql_cbg = Path("../sql/coverage_by_growth.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
        }
        df = pd.read_sql(sql_cbg, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations"})
        return df

def coverage_by_margin(MB):
    CB = None
    GB = None
    RB = None
    sql_cbm = Path("../sql/coverage_by_margin.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Margin_Bucket": MB,
        }
        df = pd.read_sql(sql_cbm, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations"})
        return df

def coverage_by_revenue(RB):
    CB = None
    MB = None
    GB = None
    sql_cbr = Path("../sql/coverage_by_revenue.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Revenue_Bucket": RB,
        }
        df = pd.read_sql(sql_cbr, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations"})
        return df

def coverage_by_regime(GB, CB, MB, RB, MinObs, MaxObs):
    sql_cbregime = Path("../sql/coverage_by_regime.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Capex_Bucket": CB,
            "Margin_Bucket": MB,
            "Revenue_Bucket": RB,
            "Min_Observations": MinObs,
            "Max_Observations": MaxObs
        }
        df = pd.read_sql(sql_cbregime, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations"})
        return df

def coverage_by_regime_minus_capex(GB, MB, RB, MinObs, MaxObs):
    CB = None
    sql_cbrmc = Path("../sql/coverage_by_regime_minus_capex.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Margin_Bucket": MB,
            "Revenue_Bucket": RB,
            "Min_Observations": MinObs,
            "Max_Observations": MaxObs
        }
        df = pd.read_sql(sql_cbrmc, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations"})
        return df

def valuation_by_regime(GB, CB, MB, RB, MinEVR, MaxEVR):
    sql_vbr = Path("../sql/valuation_by_regime.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Capex_Bucket": CB,
            "Margin_Bucket": MB,
            "Revenue_Bucket": RB,
            "Min_EV_Rev": MinEVR,
            "Max_EV_Rev": MaxEVR
        }
        df = pd.read_sql(sql_vbr, conn, params=params)
        df = df.rename(columns={"Mean_EV_Rev":"Mean EV/Rev", "Min_EV_Rev":"Min EV/Rev", "Max_EV_Rev":"Max EV/Rev"})
        return df

def valuation_by_growth_capex():
    sql_vbgc = Path("../sql/valuation_by_growth_capex.sql").read_text()
    df = pd.read_sql(sql_vbgc, conn)
    df = df.pivot(index="Growth Bucket", columns="Capex Bucket", values="Mean_EV_Rev")
    df = df[capex_buckets[1:]]
    df = df.loc[growth_buckets[1:]]
    return df

def valuation_by_growth_margin():
    sql_vbgm = Path("../sql/valuation_by_growth_margin.sql").read_text()
    df = pd.read_sql(sql_vbgm, conn)
    df = df.pivot(index="Growth Bucket", columns="Margin Bucket", values="Mean_EV_Rev")
    df = df[margin_buckets[1:]]
    df = df.loc[growth_buckets[1:]]
    return df

def valuation_by_growth_revenue():
    sql_vbgr = Path("../sql/valuation_by_growth_revenue.sql").read_text()
    df = pd.read_sql(sql_vbgr, conn)
    df = df.pivot(index="Growth Bucket", columns="Revenue Bucket", values="Mean_EV_Rev")
    df = df[revenue_buckets[1:]]
    df = df.loc[growth_buckets[1:]]
    return df

def coverage_and_valuation_by_current_stage(GB, RB):
    sql_cavbcs = Path("../sql/coverage_and_valuation_by_current_stage.sql").read_text()
    CB = None
    MB = None
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Revenue_Bucket": RB
        }
        df = pd.read_sql(sql_cavbcs, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations", "Mean_EV_Rev":"Mean EV/Rev"})
        return df

def pull_comps_exact(GB, CB, MB, RB):
    sql_pce = Path("../sql/pull_comps_exact.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Capex_Bucket": CB,
            "Margin_Bucket": MB,
            "Revenue_Bucket": RB
        }
        df = pd.read_sql(sql_pce, conn, params=params)
        return df

def pull_comps_minus_capex(GB, MB, RB):
    CB = None
    sql_pcmc = Path("../sql/pull_comps_minus_capex.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Margin_Bucket": MB,
            "Revenue_Bucket": RB
        }
        df = pd.read_sql(sql_pcmc, conn, params=params)
        return df

def pull_comps_fuzzy(GB, CB, MB, RB):
    sql_pcf = Path("../sql/pull_comps_fuzzy.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        GB_L = growth_buckets[growth_buckets.index(GB)-1] if GB != growth_buckets[0] else GB
        GB_M = growth_buckets[growth_buckets.index(GB)+1] if GB != growth_buckets[-1] else GB
        CB_L = capex_buckets[capex_buckets.index(CB)-1] if CB != capex_buckets[0] else CB
        CB_M = capex_buckets[capex_buckets.index(CB)+1] if CB != capex_buckets[-1] else CB
        MB_L = margin_buckets[margin_buckets.index(MB)-1] if MB != margin_buckets[0] else MB
        MB_M = margin_buckets[margin_buckets.index(MB)+1] if MB != margin_buckets[-1] else MB
        RB_L = revenue_buckets[revenue_buckets.index(RB)-1] if RB != revenue_buckets[0] else RB
        RB_M = revenue_buckets[revenue_buckets.index(RB)+1] if RB != revenue_buckets[-1] else RB
        params = {
            "Growth_Bucket": GB,
            "Growth_Bucket_Less": GB_L,
            "Growth_Bucket_More": GB_M,
            "Capex_Bucket": CB,
            "Capex_Bucket_Less": CB_L,
            "Capex_Bucket_More": CB_M,
            "Margin_Bucket": MB,
            "Margin_Bucket_Less": MB_L,
            "Margin_Bucket_More": MB_M,
            "Revenue_Bucket": RB,
            "Revenue_Bucket_Less": RB_L,
            "Revenue_Bucket_More": RB_M
        }
        df = pd.read_sql(sql_pcf, conn, params=params)
        return df
        
def pull_comps_fuzzy_minus_capex(GB, MB, RB):
    CB = None
    sql_pcfmc = Path("../sql/pull_comps_fuzzy_minus_capex.sql").read_text()
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        GB_L = growth_buckets[growth_buckets.index(GB)-1] if GB != growth_buckets[0] else GB
        GB_M = growth_buckets[growth_buckets.index(GB)+1] if GB != growth_buckets[-1] else GB
        MB_L = margin_buckets[margin_buckets.index(CB)-1] if MB != margin_buckets[0] else MB
        MB_M = margin_buckets[margin_buckets.index(CB)+1] if MB != margin_buckets[-1] else MB
        RB_L = revenue_buckets[revenue_buckets.index(RB)-1] if RB != revenue_buckets[0] else RB
        RB_M = revenue_buckets[revenue_buckets.index(RB)+1] if RB != revenue_buckets[-1] else RB
        params = {
            "Growth_Bucket": GB,
            "Growth_Bucket_Less": GB_L,
            "Growth_Bucket_More": GB_M,
            "Margin_Bucket": MB,
            "Margin_Bucket_Less": MB_L,
            "Margin_Bucket_More": MB_M,
            "Revenue_Bucket": RB,
            "Revenue_Bucket_Less": RB_L,
            "Revenue_Bucket_More": RB_M
        }
        df = pd.read_sql(sql_pcfmc, conn, params=params)
        return df

def pull_stage_comps(GB, RB):
    sql_psc = Path("../sql/pull_stage_comps.sql").read_text()
    CB = None
    MB = None
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Revenue_Bucket": RB
        }
        df = pd.read_sql(sql_psc, conn, params=params)
        return df

def pull_stage_comps_coverage_median_mean(GB, RB):
    sql_psccmm = Path("../sql/pull_stage_comps_coverage_median_mean.sql").read_text()
    CB = None
    MB = None
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Revenue_Bucket": RB
        }
        df = pd.read_sql(sql_psccmm, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations", "Median_EV_Rev":"Median EV/Rev", "Mean_EV_Rev":"Mean EV/Rev"})
        return df

def pull_stage_comps_plus_margin_coverage_and_median(GB, MB, RB):
    sql_pscpmcam = Path("../sql/pull_stage_comps_plus_margin_coverage_and_median.sql").read_text()
    CB = None
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        params = {
            "Growth_Bucket": GB,
            "Margin_Bucket": MB,
            "Revenue_Bucket": RB
        }
        df = pd.read_sql(sql_pscpmcam, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations", "Median_EV_Rev":"Median EV/Rev"})
        return df

def pull_stage_comps_coverage_and_median_by_margin_bracket(GB, RB):
    sql_psccambmb = Path("../sql/pull_stage_comps_coverage_and_median_by_margin_bracket.sql").read_text()
    CB = None
    MB = None
    check = check_bucket_params(GB, CB, MB, RB)
    if check["Growth Bucket"] != "Valid" or check["Capex Bucket"] != "Valid" or check["Margin Bucket"] != "Valid" or check["Revenue Bucket"] != "Valid":
        return check
    else:
        GM = df_panel[(df_panel["Growth Bucket"] == GB) & (df_panel["Revenue Bucket"] == RB)]["Gross Margin %"].median()
        params = {
            "Growth_Bucket": GB,
            "Revenue_Bucket": RB,
            "Group_Median": GM
        }
        df = pd.read_sql(sql_psccambmb, conn, params=params)
        df = df.rename(columns={"Num_Observations":"Num of Observations", "Median_EV_Rev":"Median EV/Rev"})
        return df
def r(GB,RB):
    GM = df_panel[df_panel["Growth Bucket"] == GB & df_panel["Revenue Bucket"] == RB]["Gross Margin %"].median()
    return GM