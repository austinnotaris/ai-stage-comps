from __future__ import annotations
from pathlib import Path
import pandas as pd

import sys
ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

from .company_blueprint import Company

REQUIRED_COLS = [
    "name",
    "exchange",
    "ticker",
    "total_rev_usdmm",
    "rev_yoy",
    "gross_margin_pct",
    "capex_usdmm",
    "tev_usdmm",
]

def validate_input(df):
    # required columns
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(
            f"Input CSV missing required columns: {missing}\n"
            f"Expected columns: {REQUIRED_COLS}"
        )

    # numeric coercion 
    numeric_cols = [
        "total_rev_usdmm",
        "rev_yoy",
        "gross_margin_pct",
        "capex_usdmm",
        "tev_usdmm",
    ]
    for c in numeric_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    # check for NaNs after coercion
    bad_rows = df[df[numeric_cols].isna().any(axis=1)]
    if len(bad_rows) > 0:
        raise ValueError(
            "Some rows have missing/non-numeric values in numeric columns.\n"
            "Make sure you did NOT include % signs or $ symbols, and that all numeric fields are filled.\n\n"
            f"Bad rows (showing key columns):\n{bad_rows[['name','ticker'] + numeric_cols]}"
        )

    # 4) small sanity checks
    if (df["total_rev_usdmm"] <= 0).any():
        raise ValueError("total_rev_usdmm must be > 0 for EV/Revenue calculations.")

    return df

def run_company(company, out_dir):
    
    out_dir.mkdir(parents=True, exist_ok=True)

    # Core output tables
    company_data = company.get_company_data()
    exact_comps = company.exact_comps()
    fuzzy_comps = company.fuzzy_comps()
    stage_plus_margin_comps = company.comps_minus_capex()
    stage_plus_margin_fuzzy_comps = company.fuzzy_comps_minus_capex()
    exact_comps_valuation = company.exact_comps_valuation()
    stage_comps_coverage_median_mean = company.stage_comps_coverage_median_mean()
    stage_and_margin_comps_coverage_median_mean = company.stage_comps_plus_margin_coverage_and_median()
    stage_comps_coverage_and_median_by_margin_bracket = company.stage_comps_coverage_and_median_by_margin_bracket()
    valuation_growth_vs_narrative = company.valuation_growth_vs_narrative()

    # Scalar outputs
    summary = {
        "Exact Comps Coverage": company.exact_comps_coverage(),
        "Stage + Margin Comps Coverage": company.comps_minus_capex_coverage(),
        "Change in EV/Rev by Margin": company.change_in_ev_rev_by_margin(),
    }
    pd.DataFrame([summary]).to_csv(out_dir / "summary_metrics.csv", index=False)

    # Save tables
    company_data.to_csv(out_dir / "company_data.csv", index=False)
    exact_comps.to_csv(out_dir / "exact_comps.csv", index=False)
    fuzzy_comps.to_csv(out_dir / "fuzzy_comps.csv", index=False)
    stage_plus_margin_comps.to_csv(out_dir / "stage_plus_margin_comps.csv", index=False)
    stage_plus_margin_fuzzy_comps.to_csv(out_dir / "stage_plus_margin_fuzzy_comps.csv", index=False)
    exact_comps_valuation.to_csv(out_dir / "exact_comps_valuation.csv", index=False)
    stage_comps_coverage_median_mean.to_csv(out_dir / "stage_comps_coverage_median_mean.csv", index=False)
    stage_and_margin_comps_coverage_median_mean.to_csv(
        out_dir / "stage_and_margin_comps_coverage_median_mean.csv", index=False
    )
    stage_comps_coverage_and_median_by_margin_bracket.to_csv(
        out_dir / "stage_comps_coverage_and_median_by_margin_bracket.csv", index=False
    )
    valuation_growth_vs_narrative.to_csv(out_dir / "valuation_growth_vs_narrative.csv", index=False)