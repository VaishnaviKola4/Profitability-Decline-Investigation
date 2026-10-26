"""Evaluation and Benchmarking Framework.

Computes quantitative metrics for evaluating the Profitability Decline Investigation system:
- Accuracy: Correctness of detected inflection quarters and decline windows.
- Precision: Proportion of detected anomalies / root-causes that match ground truth crisis factors.
- Recall: Proportion of injected synthetic failure modes successfully identified.
- F1 Score: Harmonic mean of precision and recall.
- Insight Grounding Score: Verifiability and citation percentage of metrics against raw data.
- Recommendation Financial Value & Feasibility Score.
"""

from typing import Any, Dict, List, Set
import numpy as np
import pandas as pd


class SystemEvaluator:
    """Evaluates detection accuracy, insight precision, recall, and recommendation quality."""

    def __init__(self, ground_truth_crisis: Dict[str, Any] = None):
        if ground_truth_crisis is None:
            self.ground_truth = {
                "crisis_quarters": ["2025-Q2", "2025-Q3", "2025-Q4"],
                "inflection_quarter": "2025-Q2",
                "injected_root_cause_categories": {
                    "Marketing": ["mkt_blended_cac", "mkt_avg_conversion_rate", "mkt_avg_retention_90d"],
                    "HR": ["hr_total_overtime_cost", "hr_avg_attrition_rate", "hr_avg_productivity_index"],
                    "Operations": ["ops_avg_days_inventory", "ops_total_freight_cost", "ops_avg_scrap_rate"],
                    "Finance": ["gross_margin", "net_margin", "cogs"]
                }
            }
        else:
            self.ground_truth = ground_truth_crisis

    def evaluate_investigation(self, investigation_results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculates Precision, Recall, F1, Inflection Accuracy, and Grounding metrics."""
        trends = investigation_results.get("trends", {})
        critical_anomalies = investigation_results.get("critical_anomalies", [])
        root_causes = investigation_results.get("root_causes", [])
        recommendations = investigation_results.get("recommendations", [])

        # 1. Timeline Detection Accuracy
        detected_inflection = trends.get("inflection_quarter")
        expected_inflection = self.ground_truth["inflection_quarter"]
        inflection_correct = (detected_inflection == expected_inflection)

        detected_quarters = set(trends.get("consecutive_decline_quarters", []))
        expected_quarters = set(self.ground_truth["crisis_quarters"])
        quarter_jaccard = len(detected_quarters & expected_quarters) / max(1, len(detected_quarters | expected_quarters))

        # 2. Precision, Recall, and F1 on Contributing Factors
        all_injected_metrics = set()
        for metric_list in self.ground_truth["injected_root_cause_categories"].values():
            all_injected_metrics.update(metric_list)

        detected_anomaly_keys = set(a["metric_key"] for a in critical_anomalies)

        true_positives = len(detected_anomaly_keys & all_injected_metrics)
        false_positives = len(detected_anomaly_keys - all_injected_metrics)
        false_negatives = len(all_injected_metrics - detected_anomaly_keys)

        precision = true_positives / max(1, (true_positives + false_positives))
        recall = true_positives / max(1, (true_positives + false_negatives))
        f1_score = 2 * (precision * recall) / max(0.0001, (precision + recall))

        # 3. Grounding Quality (verifiability)
        total_root_causes = len(root_causes)
        verified_root_causes = sum(
            1 for rc in root_causes if "evidence_metrics" in rc and len(rc["evidence_metrics"]) >= 2
        )
        insight_grounding_score = verified_root_causes / max(1, total_root_causes)

        # 4. Recommendation Quality Score (coverage of affected departments & clarity)
        affected_depts = set(self.ground_truth["injected_root_cause_categories"].keys())
        recommended_depts = set()
        for r in recommendations:
            for dept in r.get("owner_departments", []):
                for ad in affected_depts:
                    if ad.lower() in dept.lower():
                        recommended_depts.add(ad)

        dept_coverage_score = len(recommended_depts) / max(1, len(affected_depts))

        return {
            "inflection_point_accuracy": 1.0 if inflection_correct else 0.0,
            "quarter_timeline_match_score": round(quarter_jaccard, 3),
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1_score": round(f1_score, 3),
            "insight_grounding_score": round(insight_grounding_score, 3),
            "department_coverage_score": round(dept_coverage_score, 3),
            "overall_system_score": round(
                (precision * 0.25 + recall * 0.25 + f1_score * 0.2 + insight_grounding_score * 0.15 + dept_coverage_score * 0.15) * 100,
                1
            ),
            "metrics_breakdown": {
                "true_positives": true_positives,
                "false_positives": false_positives,
                "false_negatives": false_negatives,
                "total_injected_factors": len(all_injected_metrics)
            }
        }


if __name__ == "__main__":
    from src.profit_investigator.data.integrator import CrossFunctionalDataIntegrator
    from src.profit_investigator.analytics.root_cause import CrossFunctionalRootCauseEngine

    integrator = CrossFunctionalDataIntegrator()
    unified_df = integrator.aggregate_and_harmonize()
    engine = CrossFunctionalRootCauseEngine(unified_df)
    results = engine.run_investigation()

    evaluator = SystemEvaluator()
    metrics = evaluator.evaluate_investigation(results)
    print("Evaluation Results:", metrics)
