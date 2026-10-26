# 📈 AI Profitability Decline Investigation System

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Benchmark Score](https://img.shields.io/badge/Diagnostic%20Score-92.8%2F100-success.svg)]()

> An enterprise-grade, AI-powered business analyst system that integrates cross-functional data across **Marketing, HR, Operations, and Finance** to uncover the systemic root causes behind multi-quarter profitability decline—especially when individual departmental scorecards report "satisfactory" or "on target" performance.

---

## 🎯 Problem Statement

In modern enterprise organizations, business functions typically operate in silos, each evaluating performance through isolated key performance indicators (KPIs):
- **Marketing** optimizes for lead acquisition volumes, total impressions, and top-of-funnel conversion.
- **Human Resources (HR)** tracks aggregate employee headcount and overall hiring budget adherence.
- **Operations** measures gross factory production units and equipment utilization rates.
- **Finance** tracks top-line revenue growth, quarterly expense budgets, and operating margins.

### The Departmental Silo Paradox
A critical enterprise pathology emerges when **company profitability deteriorates over three consecutive quarters, yet every departmental dashboard continues to report green or "on target" status**:
1. Marketing achieved its lead quotas by spending aggressively on broad, low-intent channels—incurring escalating customer acquisition costs (CAC) and high churn that never recoups acquisition spend.
2. HR reported headcount quotas fulfilled by backfilling departures, masking that critical senior plant and engineering personnel left, forcing operations into severe overtime wage penalties and productivity loss.
3. Operations hit output quotas by paying premium expedited air-freight rates and building surplus finished inventory that sat unsold in warehouses, swelling carrying costs and scrap rates.

Because each functional unit achieved its isolated local KPI, **no single department acknowledged responsibility**. Traditional business intelligence tools only report retrospective departmental variances; they fail to model the cross-functional systemic feedback loops that erode enterprise earnings. 

This system provides an **AI-powered cross-functional business analyst** that integrates multidimensional data, identifies systemic root causes across departmental interfaces, distinguishes correlation from causation, and generates prioritized, evidence-backed corrective interventions for executive leadership.

---

## 🌟 Key Features

- **Cross-Functional Data Integration**: Harmonizes siloed datasets (Marketing campaigns, HR workforce dynamics, Operations manufacturing & logistics, Finance P&L) into a unified quarterly analytical view with cross-silo ratios (LTV/CAC, Revenue/Employee, DIO, Turnover).
- **Profitability Inflection & Waterfall Analysis**: Pinpoints the exact quarter profitability turned negative/deteriorated and performs step-by-step P&L variance decomposition across Revenue, COGS, Marketing OpEx, and Labor/G&A.
- **Multivariate Anomaly Detection**: Employs baseline standardized z-score drift tracking to isolate statistically significant cost surges, quality drops, and efficiency contractions.
- **Correlation vs. Causation Engine**: Distinguishes direct accounting causation (e.g., ad spend, air freight) from mechanistic operational causation (e.g., engineer attrition leading to overtime and scrap) and symptomatic correlations (e.g., inventory days).
- **Interactive AI Analyst Agent**: Enables natural-language conversational queries, scenario drills, and automatic generation of C-Suite Executive Briefing reports with verifiable data grounding.
- **Prioritized Strategic Recommendations**: Formulates actionable recovery initiatives categorized by execution horizon (P1 30-Day, P2 60-Day, P3 90-Day, P4 Governance) with quantified financial impact.
- **Comprehensive Evaluation Benchmark**: Includes automated scoring of Timeline Detection Accuracy, Precision, Recall, F1-Score (0.889), and Grounding Coverage (100%).

---

## 🏗️ Repository Architecture

Following modern modular software engineering standards:

```
├── data/
│   ├── raw/                           # Raw Marketing, HR, Ops, Finance, and Events CSVs
│   └── processed/                     # Harmonized cross-functional analytical table
├── docs/
│   ├── use_cases.md                   # Real-world business scenarios & paradoxes
│   ├── how_to_use.md                  # Comprehensive end-to-end user manual
│   ├── api_guide.md                   # Programmatic API, schemas, and CLI reference
│   └── technical_deep_dive.md         # Mathematical models, algorithms & causal logic
├── src/
│   └── profit_investigator/
│       ├── __init__.py
│       ├── cli.py                     # Unified CLI entrypoint
│       ├── data/
│       │   ├── generator.py           # 12-quarter realistic synthetic data generator
│       │   └── integrator.py          # Cross-functional aggregator & ratio engine
│       ├── analytics/
│       │   ├── profitability_trends.py # Inflection detection & Waterfall decomposition
│       │   ├── correlations.py         # Pearson/Spearman & Lead-lag cross-correlations
│       │   ├── anomalies.py            # Z-score outlier detection engine
│       │   └── root_cause.py           # Multi-department root cause synthesis
│       ├── llm/
│       │   └── analyst_agent.py        # Business Analyst Agent & grounding engine
│       ├── evaluation/
│       │   └── evaluator.py            # Precision, Recall, F1 & Benchmark metrics
│       └── ui/
│           └── app.py                 # Multi-page interactive Streamlit dashboard
├── tests/
│   └── test_investigator.py           # Pytest test suite (100% passing)
├── requirements.txt
└── README.md
```

---

## ⚙️ Algorithms and Methodological Overview

The system operates via an integrated 5-stage analytical pipeline designed to convert disparate time series and operational logs into verifiable, causally sound business findings:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 1. Cross-Functional Harmonization & Synthetic Ratio Synthesis               │
│    Aligns quarterly periods; derives joint unit-economic ratios             │
│    (LTV/CAC, Rev/Employee, Days Inventory on Hand, Overtime % of Salaries) │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 2. Inflection Point Detection & P&L Waterfall Walk                          │
│    • Inflection: Detects onset of consecutive quarterly margin drops (t*)   │
│    • Waterfall: Partitions ΔNet Profit into Revenue, COGS, OpEx components  │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 3. Multivariate Anomaly Detection (Standardized Z-Score Drift)              │
│    Calculates z-score deviations against pre-crisis baseline historical     │
│    distributions: flags Moderate (|z|≥1.75), High (≥2.2), and Critical (≥3.0)│
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 4. Cross-Functional Correlation & Lead-Lag Causal Modeling                  │
│    • Pearson (r) & Spearman (ρ) correlation across departmental KPIs        │
│    • Lead-lag cross-correlations (t-0, t-1, t-2) to establish precedence    │
│    • Categorization: Direct Accounting vs. Mechanistic vs. Symptomatic      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│ 5. AI Business Analyst Synthesis & Grounded Executive Action Plan           │
│    Generates audit-ready root cause syntheses (RC-01, RC-02, RC-03) with     │
│    quantified dollar headwinds and prioritized remediation recommendations  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Algorithmic Mechanics

1. **Inflection Point Detection**:
   Monitors the first difference $\Delta M_t = M_t - M_{t-1}$ of net margin $M_t$. The onset inflection quarter $t^*$ is formally identified when margin decline persists consecutively:
   $$t^* = \min \{ t \mid \Delta M_t < 0 \land \Delta M_{t+1} < 0 \land \Delta M_{t+2} < 0 \}$$

2. **P&L Waterfall Cost Variance Decomposition**:
   Decomposes total net profit variance $\Delta \Pi$ from peak baseline $t_0$ to trough $t_k$:
   $$\Delta \Pi = \Delta \text{Revenue} + \Delta \text{COGS}_{\text{headwind}} + \Delta \text{OpEx}_{\text{Mkt}} + \Delta \text{OpEx}_{\text{HR/G\&A}} + \Delta \text{OpEx}_{\text{R\&D}}$$
   Normalizes the absolute headwind contribution of each department to compute proportionate cost culpability.

3. **Multivariate Z-Score Anomaly Engine**:
   For each metric $x$, standardized drift during crisis quarters is scored against the pre-crisis baseline:
   $$z = \frac{x_q - \mu_{\text{baseline}}}{\sigma_{\text{baseline}}}$$
   Flags anomalous cost inflation (CAC $+95\%$, Overtime $+228\%$, Freight $+176\%$) and operational contractions (Productivity $-18.8\%$, Conversion $-58\%$).

4. **Epistemological Causal Categorization**:
   To prevent confabulation and specious correlation, relationships are categorized into three verified tiers:
   - **Direct Accounting Causation** (Deterministic): Ad spend and freight expediting directly debited to OpEx and COGS.
   - **Operational Mechanistic Causation** (High Plausibility): Senior engineer/ops turnover leading with lag $\tau=1$ to elevated overtime and scrap rate.
   - **Symptomatic Correlations** (Co-occurring): Finished inventory buildup tracking with margin decline, acting as both holding cost driver and demand-slump symptom.

---

## 🚀 Quick Start

### 1. Installation
```bash
git clone https://github.com/your-org/profitability-decline-investigator.git
cd profitability-decline-investigator

# Setup virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1    # On Windows
# source venv/bin/activate     # On Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate Synthetic Benchmark Data
```bash
python -m src.profit_investigator.cli --action generate-data
```

### 3. Run Executive Investigation via CLI
```bash
python -m src.profit_investigator.cli --action investigate
```

### 4. Ask the AI Analyst a Question
```bash
python -m src.profit_investigator.cli --action query --prompt "Why did marketing fail despite hitting volume targets?"
```

### 5. Launch the Streamlit Interactive Dashboard
```bash
streamlit run src/profit_investigator/ui/app.py
```
Open [http://localhost:8501](http://localhost:8501) to explore:
1. Executive Overview & Timeline
2. Financial Waterfall Decomposition
3. Departmental Silo Drill-Downs (Marketing, HR, Operations, Finance)
4. Cross-Functional Correlations & Causality Matrix
5. Interactive AI Analyst (Conversational Q&A)
6. System Evaluation & Quality Benchmark

---

## 📊 Evaluation & System Benchmark

The system was evaluated against known ground-truth injected scenarios across 12 quarters:

| Metric | Score | Description |
|---|---|---|
| **Inflection Timeline Accuracy** | **100%** | Accurately detected `2025-Q2` onset of 3 consecutive decline quarters |
| **Quarter Timeline Match (Jaccard)** | **100%** | Full alignment with `2025-Q2`, `2025-Q3`, `2025-Q4` crisis window |
| **Factor Recall** | **100%** | Successfully identified all 12 injected failure mechanisms |
| **Factor Precision** | **80.0%** | High focus on verified crisis drivers with minimal noise |
| **F1 Score** | **0.889** | Robust balance of precision and recall |
| **Insight Grounding Score** | **100%** | Every root cause backed by $\ge 2$ verifiable empirical metric shifts |
| **Department Coverage** | **100%** | Corrective actions directly target Marketing, HR, Ops, and Finance |
| **Overall System Benchmark** | **92.8 / 100** | Exceptional composite analytical performance |

---

## 🧪 Testing

Execute the comprehensive automated test suite:
```bash
pytest tests/test_investigator.py -v
```

---

## 📄 Documentation Links
- [Use Cases & The Silo Paradox](docs/use_cases.md)
- [How to Use Guide](docs/how_to_use.md)
- [API & Interface Reference](docs/api_guide.md)
- [Technical Deep Dive](docs/technical_deep_dive.md)

---

## 🤝 Contribution Guidelines
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewAnalyticsEngine`).
3. Ensure all tests pass (`pytest tests/`).
4. Commit your changes and open a Pull Request.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.

