from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "src"))

from company_blueprint import Company
from runner import run_company


def run_apld_example():
    apld = Company(
        name="Applied Digital",
        exchange="NASDAQGS",
        ticker="APLD",
        total_rev_usdmm=173.6,
        rev_yoy=0.284,
        gross_margin_pct=0.226,
        capex_usdmm=-686.6,
        tev_usdmm=8718.2,
    )
    out_dir = ROOT / "examples" / "APLD"
    run_company(apld, out_dir)

    print(f"✅ APLD example written to: {out_dir.resolve()}")


if __name__ == "__main__":
    run_apld_example()
