# Company requires Name, Exchange, Ticker, Total Rev, Rev YoY, Gross Margin %, Capex, TEV 

import pandas as pd

import sys
sys.path.append("../src")
from stage_classifier import stage_classifier
from call_sql_queries import *

class Company:
    def __init__(self,name,exchange,ticker,total_rev_usdmm,rev_yoy,gross_margin_pct,capex_usdmm,tev_usdmm):
        self.df = pd.DataFrame([[name,exchange,ticker,total_rev_usdmm,rev_yoy,gross_margin_pct,capex_usdmm]],
                                    columns=["Company Name",
                                             "Exchange",
                                             "Ticker",
                                             "Total Revenue ($USDmm)",
                                             "Revenue YoY",
                                             "Gross Margin %",
                                             "Capital Expenditure ($USDmm)"])
        self.df["Total Revenue ($USDmm)"] = pd.to_numeric(self.df["Total Revenue ($USDmm)"], errors="coerce")
        self.df["Revenue YoY"] = pd.to_numeric(self.df["Revenue YoY"], errors="coerce")
        self.df["Gross Margin %"] = pd.to_numeric(self.df["Gross Margin %"], errors="coerce")
        self.df["Capital Expenditure ($USDmm)"] = pd.to_numeric(self.df["Capital Expenditure ($USDmm)"], errors="coerce")
        self.df["Capex to Rev"] = (self.df["Capital Expenditure ($USDmm)"]/self.df["Total Revenue ($USDmm)"]).round(4)
        self.df = stage_classifier(self.df)
        self.df["TEV"] = tev_usdmm
        self.df["TEV"] = pd.to_numeric(self.df["TEV"], errors="coerce")
        self.df["EV/Rev"] = self.df["TEV"]/self.df["Total Revenue ($USDmm)"]

    def exact_comps(self):
        return pull_comps_exact(self.df["Growth Bucket"].item(), self.df["Capex Bucket"].item(), self.df["Margin Bucket"].item(), self.df["Revenue Bucket"].item())

    def comps_minus_capex(self):
        return pull_comps_minus_capex(self.df["Growth Bucket"].item(), self.df["Margin Bucket"].item(), self.df["Revenue Bucket"].item())

    def fuzzy_comps(self):
        return pull_comps_fuzzy(self.df["Growth Bucket"].item(), self.df["Capex Bucket"].item(), self.df["Margin Bucket"].item(), self.df["Revenue Bucket"].item())

    def fuzzy_comps_minus_capex(self):
        return pull_comps_fuzzy_minus_capex(self.df["Growth Bucket"].item(), self.df["Margin Bucket"].item(), self.df["Revenue Bucket"].item())

    def stage_comps(self):
        return pull_stage_comps(self.df["Growth Bucket"].item(), self.df["Revenue Bucket"].item())

    def exact_comps_coverage(self):
        df_count = coverage_by_regime(self.df["Growth Bucket"].item(), self.df["Capex Bucket"].item(), self.df["Margin Bucket"].item(), self.df["Revenue Bucket"].item(), None, None)
        if df_count.empty:
            return 0
        else:
            return df_count["Num of Observations"].item()

    def comps_minus_capex_coverage(self):
        df_count = coverage_by_regime_minus_capex(self.df["Growth Bucket"].item(), self.df["Margin Bucket"].item(), self.df["Revenue Bucket"].item(), None, None)
        if df_count.empty:
            return 0
        else:
            return df_count["Num of Observations"].item()
    
    def exact_comps_valuation(self):
        df_valuation = valuation_by_regime(self.df["Growth Bucket"].item(), self.df["Capex Bucket"].item(), self.df["Margin Bucket"].item(), self.df["Revenue Bucket"].item(), None, None)
        return df_valuation.iloc[:,4:]

    def stage_comps_coverage_and_valuation(self):
        df_stage_comps = coverage_and_valuation_by_current_stage(self.df["Growth Bucket"].item(), self.df["Revenue Bucket"].item())
        return df_stage_comps.iloc[:,2:]

    def stage_comps_coverage_median_mean(self):
        df_stage_comps_med = pull_stage_comps_coverage_median_mean(self.df["Growth Bucket"].item(), self.df["Revenue Bucket"].item())
        return df_stage_comps_med.iloc[:,2:]

    def stage_comps_plus_margin_coverage_and_median(self):
        df_stage_comps_plus_margin_med = pull_stage_comps_plus_margin_coverage_and_median(self.df["Growth Bucket"].item(), self.df["Margin Bucket"].item(), self.df["Revenue Bucket"].item())
        return df_stage_comps_plus_margin_med.iloc[:,2:]

    def stage_comps_coverage_and_median_by_margin_bracket(self):
        df_stage_comps_med_by_margin = pull_stage_comps_coverage_and_median_by_margin_bracket(self.df["Growth Bucket"].item(), self.df["Revenue Bucket"].item())
        return df_stage_comps_med_by_margin.iloc[:,1:]

    def get_company_data(self):
        return self.df

    def get_ev_to_rev(self):
        return self.df["EV/Rev"].item()

    def valuation_growth_vs_narrative(self):
        df_company = self.get_company_data()
        company_ev_rev = df_company["EV/Rev"].item()
        df_stage_comps = self.stage_comps_coverage_median_mean()
        stage_comps_ev_rev = df_stage_comps["Median EV/Rev"].item()
        df_stage_margin_comps = self.stage_comps_plus_margin_coverage_and_median()
        stage_margin_comps_ev_rev = df_stage_margin_comps["Median EV/Rev"].item()
        one_minus_stage_margin_comps_ev_rev = 1-stage_margin_comps_ev_rev
        data = {
            "Metric": ["Actual", "Explained by Growth", "Explained by Growth + Margin", "Narrative/Future Assumptions"],
            "Formula": ["EV/Rev", "(Stage Comps Median EV/Rev)/(Actual EV/Rev)", "(Stage + Margin Comps Median EV/Rev)/(Actual EV/Rev)", "1-(Stage + Margin Comps Median EV/Rev)/(Actual EV/Rev)"],
            "Result": [1, stage_comps_ev_rev/company_ev_rev, stage_margin_comps_ev_rev/company_ev_rev, 1-(stage_margin_comps_ev_rev/company_ev_rev)]
        }
        df_vgvn = pd.DataFrame(data)
        return df_vgvn

    def change_in_ev_rev_by_margin(self):
        df_stage_comps = self.stage_comps_coverage_median_mean()
        stage_comps_ev_rev = df_stage_comps["Median EV/Rev"].item()
        df_stage_margin_comps = self.stage_comps_plus_margin_coverage_and_median()
        stage_margin_comps_ev_rev = df_stage_margin_comps["Median EV/Rev"].item()
        change = stage_margin_comps_ev_rev - stage_comps_ev_rev
        if change>0:
            return f"{change} > 0 → margin rewarded"
        elif change<0:
            return f"{change} < 0 → margin penalized"
        else:
            return f"{change} = 0 → margin neutral" 