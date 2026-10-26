"""Synthetic data generator for cross-functional business datasets.

Generates 12 quarters (Q1 2023 - Q4 2025) of granular departmental data:
- Marketing (Campaigns, CAC, ROI, Retention, Channel spend)
- HR (Headcount, Salaries, Overtime, Turnover, Productivity)
- Operations (Production cost, Inventory, Scrap rate, Fulfillment, Logistics)
- Finance (Revenue, COGS, OpEx, Gross Profit, Operating Margin, Net Profit, Cash Flow)

Ground-truth injected crisis:
During Q2-Q4 2025 (three consecutive quarters), profitability declines precipitously:
- Marketing maintained high top-of-funnel lead count via heavy paid acquisition, but lead quality collapsed.
  CAC rose from $185 to $340, conversion plummeted from 4.2% to 1.8%, 90-day churn spiked.
- HR reported stable overall headcount, but high engineering/operations attrition led to massive overtime
  (overtime surge +240%), contracting costs, and drop in effective productivity.
- Operations suffered supply chain bottlenecks, stockouts of tier-1 components, carrying excess dead inventory
  (days of inventory jumped from 46 to 88 days), and expedited freight costs escalated (+180%).
- Finance reports shrinking gross margin (from 52% down to 34%) and net margin (from 14.5% to -4.8%),
  even though individual departmental summaries superficially showed "budgets on track" and "targets partially hit".
"""

import json
from pathlib import Path
from typing import Dict, Tuple
import numpy as np
import pandas as pd


