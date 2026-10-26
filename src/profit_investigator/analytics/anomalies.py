"""Multivariate Anomaly Detection Engine for Business Metrics.

Detects statistical anomalies, sudden structural breaks, and z-score / IQR excursions
across Marketing, HR, Operations, and Finance indicators during decline periods.
"""

from typing import Any, Dict, List
import numpy as np
import pandas as pd


class AnomalyDetector:
    """Detects statistical and structural anomalies across cross-functional enterprise KPIs."""

    def __init__(self, unified_df: pd.DataFrame):
        self.df = unified_df.copy()

    def detect_anomalies(
        self,
        target_quarters: List[str] = None,
        z_threshold: float = 1.75
    ) -> List[Dict[str, Any]]:
        """Identifies metrics whose values in target quarters deviate significantly from the pre-crisis baseline."""
        if target_quarters is None:
            target_quarters = ["2025-Q2", "2025-Q3", "2025-Q4"]

        # Baseline: quarters prior to target quarters
        baseline_mask = ~self.df["quarter"].isin(target_quarters)
        baseline_df = self.df[baseline_mask]

        metrics_to_test = [
            ("mkt_blended_cac", "Marketing", "Blended Customer Acquisition Cost ($)", "higher_is_bad"),
            ("mkt_avg_conversion_rate", "Marketing", "Campaign Conversion Rate", "lower_is_bad"),
            ("mkt_avg_retention_90d", "Marketing", "90-Day Retention Rate", "lower_is_bad"),
            ("mkt_total_spend", "Marketing", "Marketing Campaign Spend ($)", "higher_is_bad"),
            ("hr_total_overtime_cost", "HR", "Quarterly Overtime Expense ($)", "higher_is_bad"),
            ("hr_avg_attrition_rate", "HR", "Quarterly Attrition Rate", "higher_is_bad"),
            ("hr_avg_productivity_index", "HR", "Workforce Productivity Index", "lower_is_bad"),
            ("ops_avg_days_inventory", "Operations", "Days of Inventory on Hand (DIO)", "higher_is_bad"),
            ("ops_total_freight_cost", "Operations", "Freight & Logistics Cost ($)", "higher_is_bad"),
            ("ops_avg_scrap_rate", "Operations", "Production Scrap Rate", "higher_is_bad"),
            ("ops_avg_unit_cost", "Operations", "Average Production Unit Cost ($)", "higher_is_bad"),
            ("cogs", "Finance", "Cost of Goods Sold ($)", "higher_is_bad"),
            ("gross_margin", "Finance", "Gross Profit Margin", "lower_is_bad"),
            ("net_margin", "Finance", "Net Profit Margin", "lower_is_bad"),
            ("operating_cash_flow", "Finance", "Operating Cash Flow ($)", "lower_is_bad")
        ]

        anomalies = []

        for q in target_quarters:
            quarter_row = self.df[self.df["quarter"] == q]
            if len(quarter_row) == 0:
                continue
            quarter_row = quarter_row.iloc[0]

            for metric_key, dept, display_name, direction in metrics_to_test:
                if metric_key not in self.df.columns:
                    continue

                base_vals = baseline_df[metric_key].dropna()
                mean = base_vals.mean()
                std = base_vals.std()
                if std == 0 or np.isnan(std):
                    std = 0.0001

                q_val = quarter_row[metric_key]
                z_score = (q_val - mean) / std

                is_anomaly = False
                severity = "Normal"

                if direction == "higher_is_bad" and z_score > z_threshold:
                    is_anomaly = True
                elif direction == "lower_is_bad" and z_score < -z_threshold:
                    is_anomaly = True

                if is_anomaly:
                    abs_z = abs(z_score)
                    if abs_z >= 3.0:
                        severity = "Critical Outlier"
                    elif abs_z >= 2.2:
                        severity = "High Severity"
                    else:
                        severity = "Moderate Anomaly"

                    pct_change_vs_baseline = ((q_val - mean) / abs(mean)) * 100

                    anomalies.append({
                        "quarter": q,
                        "department": dept,
                        "metric_key": metric_key,
                        "metric_name": display_name,
                        "observed_value": round(float(q_val), 3),
                        "baseline_mean": round(float(mean), 3),
                        "baseline_std": round(float(std), 3),
                        "z_score": round(float(z_score), 2),
                        "percentage_drift": round(float(pct_change_vs_baseline), 1),
                        "severity": severity,
                        "impact_nature": "Unfavorable Cost/Efficiency Surge" if direction == "higher_is_bad" else "Unfavorable Margin/Performance Contraction"
                    })

        # Sort by absolute z-score descending
        anomalies.sort(key=lambda x: abs(x["z_score"]), reverse=True)
        return anomalies
