# Use Cases: Profitability Decline Investigation & Cross-Functional Root Cause Analysis

## Overview
This document details real-world scenarios and diagnostic use cases where individual functional departments report 'satisfactory' or 'green' operational health, yet the overarching enterprise suffers multi-quarter margin erosion and profitability collapse.

---

## Use Case 1: The "Lead-Volume Mirage" (Marketing vs. Finance)

### Scenario
The Marketing department launches an aggressive acquisition push across paid digital channels. At the quarterly board review, the CMO presents a glowing scorecard:
- **Lead Volume:** 112% of target
- **Gross Customer Acquisitions:** Up 18% QoQ
- **Marketing Campaign Budget:** Maintained strictly within quarterly allocated limits

### The Hidden Breakdown
In reality, the marketing team achieved lead targets by loosening keyword match types and targeting broader audiences. 
- **Customer Acquisition Cost (CAC):** Inflated from \$185 to \$362 (+95%)
- **Lead-to-Paid Conversion Rate:** Collapsed from 4.15% to 1.74% (-58%)
- **90-Day Retention Rate:** Slipped from 88% to 64% (-27%)

### How Profitability Investigator Diagnoses This
1. The **Data Integrator** joins marketing acquisitions with quarterly finance cohort revenues.
2. The **Correlation Engine** identifies that CAC holds a -0.92 correlation with consolidated net margin.
3. The **Root Cause Engine** flags `RC-01`: "Marketing Efficiency Collapse & Customer Quality Degradation", exposing that customer lifetime value (LTV) dropped below CAC, turning marketing spend into a net margin headwind.

---

## Use Case 2: The "Overtime Attrition Trap" (HR vs. Operations)

### Scenario
The Vice President of HR reports that total corporate headcount is stable (within 2% of budget) and recruitment quotas were met. 

### The Hidden Breakdown
While overall headcount numbers were maintained, voluntary attrition among experienced plant supervisors and senior engineers spiked to 9.8% per quarter. To hit delivery commitments with junior staff and open vacancies, plant managers instituted emergency overtime:
- **Overtime Expense:** Surged from \$420,000 to \$1,380,000 per quarter (+228%)
- **Workforce Productivity Index:** Declined from 101.4 to 82.3 (-18.8%)
- **Operational Scrap:** Climbed from 2.1% to 5.4% due to operator fatigue and onboarding re-work

### How Profitability Investigator Diagnoses This
1. The **Anomaly Detector** flags quarterly overtime expenses with a z-score of +3.4 ("Critical Outlier").
2. The **Waterfall Decomposition** attributes 28% of the total operating profit contraction to G&A / overtime wage surges.
3. The **Root Cause Engine** generates `RC-02`, showing that headcount stability was an artificial facade masking institutional brain-drain and premium wage leakages.

---

## Use Case 3: Supply Chain Expedites & The Working Capital Squeeze (Operations vs. Finance)

### Scenario
The Operations COO reports that factory output quotas and unit volume production were 100% fulfilled.

### The Hidden Breakdown
Supply chain bottlenecks on tier-1 components forced the procurement team to pay exorbitant air-freight surcharges to avoid line shutdowns. Simultaneously, finished goods accumulated because customer churn diminished downstream sales:
- **Expedited Freight Costs:** Rose +176% to \$3.45M per quarter
- **Days of Inventory on Hand (DIO):** Jumped from 46 days to 87 days
- **Cost of Goods Sold (COGS):** Inflated, compressing gross margin from 52% to 34%
- **Operating Cash Flow:** Severely compromised due to tied-up working capital

### How Profitability Investigator Diagnoses This
1. The **Waterfall Decomposition** measures direct COGS escalation and freight inflation.
2. The **Lagged Impact Engine** proves that supply chain lead-time delays at $t-1$ directly triggered gross margin decline at $t$.
3. The system generates actionable recommendation `P3`: transitioning to Demand-Driven Material Requirements Planning (DDMRP) and dual-sourcing tier-1 parts.

---

## Use Case 4: C-Suite Multi-Departmental Strategic Alignment

### Scenario
The CEO and CFO require an audit-ready, non-partisan explanation of why net earnings turned from \$14.0M in Q1 2025 to \$7.8M in Q4 2025, with prioritized interventions for the upcoming fiscal plan.

### System Output Delivered
- **Waterfall P&L Walk:** Exact dollar attribution of margin compression across COGS, Marketing OpEx, and G&A.
- **Correlation Matrix with Epistemological Caveats:** Clear demarcation between direct accounting causation and co-occurring symptoms.
- **Prioritized Corrective Roadmap:** P1 (30-day), P2 (60-day), and P3 (90-day) initiatives mapped to specific department owners with projected financial run-rate impact (\$4.1M+ total annualized EBITDA recovery).