def generate_enterprise_data(
    seed: int = 42,
    output_dir: str = "data/raw"
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Generates synthetic historical business datasets for 12 quarters (Q1 2023 to Q4 2025)."""
    np.random.seed(seed)
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    quarters = [
        "2023-Q1", "2023-Q2", "2023-Q3", "2023-Q4",
        "2024-Q1", "2024-Q2", "2024-Q3", "2024-Q4",
        "2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4"
    ]
    n_q = len(quarters)

    # -------------------------------------------------------------
    # 1. Marketing Department Data
    # -------------------------------------------------------------
    # Base baseline
    mkt_rows = []
    channels = ["Paid Search", "Social Media", "Enterprise Events", "Content/Inbound", "Affiliate"]

    for i, q in enumerate(quarters):
        is_crisis = i >= 9  # 2025-Q2, Q3, Q4 (indices 9, 10, 11)
        crisis_severity = (i - 8) if is_crisis else 0  # 1, 2, 3

        base_spend = 1_800_000 + i * 80_000 + (crisis_severity * 350_000)
        # In crisis: spend went up to compensate for falling revenue, CAC inflated
        cac = 180 + i * 2 + (crisis_severity * 60) + np.random.normal(0, 5)
        conv_rate = max(0.012, 0.042 - (i * 0.0005) - (crisis_severity * 0.008) + np.random.normal(0, 0.001))
        retention_rate = max(0.60, 0.88 - (crisis_severity * 0.07) + np.random.normal(0, 0.01))
        leads_generated = int(base_spend / (cac * 0.4))
        acquisitions = int(leads_generated * conv_rate)
        mkt_attributed_rev = acquisitions * (3200 - crisis_severity * 300 + np.random.normal(0, 50))
        mkt_roi = round((mkt_attributed_rev - base_spend) / base_spend, 3)

        for ch in channels:
            ch_share = 0.30 if ch == "Paid Search" else (0.25 if ch == "Social Media" else 0.15)
            ch_spend = base_spend * ch_share * np.random.uniform(0.92, 1.08)
            ch_acq = int(acquisitions * ch_share * np.random.uniform(0.85, 1.15))
            mkt_rows.append({
                "quarter": q,
                "quarter_index": i + 1,
                "channel": ch,
                "campaign_spend": round(ch_spend, 2),
                "leads_generated": int(leads_generated * ch_share),
                "customer_acquisitions": ch_acq,
                "cac": round(ch_spend / max(1, ch_acq), 2),
                "conversion_rate": round(conv_rate * np.random.uniform(0.9, 1.1), 4),
                "retention_rate_90d": round(retention_rate * np.random.uniform(0.95, 1.02), 3),
                "attributed_revenue": round(ch_acq * 3000 * (1 - crisis_severity * 0.08), 2),
                "department_status_reported": "Target Met (Traffic & Leads OK)" if is_crisis else "On Target"
            })

    df_marketing = pd.DataFrame(mkt_rows)

    # -------------------------------------------------------------
    # 2. Human Resources (HR) Data
    # -------------------------------------------------------------
    hr_rows = []
    departments = ["Engineering", "Sales", "Operations", "Marketing", "G&A"]

    for i, q in enumerate(quarters):
        is_crisis = i >= 9
        crisis_severity = (i - 8) if is_crisis else 0

        for dept in departments:
            base_hc = {"Engineering": 160, "Sales": 90, "Operations": 140, "Marketing": 45, "G&A": 35}[dept]
            # Net headcount kept flat or slight growth to hide turnover
            headcount = base_hc + int(i * 1.5) + np.random.randint(-2, 3)
            # High turnover in Ops & Eng during crisis
            attrition_rate = 0.035 if not is_crisis else (0.095 if dept in ["Operations", "Engineering"] else 0.05)
            attrition_rate += np.random.uniform(-0.005, 0.008)
            departures = int(headcount * attrition_rate)
            recruits = departures + np.random.randint(0, 3)
            recruitment_cost = recruits * (12000 if dept in ["Engineering", "Operations"] else 7000)
            
            # Massive overtime in Operations & Engineering
            avg_salary_quarterly = {"Engineering": 32000, "Sales": 24000, "Operations": 18000, "Marketing": 22000, "G&A": 21000}[dept]
            total_salaries = headcount * avg_salary_quarterly
            
            overtime_hours = np.random.randint(400, 900)
            if is_crisis and dept in ["Operations", "Engineering"]:
                overtime_hours = int(overtime_hours * (2.8 + crisis_severity * 0.6))
            overtime_cost = overtime_hours * 55.0

            # Productivity score index (100 base)
            productivity_score = 102.0 - (crisis_severity * 8.5 if dept in ["Operations", "Engineering"] else crisis_severity * 2.0)
            workforce_utilization = min(1.05, 0.84 + (crisis_severity * 0.07 if dept in ["Operations", "Engineering"] else 0.0))

            hr_rows.append({
                "quarter": q,
                "quarter_index": i + 1,
                "department_unit": dept,
                "headcount": headcount,
                "attrition_rate": round(attrition_rate, 4),
                "departures": departures,
                "new_hires": recruits,
                "recruitment_cost": round(recruitment_cost, 2),
                "total_salaries": round(total_salaries, 2),
                "overtime_hours": overtime_hours,
                "overtime_cost": round(overtime_cost, 2),
                "workforce_utilization": round(workforce_utilization, 3),
                "productivity_index": round(productivity_score, 1),
                "department_status_reported": "Headcount Targets Maintained" if is_crisis else "On Plan"
            })

    df_hr = pd.DataFrame(hr_rows)

    # -------------------------------------------------------------
    # 3. Operations Department Data
    # -------------------------------------------------------------
    ops_rows = []
    facilities = ["Plant-North", "Plant-South", "Distribution-Hub-East", "Distribution-Hub-West"]

    for i, q in enumerate(quarters):
        is_crisis = i >= 9
        crisis_severity = (i - 8) if is_crisis else 0

        for fac in facilities:
            units_produced = 45000 + i * 1200 + np.random.randint(-1500, 1500)
            unit_cost = 42.0 + (i * 0.3) + (crisis_severity * 5.2) + np.random.uniform(-0.5, 0.5)
            prod_cost = units_produced * unit_cost
            
            # Inventory buildup and scrap rate increase during crisis
            scrap_rate = 0.021 + (crisis_severity * 0.016) + np.random.uniform(-0.002, 0.003)
            scrap_cost = prod_cost * scrap_rate
            inventory_carrying_val = 5_200_000 + (crisis_severity * 1_850_000) + np.random.uniform(-100_000, 100_000)
            days_of_inventory = 45 + (crisis_severity * 14) + np.random.randint(-2, 3)

            # Logistics & expedited freight
            expedited_freight_pct = 0.03 + (crisis_severity * 0.07)
            freight_base = prod_cost * 0.08
            freight_cost = freight_base * (1 + expedited_freight_pct * 2.2)

            delivery_on_time_rate = max(0.72, 0.96 - (crisis_severity * 0.07) + np.random.uniform(-0.01, 0.01))
            resource_utilization = 0.85 + (crisis_severity * 0.04)

            ops_rows.append({
                "quarter": q,
                "quarter_index": i + 1,
                "facility": fac,
                "units_produced": units_produced,
                "unit_production_cost": round(unit_cost, 2),
                "total_production_cost": round(prod_cost, 2),
                "scrap_rate": round(scrap_rate, 4),
                "scrap_cost": round(scrap_cost, 2),
                "inventory_valuation": round(inventory_carrying_val, 2),
                "days_inventory_on_hand": days_of_inventory,
                "freight_logistics_cost": round(freight_cost, 2),
                "on_time_delivery_rate": round(delivery_on_time_rate, 3),
                "facility_utilization": round(resource_utilization, 3),
                "department_status_reported": "Volume Output Quotas Achieved" if is_crisis else "Optimal"
            })

    df_ops = pd.DataFrame(ops_rows)

    # -------------------------------------------------------------
    # 4. Finance Department Data (Quarterly P&L and Balance Sheet)
    # -------------------------------------------------------------
    fin_rows = []
    for i, q in enumerate(quarters):
        is_crisis = i >= 9
        crisis_severity = (i - 8) if is_crisis else 0

        # Department totals for reconciliation
        mkt_q_spend = df_marketing[df_marketing["quarter"] == q]["campaign_spend"].sum()
        hr_q_salaries = df_hr[df_hr["quarter"] == q]["total_salaries"].sum()
        hr_q_recruiting = df_hr[df_hr["quarter"] == q]["recruitment_cost"].sum()
        hr_q_ot = df_hr[df_hr["quarter"] == q]["overtime_cost"].sum()
        ops_q_prod = df_ops[df_ops["quarter"] == q]["total_production_cost"].sum()
        ops_q_freight = df_ops[df_ops["quarter"] == q]["freight_logistics_cost"].sum()
        ops_q_scrap = df_ops[df_ops["quarter"] == q]["scrap_cost"].sum()

        # Revenue was growing steadily, then flattened or dropped slightly in crisis despite higher spend
        base_rev = 24_000_000 + i * 1_100_000
        if is_crisis:
            # Revenue flattened: 2025 Q2: flat, Q3: -3%, Q4: -6%
            base_rev = 33_500_000 - ((crisis_severity - 1) * 950_000) + np.random.normal(0, 150_000)
        else:
            base_rev += np.random.normal(0, 180_000)

        cogs = (ops_q_prod * 0.65) + ops_q_freight + ops_q_scrap + np.random.normal(0, 50_000)
        gross_profit = base_rev - cogs
        gross_margin = gross_profit / base_rev

        opex_rnd = 2_200_000 + i * 40_000
        opex_mkt = mkt_q_spend * 1.15  # Includes marketing headcount & tooling
        opex_ga = 1_800_000 + (hr_q_recruiting * 1.2) + (hr_q_ot * 0.8)
        total_opex = opex_rnd + opex_mkt + opex_ga

        operating_income = gross_profit - total_opex
        operating_margin = operating_income / base_rev

        tax_and_interest = max(100_000, operating_income * 0.22 if operating_income > 0 else 50_000)
        net_profit = operating_income - tax_and_interest
        net_margin = net_profit / base_rev

        operating_cash_flow = net_profit + 850_000 - (df_ops[df_ops["quarter"] == q]["inventory_valuation"].mean() * 0.08)

        fin_rows.append({
            "quarter": q,
            "quarter_index": i + 1,
            "revenue": round(base_rev, 2),
            "cogs": round(cogs, 2),
            "gross_profit": round(gross_profit, 2),
            "gross_margin": round(gross_margin, 4),
            "opex_marketing": round(opex_mkt, 2),
            "opex_rnd": round(opex_rnd, 2),
            "opex_ga": round(opex_ga, 2),
            "total_opex": round(total_opex, 2),
            "operating_income": round(operating_income, 2),
            "operating_margin": round(operating_margin, 4),
            "net_profit": round(net_profit, 2),
            "net_margin": round(net_margin, 4),
            "operating_cash_flow": round(operating_cash_flow, 2),
            "budgeted_net_profit": round(4_200_000 + i * 250_000, 2),
            "profit_variance_to_budget": round(net_profit - (4_200_000 + i * 250_000), 2),
            "is_decline_quarter": is_crisis
        })

    df_fin = pd.DataFrame(fin_rows)

    # -------------------------------------------------------------
    # 5. Business Events Log (Contextual Qualitative Ledger)
    # -------------------------------------------------------------
    events = [
        {"quarter": "2023-Q1", "event": "ERP system migration completed", "department": "Cross-Functional", "impact_type": "Neutral"},
        {"quarter": "2023-Q3", "event": "Expanded into Tier-2 enterprise clients", "department": "Marketing/Sales", "impact_type": "Positive"},
        {"quarter": "2024-Q2", "event": "New automated packaging line commissioned in Plant-North", "department": "Operations", "impact_type": "Positive"},
        {"quarter": "2024-Q4", "event": "Key senior plant managers and engineering leads departed", "department": "HR", "impact_type": "Negative"},
        {"quarter": "2025-Q1", "event": "Aggressive Paid Search acquisition campaign initiated", "department": "Marketing", "impact_type": "Informative"},
        {"quarter": "2025-Q2", "event": "Supplier component tier-1 shortage triggers expedited air freight; Lead quality drops", "department": "Operations/Marketing", "impact_type": "Critical Negative"},
        {"quarter": "2025-Q3", "event": "Mandatory overtime implemented across distribution and engineering; customer returns increase", "department": "HR/Operations", "impact_type": "Critical Negative"},
        {"quarter": "2025-Q4", "event": "Inventory write-down and compounding customer churn erode net earnings to negative", "department": "Finance/Marketing", "impact_type": "Critical Negative"}
    ]
    df_events = pd.DataFrame(events)

    # Save to disk
    df_marketing.to_csv(out_path / "marketing_quarterly.csv", index=False)
    df_hr.to_csv(out_path / "hr_workforce_quarterly.csv", index=False)
    df_ops.to_csv(out_path / "operations_quarterly.csv", index=False)
    df_fin.to_csv(out_path / "finance_pl_quarterly.csv", index=False)
    df_events.to_csv(out_path / "business_events.csv", index=False)

    metadata = {
        "dataset_name": "Enterprise Profitability Decline Synthetic Benchmark",
        "quarters_count": n_q,
        "date_range": "2023-Q1 to 2025-Q4",
        "crisis_window": ["2025-Q2", "2025-Q3", "2025-Q4"],
        "departments": ["Marketing", "HR", "Operations", "Finance"],
        "injected_mechanisms": [
            "Over-optimistic top-of-funnel ad spend yielding low-intent customers with steep CAC and high 90-day churn",
            "Hidden operational friction: skilled attrition replaced with massive overtime and contractors, reducing overall labor efficiency",
            "Supply chain expedites & inventory bloat: excess slow-moving stock inflating carrying costs + freight surcharges",
            "Siloed departmental reporting: each unit claimed 'targets achieved' (e.g. leads hit, headcount hit, units made) while joint unit economics broke down"
        ]
    }
    with open(out_path / "dataset_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    return df_marketing, df_hr, df_ops, df_fin, df_events


if __name__ == "__main__":
    generate_enterprise_data()
    print("Synthetic enterprise datasets successfully generated in data/raw.")
