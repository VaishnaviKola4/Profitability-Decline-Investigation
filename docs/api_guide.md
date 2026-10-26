# API and Interface Guide

## Overview
The **Profitability Decline Investigation System** provides programmatic APIs, a Command-Line Interface (CLI), and a modern Streamlit web user interface.

---

## 1. Programmatic Python API

### Core Modules and Classes

| Module | Primary Class | Purpose |
|---|---|---|
| `src.profit_investigator.data.generator` | `generate_enterprise_data` | Generates 12 quarters of synthetic cross-departmental data. |
| `src.profit_investigator.data.integrator` | `CrossFunctionalDataIntegrator` | Harmonizes Marketing, HR, Ops, and Finance tables. |
| `src.profit_investigator.analytics.profitability_trends` | `ProfitabilityTrendAnalyzer` | Detects inflection quarters and computes waterfall walks. |
| `src.profit_investigator.analytics.correlations` | `CrossFunctionalRelationshipEngine` | Analyzes Pearson/Spearman correlations and lag impacts. |
| `src.profit_investigator.analytics.anomalies` | `AnomalyDetector` | Computes baseline z-scores and flags significant excursions. |
| `src.profit_investigator.analytics.root_cause` | `CrossFunctionalRootCauseEngine` | Synthesizes quantitative findings into validated root causes. |
| `src.profit_investigator.llm.analyst_agent` | `BusinessAnalystAgent` | Executive briefing and conversational natural-language Q&A. |
| `src.profit_investigator.evaluation.evaluator` | `SystemEvaluator` | Evaluates Precision, Recall, F1, Grounding, and Accuracy. |

---

### Python Code Example

```python
from src.profit_investigator.data.integrator import CrossFunctionalDataIntegrator
from src.profit_investigator.analytics.root_cause import CrossFunctionalRootCauseEngine
from src.profit_investigator.llm.analyst_agent import BusinessAnalystAgent
from src.profit_investigator.evaluation.evaluator import SystemEvaluator

# 1. Integrate data
integrator = CrossFunctionalDataIntegrator(data_dir="data/raw")
unified_df = integrator.aggregate_and_harmonize()

# 2. Run investigation pipeline
engine = CrossFunctionalRootCauseEngine(unified_df)
investigation = engine.run_investigation()

# Inspect detected root causes
for rc in investigation["root_causes"]:
    print(f"[{rc['id']}] {rc['title']} - Confidence: {rc['confidence_score']*100}%")

# 3. Ask the AI Analyst
agent = BusinessAnalystAgent(investigation, unified_df)
response = agent.ask_analyst("What caused the sudden gross margin contraction?")
print(response["response"])

# 4. Evaluate system accuracy
evaluator = SystemEvaluator()
metrics = evaluator.evaluate_investigation(investigation)
print("System F1-Score:", metrics["f1_score"])
```

---

## 2. Command Line Interface (CLI)

The CLI entrypoint is `src.profit_investigator.cli`.

```
usage: python -m src.profit_investigator.cli [-h] [--action {generate-data,integrate,investigate,evaluate,query}] [--prompt PROMPT]

Profitability Decline Investigation - Cross-Functional AI Business Analyst

options:
  -h, --help            show this help message and exit
  --action {generate-data,integrate,investigate,evaluate,query}
                        Action to execute (default: investigate)
  --prompt PROMPT       Query to ask the analyst agent (used with --action query)
```

### CLI Exit Codes
- `0`: Execution succeeded without errors.
- `1`: Unhandled exception or missing dependencies.

---

## 3. Data Schema & Contracts

### Input File Requirements (`data/raw/`)
1. **`marketing_quarterly.csv`**:
   - `quarter` (str, e.g. "2023-Q1")
   - `channel` (str)
   - `campaign_spend` (float)
   - `leads_generated` (int)
   - `customer_acquisitions` (int)
   - `conversion_rate` (float)
   - `retention_rate_90d` (float)

2. **`hr_workforce_quarterly.csv`**:
   - `quarter` (str)
   - `department_unit` (str)
   - `headcount` (int)
   - `attrition_rate` (float)
   - `total_salaries` (float)
   - `overtime_cost` (float)
   - `productivity_index` (float)

3. **`operations_quarterly.csv`**:
   - `quarter` (str)
   - `facility` (str)
   - `units_produced` (int)
   - `unit_production_cost` (float)
   - `scrap_cost` (float)
   - `inventory_valuation` (float)
   - `days_inventory_on_hand` (int)
   - `freight_logistics_cost` (float)

4. **`finance_pl_quarterly.csv`**:
   - `quarter` (str)
   - `revenue` (float)
   - `cogs` (float)
   - `gross_profit` (float)
   - `gross_margin` (float)
   - `opex_marketing` (float)
   - `opex_ga` (float)
   - `net_profit` (float)
   - `net_margin` (float)
   - `operating_cash_flow` (float)
