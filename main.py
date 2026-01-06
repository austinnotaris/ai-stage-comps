from pathlib import Path
import argparse
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parent
sys.path.append(str(ROOT / "src"))

from company_blueprint import Company
from runner import validate_input, run_company


def parse_args():
    p = argparse.ArgumentParser(
        description="Run stage-based comps analysis for one or more companies from a CSV input."
    )
    p.add_argument(
        "--input",
        default="examples/example_inputs.csv",
        help="Path to input CSV (default: examples/example_inputs.csv)",
    )
    p.add_argument(
        "--out",
        default="outputs",
        help="Output directory root (default: outputs)",
    )
    return p.parse_args()


def main():
    args = parse_args()
    input_path = Path(args.input)
    out_root = Path(args.out)

    if not input_path.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_path}")

    # Read as strings first; validate_input will coerce numeric columns
    df = pd.read_csv(input_path, dtype=str)
    df = validate_input(df)

    out_root.mkdir(parents=True, exist_ok=True)

    for _, row in df.iterrows():
        ticker = str(row["ticker"]).upper().strip()
        company_out_dir = out_root / ticker

        company = Company(
            name=row["name"],
            exchange=row["exchange"],
            ticker=ticker,
            total_rev_usdmm=float(row["total_rev_usdmm"]),
            rev_yoy=float(row["rev_yoy"]),
            gross_margin_pct=float(row["gross_margin_pct"]),
            capex_usdmm=float(row["capex_usdmm"]),
            tev_usdmm=float(row["tev_usdmm"]),
        )

        run_company(company, company_out_dir)
        print(f"Wrote outputs for {ticker} → {company_out_dir.resolve()}")

    print("\nDone.")


if __name__ == "__main__":
    main()