# Growth-Stage Comparable Analysis for AI Infrastructure Companies

This repository implements a **growth-stage–adjusted comparable-company framework** for analyzing AI infrastructure and hyperscaling platforms.

The project is designed to:
- Benchmark AI infrastructure companies against historical infrastructure platforms
- Adjust valuation comparisons for scale, growth, and capital intensity
- Produce **reproducible, table-based outputs** rather than ad hoc analysis
- Separate **demo usage** from **batch / production-style analysis**

---

## Repository Structure

    ## Repository Structure

    Ai_Stage_Comps
    ├── README.md
    ├── requirements.txt
    ├── main.py                      # Batch runner (CSV-driven entry point)
    │
    ├── data/
    │   ├── raw/                     # Raw Capital IQ datasets (by industry filters)
    │   └── processed/               # Cleaned, canonical datasets produced by notebooks
    │
    ├── src/
    │   ├── __init__.py
    │   ├── company_blueprint.py     # Company class and core analysis methods
    │   ├── bucket_orders.py         # Canonical ordering of scale / growth buckets
    │   ├── call_sql_queries.py      # SQL execution and formatting helpers
    │   ├── check_bucket_params.py   # Validation logic for stage bucket definitions
    │   ├── stage_classifier.py      # Assigns company-periods to scale/growth stages
    │   ├── yoy_data.py              # YoY revenue calculation utilities
    │   └── runner.py                # Shared execution logic (CSV validation + outputs)
    │
    ├── sql/
    │   └── *.sql                    # SQL queries used to pull and structure raw data
    │
    ├── examples/
    │   ├── run_apld.py              # Single-company demo (Applied Digital)
    │   ├── APLD_outputs/            # Demo outputs (generated when run_apld.py is executed)
    │   └── example_inputs.csv   # Editable input template for main.py
    │
    ├── outputs/
    │   ├── <TICKER>/                # Batch outputs created by main.py (one folder per company)
    │   └── notebook_outputs/        # Precomputed, cross-sectional summary tables
    │       ├── coverage_and_valuation_by_current_stage.csv
    │       ├── coverage_by_regime_all.csv
    │       ├── coverage_by_margin.csv
    │       ├── coverage_by_growth.csv
    │       ├── coverage_by_regime_no_capex.csv
    │       ├── valuation_by_growth_capex.csv
    │       ├── valuation_by_growth_margin.csv
    │       ├── valuation_by_growth_revenue.csv
    │       └── valuation_by_regime_all.csv
    │
    └── notebooks/
        ├── 01_load_and_clean.ipynb       # Load and clean raw Capital IQ data
        ├── 02_build_panel.ipynb          # Construct company-period panel
        ├── 03_stage_definition.ipynb     # Define scale/growth stage framework
        ├── 04_sql_table_outputs.ipynb    # Generate notebook output tables
        └── 05_company_class_test.ipynb   # Validate Company class methods


---

## Installation

This project requires Python 3.9+.

Install dependencies from the repository root:

    pip install -r requirements.txt

---

## Input CSV Format

Batch analysis is driven by a CSV input file.

An example template is provided at:

    examples/example_inputs.csv

Open this file in Excel, Google Sheets, or a text editor to edit or add companies.

### Required Columns

All monetary values must be provided in **USD millions (USDmm)**.  
Growth and margin values must be provided as **decimals**, not percentages.

| Column | Description | Example |
|------|------------|---------|
| `name` | Company name | Applied Digital |
| `exchange` | Listing exchange | NASDAQGS |
| `ticker` | Ticker symbol | APLD |
| `total_rev_usdmm` | Most recent total revenue | 173.6 |
| `rev_yoy` | Year-over-year revenue growth | 0.284 |
| `gross_margin_pct` | Gross margin | 0.226 |
| `capex_usdmm` | Capital expenditures | -686.6 |
| `tev_usdmm` | Total enterprise value | 8718.2 |

### Notes
- Do not rename columns.
- Do not include currency symbols (`$`) or percentage signs (`%`).
- One row represents one company.
- The example file is pre-populated with Applied Digital (APLD) as a working example.  
  You may replace or remove this row, or add additional companies.

---

## Running the Batch Analysis

From the repository root:

    python main.py --input examples/example_inputs.csv --out outputs/

This will:
- Read all companies listed in the input CSV
- Run the full analysis for each company
- Write outputs to:

    outputs/<TICKER>/

(one folder per company)

---

## Running the Applied Digital Demo

A single-company demo is provided for clarity and sanity checking.

Run:

    python examples/run_apld.py

This script:
- Instantiates Applied Digital (APLD) with hard-coded inputs
- Runs the same analysis logic used by the batch runner
- Writes outputs to:

    examples/APLD_outputs/

This demo is **independent of the CSV** and does not affect batch runs.

---

## Outputs

For each company, the following outputs are generated as CSV files:

- Company-level data table
- Exact comparables
- Fuzzy comparables
- Stage-based comparables
- Stage + margin-adjusted comparables
- Valuation summaries and coverage statistics
- Growth vs narrative decomposition tables

## General Summary Tables

In addition to per-company outputs, the repository includes a set of
**precomputed, cross-sectional summary tables** generated in the notebooks.

These tables capture:
- Distributional properties of historical infrastructure companies
- Growth-stage and scale-based benchmarks
- Capital-intensity and margin band summaries
- Aggregate trends used to contextualize company-level outputs

The tables are located at:

    outputs/notebook_outputs/

These files are static artifacts derived from the notebook analysis and are
intended to be inspected directly in Excel or used as reference inputs for
interpretation. They are **not regenerated by `main.py`**.

### Relationship to Per-Company Outputs

- `main.py` and `runner.py` generate **company-specific outputs** under:
  
      outputs/<TICKER>/

- `outputs/tables/` contains **global reference tables** that summarize the
  broader dataset and provide historical context for valuation and stage
  comparisons.

This separation is intentional and reflects the distinction between
**company-level analysis** and **dataset-level benchmarking**.

All outputs are designed to be:
- Machine-readable
- Easy to inspect in Excel
- Easy to aggregate or visualize downstream

---

## Design Principles

- **CSV = configuration**  
  Users edit inputs without touching Python code.

- **Single source of truth for execution**  
  All per-company outputs are generated by a shared runner function reused by both
  the batch runner and the demo script.

- **Separation of concerns**  
  - `company_blueprint.py`: financial logic
  - `runner.py`: execution + output generation
  - `main.py`: CLI orchestration
  - `examples/`: demos and templates

- **No hidden automation**  
  Nothing runs unless explicitly executed by the user.

---

## Notes

- Capital IQ data is proprietary and must be supplied by the user.
- This project focuses on **infrastructure-stage behavior**, not SaaS benchmarks.
- Valuations are framed as **ranges**, not point estimates.

---

## License / Usage

This project is intended for educational and research purposes.