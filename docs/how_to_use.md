# How to Use: Profitability Decline Investigation System

## 1. Prerequisites and Installation

### Environment Setup
Python 3.10+ is recommended. Ensure pip and virtual environments are installed.

```bash
# Clone or navigate to the repository
cd "Profitability Decline Investigation"

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1    # On Windows PowerShell
# source venv/bin/activate     # On Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

---

## 2. Generating & Ingesting Enterprise Data

The system accepts either synthetic benchmark datasets or your enterprise CSV exports for Marketing, HR, Operations, and Finance.

### Generating Synthetic Benchmark Datasets
To generate 12 quarters (Q1 2023 - Q4 2025) of realistic cross-departmental data containing an injected 3-quarter crisis:
```bash
python -m src.profit_investigator.cli --action generate-data
```
This produces raw CSV files under `data/raw/`:
- `marketing_quarterly.csv`: Campaigns, spend, CAC, retention, conversion.
- `hr_workforce_quarterly.csv`: Headcount, attrition, overtime, salaries, productivity.
- `operations_quarterly.csv`: Unit cost, scrap, inventory valuation, days inventory, freight.
- `finance_pl_quarterly.csv`: Revenue, COGS, OpEx, Gross/Net Margins, Operating Cash Flow.
- `business_events.csv`: Qualitative contextual timeline ledger.

---

## 3. Data Integration & Harmonization Pipeline

Run the cross-functional data harmonization step:
```bash
python -m src.profit_investigator.cli --action integrate
```
The integrator will:
1. Aggregate granular channel and departmental records to quarterly granularity.
2. Align all metrics chronologically along unified quarterly indices.
3. Compute derived cross-silo indicators (e.g. `revenue_per_employee`, `mkt_blended_cac`, `inventory_turnover_ratio`, `ltv_to_cac_ratio`).
4. Save the harmonized table to `data/processed/unified_cross_functional.csv`.

---

## 4. Running the Investigation via CLI

### Generating the Executive Investigation Briefing
```bash
python -m src.profit_investigator.cli --action investigate
```
This executes:
- Inflection Point Detection (locating consecutive margin drop quarters).
- Waterfall Variance Decomposition.
- Multivariate Anomaly Detection.
- Cross-Functional Correlation & Granger-style lead-lag tests.
- Root Cause Synthesis & Prioritized Recommendations.

### Asking Natural Language Questions
```bash
python -m src.profit_investigator.cli --action query --prompt "Why did marketing fail despite hitting volume targets?"
```

### Running Model Quality & Benchmarking Evaluation
```bash
python -m src.profit_investigator.cli --action evaluate
```

---

## 5. Launching the Interactive Streamlit Web UI

For interactive dashboard exploration, visual waterfall charts, and conversational Q&A:
```bash
streamlit run src/profit_investigator/ui/app.py
```
Open your browser to `http://localhost:8501`.

The web application contains 6 dedicated tabs:
1. **Executive Overview & Timeline**: Margin trajectory and departmental paradox matrix.
2. **Financial Waterfall Decomposition**: Step-by-step P&L bridge and cost headwinds.
3. **Departmental Silo Drill-Down**: Interactive metric exploration for Marketing, HR, Operations, and Finance.
4. **Cross-Functional Correlations & Causality**: Statistical correlation matrix and causality evaluation.
5. **Interactive AI Analyst (Q&A)**: Conversational inquiry interface.
6. **System Benchmark & Evaluation**: Real-time accuracy, precision, recall, and grounding metrics.

---

## 6. Running Unit and Integration Tests

Run the complete test suite:
```bash
pytest tests/test_investigator.py -v
```
