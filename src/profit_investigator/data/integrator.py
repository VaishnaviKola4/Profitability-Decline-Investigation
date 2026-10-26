"""Unified cross-functional data loader and integrator.

Loads raw CSVs from Marketing, HR, Operations, and Finance, performs data validation,
aligns time periods, computes cross-departmental derived metrics, and outputs a canonical
unified quarterly dataframe for multidimensional root-cause analysis.
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import numpy as np
import pandas as pd


class CrossFunctionalDataIntegrator:
    """Integrates marketing, HR, operations, and financial datasets into a harmonized view."""

    def __init__(self, data_dir: str = "data/raw"):
        self.data_dir = Path(data_dir)
        self.marketing_df: Optional[pd.DataFrame] = None
        self.hr_df: Optional[pd.DataFrame] = None
        self.ops_df: Optional[pd.DataFrame] = None
        self.finance_df: Optional[pd.DataFrame] = None
        self.events_df: Optional[pd.DataFrame] = None
        self.unified_df: Optional[pd.DataFrame] = None

    def load_data(self) -> Dict[str, pd.DataFrame]:
        """Loads all raw datasets from disk."""
        self.marketing_df = pd.read_csv(self.data_dir / "marketing_quarterly.csv")
        self.hr_df = pd.read_csv(self.data_dir / "hr_workforce_quarterly.csv")
        self.ops_df = pd.read_csv(self.data_dir / "operations_quarterly.csv")
        self.finance_df = pd.read_csv(self.data_dir / "finance_pl_quarterly.csv")
        
        events_path = self.data_dir / "business_events.csv"
        if events_path.exists():
            self.events_df = pd.read_csv(events_path)
            
        return {
            "marketing": self.marketing_df,
            "hr": self.hr_df,
            "operations": self.ops_df,
            "finance": self.finance_df,
            "events": self.events_df
        }

    def aggregate_and_harmonize(self) -> pd.DataFrame:
        """Aggregates sub-department / channel-level metrics to quarterly level and merges with finance."""
        if self.finance_df is None:
            self.load_data()

        # 1. Aggregate Marketing to quarterly
        mkt_agg = self.marketing_df.groupby("quarter").agg(
            mkt_total_spend=("campaign_spend", "sum"),
            mkt_total_leads=("leads_generated", "sum"),
            mkt_total_acquisitions=("customer_acquisitions", "sum"),
            mkt_avg_cac=("cac", "mean"),
            mkt_avg_conversion_rate=("conversion_rate", "mean"),
            mkt_avg_retention_90d=("retention_rate_90d", "mean"),
            mkt_attributed_rev=("attributed_revenue", "sum")
        ).reset_index()

        # Weighted CAC & blended metrics
        mkt_agg["mkt_blended_cac"] = mkt_agg["mkt_total_spend"] / mkt_agg["mkt_total_acquisitions"].replace(0, 1)

        # 2. Aggregate HR to quarterly
        hr_agg = self.hr_df.groupby("quarter").agg(
            hr_total_headcount=("headcount", "sum"),
            hr_avg_attrition_rate=("attrition_rate", "mean"),
            hr_total_departures=("departures", "sum"),
            hr_total_new_hires=("new_hires", "sum"),
            hr_total_recruitment_cost=("recruitment_cost", "sum"),
            hr_total_salaries=("total_salaries", "sum"),
            hr_total_overtime_hours=("overtime_hours", "sum"),
            hr_total_overtime_cost=("overtime_cost", "sum"),
            hr_avg_productivity_index=("productivity_index", "mean"),
            hr_avg_workforce_utilization=("workforce_utilization", "mean")
        ).reset_index()

        # 3. Aggregate Operations to quarterly
        ops_agg = self.ops_df.groupby("quarter").agg(
            ops_total_units_produced=("units_produced", "sum"),
            ops_avg_unit_cost=("unit_production_cost", "mean"),
            ops_total_prod_cost=("total_production_cost", "sum"),
            ops_avg_scrap_rate=("scrap_rate", "mean"),
            ops_total_scrap_cost=("scrap_cost", "sum"),
            ops_total_inventory_val=("inventory_valuation", "sum"),
            ops_avg_days_inventory=("days_inventory_on_hand", "mean"),
            ops_total_freight_cost=("freight_logistics_cost", "sum"),
            ops_avg_on_time_delivery=("on_time_delivery_rate", "mean"),
            ops_avg_utilization=("facility_utilization", "mean")
        ).reset_index()

        # 4. Merge with Finance
        unified = pd.merge(self.finance_df, mkt_agg, on="quarter", how="left")
        unified = pd.merge(unified, hr_agg, on="quarter", how="left")
        unified = pd.merge(unified, ops_agg, on="quarter", how="left")

        # Sort chronologically by quarter_index
        unified = unified.sort_values("quarter_index").reset_index(drop=True)

        # 5. Compute Advanced Cross-Functional Ratio Indicators
        # Efficiency and burn ratios
        unified["marketing_intensity_pct"] = (unified["mkt_total_spend"] / unified["revenue"]) * 100
        unified["overtime_pct_of_salaries"] = (unified["hr_total_overtime_cost"] / unified["hr_total_salaries"]) * 100
        unified["revenue_per_employee"] = unified["revenue"] / unified["hr_total_headcount"]
        unified["gross_profit_per_employee"] = unified["gross_profit"] / unified["hr_total_headcount"]
        unified["freight_pct_of_cogs"] = (unified["ops_total_freight_cost"] / unified["cogs"]) * 100
        unified["inventory_turnover_ratio"] = unified["cogs"] / unified["ops_total_inventory_val"]
        unified["customer_lifetime_value_proxy"] = (unified["revenue"] / unified["mkt_total_acquisitions"].replace(0, 1)) * unified["mkt_avg_retention_90d"]
        unified["ltv_to_cac_ratio"] = unified["customer_lifetime_value_proxy"] / unified["mkt_blended_cac"]

        # QoQ Growth / Delta metrics
        for col in ["revenue", "gross_profit", "net_profit", "gross_margin", "net_margin", "mkt_blended_cac", "ops_avg_days_inventory", "hr_total_overtime_cost"]:
            unified[f"{col}_qoq_pct"] = unified[col].pct_change() * 100

        self.unified_df = unified
        return unified

    def save_processed(self, output_path: str = "data/processed/unified_cross_functional.csv") -> Path:
        """Saves the unified cross-functional analytical table."""
        if self.unified_df is None:
            self.aggregate_and_harmonize()

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        self.unified_df.to_csv(out, index=False)
        return out


if __name__ == "__main__":
    integrator = CrossFunctionalDataIntegrator()
    df = integrator.aggregate_and_harmonize()
    integrator.save_processed()
    print(f"Data integrated successfully. Shape: {df.shape}, Columns: {len(df.columns)}")
