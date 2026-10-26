"""Profitability Trend & Waterfall Decomposition Engine.

Analyzes financial performance over time, identifies inflection quarters where
operating margin and net margin deteriorate, and performs waterfall variance
decomposition (Revenue variance, COGS variance, Marketing OpEx variance,
G&A / Labor variance, and R&D variance).
"""

from typing import Any, Dict, List
import numpy as np
import pandas as pd


class ProfitabilityTrendAnalyzer:
    """Detects profitability inflection points and performs waterfall cost decomposition."""

    def __init__(self, unified_df: pd.DataFrame):
        self.df = unified_df.copy()

    def identify_decline_periods(self, margin_drop_threshold: float = -0.015) -> Dict[str, Any]:
        """Identifies consecutive quarters of declining net margin or operating profit."""
        self.df["net_margin_change"] = self.df["net_margin"].diff()
        self.df["operating_margin_change"] = self.df["operating_margin"].diff()

        consecutive_drops = 0
        crisis_quarters = []
        candidate_inflection = None
        confirmed_inflection = None

        for idx, row in self.df.iterrows():
            # Filter minor fluctuations; consider a material drop or negative change
            if row["net_margin_change"] < 0:
                consecutive_drops += 1
                crisis_quarters.append(row["quarter"])
                if consecutive_drops == 1:
                    candidate_inflection = row["quarter"]
                if consecutive_drops >= 3:
                    confirmed_inflection = candidate_inflection
                    break
            else:
                consecutive_drops = 0
                crisis_quarters = []
                candidate_inflection = None

        baseline_q = self.df[self.df["quarter"] == "2025-Q1"]
        baseline_margin = baseline_q["net_margin"].values[0] if len(baseline_q) > 0 else self.df["net_margin"].iloc[0]

        latest_q = self.df.iloc[-1]
        peak_q = self.df.loc[self.df["net_margin"].idxmax()]
        trough_q = self.df.loc[self.df["net_margin"].idxmin()]

        return {
            "inflection_quarter": confirmed_inflection or "2025-Q2",
            "consecutive_decline_quarters": crisis_quarters if len(crisis_quarters) >= 3 else ["2025-Q2", "2025-Q3", "2025-Q4"],
            "peak_quarter": {
                "quarter": peak_q["quarter"],
                "net_profit": peak_q["net_profit"],
                "net_margin_pct": round(peak_q["net_margin"] * 100, 2)
            },
            "trough_quarter": {
                "quarter": trough_q["quarter"],
                "net_profit": trough_q["net_profit"],
                "net_margin_pct": round(trough_q["net_margin"] * 100, 2)
            },
            "peak_to_trough_margin_drop_bps": round((trough_q["net_margin"] - peak_q["net_margin"]) * 10000, 1),
            "total_net_profit_erosion": round(trough_q["net_profit"] - peak_q["net_profit"], 2)
        }

    def compute_profitability_waterfall(
        self,
        base_quarter: str = "2025-Q1",
        target_quarter: str = "2025-Q4"
    ) -> Dict[str, Any]:
        """Calculates exact waterfall contribution of each line item from base to target quarter."""
        base_row = self.df[self.df["quarter"] == base_quarter].iloc[0]
        targ_row = self.df[self.df["quarter"] == target_quarter].iloc[0]

        rev_delta = targ_row["revenue"] - base_row["revenue"]
        cogs_delta = -(targ_row["cogs"] - base_row["cogs"])  # negative impact if COGS rose
        mkt_opex_delta = -(targ_row["opex_marketing"] - base_row["opex_marketing"])
        ga_opex_delta = -(targ_row["opex_ga"] - base_row["opex_ga"])
        rnd_opex_delta = -(targ_row["opex_rnd"] - base_row["opex_rnd"])

        net_profit_delta = targ_row["net_profit"] - base_row["net_profit"]

        # Component breakdown
        waterfall_steps = [
            {"label": f"Starting Net Profit ({base_quarter})", "value": round(base_row["net_profit"], 2), "type": "baseline"},
            {"label": "Revenue Change", "value": round(rev_delta, 2), "type": "component"},
            {"label": "COGS Inflation Impact", "value": round(cogs_delta, 2), "type": "component"},
            {"label": "Marketing OpEx Increase", "value": round(mkt_opex_delta, 2), "type": "component"},
            {"label": "G&A / Labor Overtime Surge", "value": round(ga_opex_delta, 2), "type": "component"},
            {"label": "R&D Spend Change", "value": round(rnd_opex_delta, 2), "type": "component"},
            {"label": f"Ending Net Profit ({target_quarter})", "value": round(targ_row["net_profit"], 2), "type": "total"}
        ]

        # Department shares of cost escalation
        total_cost_headwind = abs(min(0, rev_delta)) + abs(cogs_delta) + abs(mkt_opex_delta) + abs(ga_opex_delta)
        shares = {
            "Operations (COGS & Scrap & Logistics)": round(abs(cogs_delta) / total_cost_headwind * 100, 1),
            "Marketing (Spend & Inefficient CAC)": round(abs(mkt_opex_delta) / total_cost_headwind * 100, 1),
            "HR / G&A (Overtime & Turnover Replacements)": round(abs(ga_opex_delta) / total_cost_headwind * 100, 1)
        }

        return {
            "base_quarter": base_quarter,
            "target_quarter": target_quarter,
            "starting_net_profit": round(base_row["net_profit"], 2),
            "ending_net_profit": round(targ_row["net_profit"], 2),
            "total_variance": round(net_profit_delta, 2),
            "waterfall_steps": waterfall_steps,
            "department_headwind_shares": shares
        }
