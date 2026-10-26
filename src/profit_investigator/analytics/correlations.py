"""Cross-Functional Correlation and Causal Relationship Engine.

Analyzes statistical correlations, lag effects, lead-lag cross-correlations,
and Granger-causality proxies between Marketing, HR, Operations, and Finance metrics.
Distinguishes clearly between statistical correlation and business causation.
"""

from typing import Any, Dict, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats


class CrossFunctionalRelationshipEngine:
    """Analyzes multivariate interdependencies and lag structures across business silos."""

    def __init__(self, unified_df: pd.DataFrame):
        self.df = unified_df.copy()

    def compute_correlation_matrix(self, target_metric: str = "net_margin") -> pd.DataFrame:
        """Computes Pearson and Spearman correlations of all operational and departmental metrics against target."""
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        exclude = ["quarter_index", "is_decline_quarter"]
        feature_cols = [c for c in numeric_cols if c not in exclude and c != target_metric]

        records = []
        for col in feature_cols:
            series = self.df[col].dropna()
            target_series = self.df.loc[series.index, target_metric].dropna()
            
            # Align indices
            common_idx = series.index.intersection(target_series.index)
            if len(common_idx) < 5 or series.std() == 0 or target_series.std() == 0:
                continue

            r_pearson, p_pearson = stats.pearsonr(series.loc[common_idx], target_series.loc[common_idx])
            r_spearman, p_spearman = stats.spearmanr(series.loc[common_idx], target_series.loc[common_idx])

            # Classify department
            dept = "General"
            if col.startswith("mkt_"):
                dept = "Marketing"
            elif col.startswith("hr_"):
                dept = "HR"
            elif col.startswith("ops_"):
                dept = "Operations"
            elif col in ["cogs", "revenue", "opex_marketing", "opex_ga", "operating_cash_flow", "operating_margin", "gross_margin"]:
                dept = "Finance"

            records.append({
                "metric": col,
                "department": dept,
                "pearson_r": round(float(r_pearson), 3),
                "pearson_p_value": round(float(p_pearson), 4),
                "spearman_rho": round(float(r_spearman), 3),
                "spearman_p_value": round(float(p_spearman), 4),
                "relationship_direction": "Negative Impact" if r_pearson < -0.4 else ("Positive Driver" if r_pearson > 0.4 else "Neutral/Weak")
            })

        corr_df = pd.DataFrame(records)
        corr_df["abs_r"] = corr_df["pearson_r"].abs()
        corr_df = corr_df.sort_values(by="abs_r", ascending=False).drop(columns=["abs_r"]).reset_index(drop=True)
        return corr_df

    def analyze_lagged_impact(self, cause_metric: str, effect_metric: str = "net_margin", max_lags: int = 2) -> Dict[str, Any]:
        """Examines cross-correlation across quarterly time lags (t-0, t-1, t-2)."""
        lag_results = {}
        for lag in range(0, max_lags + 1):
            if lag == 0:
                s_cause = self.df[cause_metric]
                s_effect = self.df[effect_metric]
            else:
                s_cause = self.df[cause_metric].iloc[:-lag].reset_index(drop=True)
                s_effect = self.df[effect_metric].iloc[lag:].reset_index(drop=True)

            if len(s_cause) > 3 and s_cause.std() > 0 and s_effect.std() > 0:
                r, p = stats.pearsonr(s_cause, s_effect)
                lag_results[f"lag_{lag}_quarters"] = {
                    "pearson_r": round(float(r), 3),
                    "p_value": round(float(p), 4),
                    "interpretation": f"{cause_metric} at (t-{lag}) correlates with {effect_metric} at (t) with r={round(float(r), 3)}"
                }

        best_lag = max(lag_results.items(), key=lambda x: abs(x[1]["pearson_r"]))
        return {
            "cause_metric": cause_metric,
            "effect_metric": effect_metric,
            "optimal_lag": best_lag[0],
            "optimal_correlation": best_lag[1]["pearson_r"],
            "lag_breakdown": lag_results
        }

    def evaluate_causality_caveats(self, factor_name: str) -> Dict[str, Any]:
        """Provides rigorous methodology caveats distinguishing correlation from causation."""
        caveats = {
            "mkt_blended_cac": {
                "plausible_mechanism": "High CAC directly increases cost per acquisition while lower lead quality drops retention, directly squeezing net operating margins.",
                "correlation_vs_causation": "Likely Direct Causal Driver & Compounding Effect.",
                "uncertainty_level": "Low (Direct economic linkage via OpEx & revenue churn).",
                "alternative_hypothesis": "External macroeconomic competition or ad platform price inflation may have raised CAC independently."
            },
            "hr_total_overtime_cost": {
                "plausible_mechanism": "Unplanned attrition of experienced personnel necessitated premium overtime shifts and contractor backfills, inflating wage expenses and degrading quality.",
                "correlation_vs_causation": "Plausible Causal Mechanism backed by operational timeline.",
                "uncertainty_level": "Low-to-Medium.",
                "alternative_hypothesis": "Overtime could also be a symptom of sudden production quota shifts rather than solely attrition."
            },
            "ops_avg_days_inventory": {
                "plausible_mechanism": "Surge in days inventory ties up working capital, increases carrying and warehouse fees, and leads to inventory obsolescence write-downs.",
                "correlation_vs_causation": "Strong Causal Contribution to gross margin & operating cash flow erosion.",
                "uncertainty_level": "Low.",
                "alternative_hypothesis": "Supply chain buffer policies instituted post-2024 supply disruption might have intentionally raised inventory targets."
            }
        }
        return caveats.get(factor_name, {
            "plausible_mechanism": "Statistically correlated metric. Cross-departmental qualitative review required before assigning causality.",
            "correlation_vs_causation": "Statistical Correlation - Causality unproven without controlled counterfactual.",
            "uncertainty_level": "Medium-High.",
            "alternative_hypothesis": "May be a co-occurring symptom driven by a deeper shared macroeconomic or operational variable."
        })
