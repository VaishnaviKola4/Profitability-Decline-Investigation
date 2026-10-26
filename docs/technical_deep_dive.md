# Technical Deep Dive: Architecture, Mathematical Formulations, and Causal Reasoning

## 1. Architectural Overview

The **Profitability Decline Investigation System** is designed with a layered, decoupled architecture consisting of five distinct tiers:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       Interactive Presentation Tier                         │
│       Streamlit Multi-Page Web App (app.py)   │   Unified CLI (cli.py)      │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                  Cognitive & Reasoning Tier (LLM / Agent)                   │
│   • BusinessAnalystAgent: Conversational Q&A, Grounded Executive Briefing   │
│   • Uncertainty Framing & Epistemological Boundaries Engine                 │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                    Analytical & Diagnostic Engine Tier                      │
│   • ProfitabilityTrendAnalyzer: Trend & Inflection Point Detection          │
│   • P&L WaterfallDecomposition: Stepwise Operating Profit Attribution       │
│   • CrossFunctionalRelationshipEngine: Pearson / Spearman & Lead-Lag Tests  │
│   • AnomalyDetector: Z-score & Structural Break Detection                   │
│   • CrossFunctionalRootCauseEngine: Multi-Department Synthesis              │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                     Cross-Functional Data Integration Tier                  │
│   • Harmonization of Marketing, HR, Operations, Finance & Events            │
│   • Cross-Silo Derived Ratios (LTV/CAC, Rev/Employee, Turnover, DIO)        │
└──────────────────────────────────────┬──────────────────────────────────────┘
                                       │
┌──────────────────────────────────────▼──────────────────────────────────────┐
│                       Data Layer & Benchmarks                               │
│     Marketing CSV  │  HR CSV  │  Operations CSV  │  Finance P&L CSV         │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Mathematical & Algorithmic Formulations

### 2.1 Inflection Point Detection Algorithm
To locate the exact onset of multi-quarter profitability erosion, the system tracks the second difference of the Net Margin series $M_t = \frac{\text{Net Profit}_t}{\text{Revenue}_t}$:

$$\Delta M_t = M_t - M_{t-1}$$

A confirmed inflection period $t^*$ satisfies:
$$t^* = \min \{ t \mid \Delta M_t < 0 \land \Delta M_{t+1} < 0 \land \Delta M_{t+2} < 0 \}$$

This guarantees that temporary quarterly fluctuations are not misidentified as structural multi-quarter crises.

---

### 2.2 P&L Waterfall Variance Decomposition
Between a healthy baseline quarter $t_0$ (e.g. 2025-Q1) and the trough crisis quarter $t_k$ (e.g. 2025-Q4), total net income variance $\Delta \Pi$ is algebraically partitioned into mutually exclusive components:

$$\Delta \Pi = \Pi_{t_k} - \Pi_{t_0} = \Delta \text{Rev} + \Delta \text{COGS}_{\text{impact}} + \Delta \text{OpEx}_{\text{Mkt}} + \Delta \text{OpEx}_{\text{GA}} + \Delta \text{OpEx}_{\text{R\&D}}$$

Where:
- $\Delta \text{Rev} = \text{Revenue}_{t_k} - \text{Revenue}_{t_0}$
- $\Delta \text{COGS}_{\text{impact}} = -(\text{COGS}_{t_k} - \text{COGS}_{t_0})$
- $\Delta \text{OpEx}_{\text{Mkt}} = -(\text{OpEx}_{\text{Mkt}, t_k} - \text{OpEx}_{\text{Mkt}, t_0})$
- $\Delta \text{OpEx}_{\text{GA}} = -(\text{OpEx}_{\text{GA}, t_k} - \text{OpEx}_{\text{GA}, t_0})$

The headwind share attributed to department $d$ is given by:

$$S_d = \frac{|\Delta \text{Cost}_d|}{\sum_{j} |\Delta \text{Cost}_j|} \times 100\%$$

---

### 2.3 Multivariate Anomaly Detection (Z-Score Standardized Drift)
For each departmental metric $x$ in a crisis quarter $q \in Q_{\text{crisis}}$, its standardized departure from pre-crisis historical mean $\mu_{\text{baseline}}$ and standard deviation $\sigma_{\text{baseline}}$ is computed:

$$z = \frac{x_q - \mu_{\text{baseline}}}{\sigma_{\text{baseline}}}$$

A metric is flagged as an anomaly if:
$$|z| \ge \theta_z \quad (\text{default } \theta_z = 1.75)$$

Severity tiers:
- **Moderate Anomaly:** $1.75 \le |z| < 2.2$
- **High Severity:** $2.2 \le |z| < 3.0$
- **Critical Outlier:** $|z| \ge 3.0$

---

### 2.4 Lead-Lag Cross-Correlation & Granger Causality Proxies
To discover whether operational bottlenecks preceded financial margin drops, the system computes the lagged Pearson correlation coefficient $r(\tau)$ for lag offsets $\tau \in \{0, 1, 2\}$ quarters:

$$r(\tau) = \frac{\sum_{t} (x_{t-\tau} - \bar{x}) (y_t - \bar{y})}{\sqrt{\sum_{t} (x_{t-\tau} - \bar{x})^2 \sum_{t} (y_t - \bar{y})^2}}$$

An optimal lag $\tau^* = \arg\max_\tau |r(\tau)|$ reveals whether an operational indicator $x$ serves as a leading indicator ($\tau^* \ge 1$) for financial margin deterioration $y$.

---

## 3. Epistemological Causal Reasoning Framework

To prevent the AI assistant from presenting statistical coincidences as proven causes, the engine enforces a three-level epistemological classification:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Level 1: Direct Accounting Causation                                        │
│ Direct cash outflow that flows straight into P&L line items.               │
│ • Example: Marketing Paid Ad Spend, Air-Freight Surcharges.                 │
│ • Certainty: High. Mathematical certainty via financial accounting.        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Level 2: Mechanistic Operational Causation                                  │
│ Plausible operational chain supported by timeline precedence (lag t-1 -> t).│
│ • Example: Senior engineer attrition leading to overtime and scrap surge.  │
│ • Certainty: Medium-High. Grounded in temporal precedence & field context.  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Level 3: Symptomatic / Co-Occurring Correlations                            │
│ Metric tracks with decline, but is both a consequence and amplifier.       │
│ • Example: Days Inventory on Hand (DIO).                                    │
│ • Certainty: Requires explicit uncertainty communication in briefings.      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Evaluation and Ground-Truth Scoring Metrics

The system's diagnostic fidelity is quantified across six objective evaluation dimensions:

1. **Inflection Point Accuracy:**
   $$\mathbb{I}(\hat{t}^* = t^*_{\text{ground\_truth}})$$

2. **Precision:**
   $$\text{Precision} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Positives}}$$

3. **Recall:**
   $$\text{Recall} = \frac{\text{True Positives}}{\text{True Positives} + \text{False Negatives}}$$

4. **F1-Score:**
   $$F_1 = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

5. **Insight Grounding Score:**
   $$\text{Grounding} = \frac{\text{Root Causes with } \ge 2 \text{ Verifiable Empirical Data Points}}{\text{Total Root Causes Generated}}$$

6. **Department Coverage Score:**
   $$\text{Coverage} = \frac{|\text{Departments Addressed in Recommendations} \cap \text{Distressed Departments}|}{|\text{Distressed Departments}|}$$

