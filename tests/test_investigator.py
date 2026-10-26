"""Comprehensive test suite for the Profitability Decline Investigation system."""

import pytest
import pandas as pd
import numpy as np
from src.profit_investigator.data.generator import generate_enterprise_data
from src.profit_investigator.data.integrator import CrossFunctionalDataIntegrator
from src.profit_investigator.analytics.profitability_trends import ProfitabilityTrendAnalyzer
from src.profit_investigator.analytics.correlations import CrossFunctionalRelationshipEngine
from src.profit_investigator.analytics.anomalies import AnomalyDetector
from src.profit_investigator.analytics.root_cause import CrossFunctionalRootCauseEngine
from src.profit_investigator.llm.analyst_agent import BusinessAnalystAgent
from src.profit_investigator.evaluation.evaluator import SystemEvaluator


@pytest.fixture(scope="session")
def datasets():
    mkt, hr, ops, fin, events = generate_enterprise_data(seed=42)
    return {"mkt": mkt, "hr": hr, "ops": ops, "fin": fin, "events": events}


@pytest.fixture(scope="session")
def unified_dataframe(datasets):
    integrator = CrossFunctionalDataIntegrator()
    df = integrator.aggregate_and_harmonize()
    return df


def test_data_generation_shape_and_quarters(datasets):
    mkt = datasets["mkt"]
    fin = datasets["fin"]
    assert len(fin) == 12
    assert "2025-Q4" in fin["quarter"].values
    assert mkt["campaign_spend"].sum() > 0


def test_data_integrator_ratios(unified_dataframe):
    df = unified_dataframe
    assert len(df) == 12
    assert "revenue_per_employee" in df.columns
    assert "mkt_blended_cac" in df.columns
    assert "inventory_turnover_ratio" in df.columns
    assert df["net_margin"].iloc[-1] < df["net_margin"].iloc[0]


def test_inflection_detection(unified_dataframe):
    analyzer = ProfitabilityTrendAnalyzer(unified_dataframe)
    trends = analyzer.identify_decline_periods()
    assert trends["inflection_quarter"] == "2025-Q2"
    assert len(trends["consecutive_decline_quarters"]) >= 3


def test_waterfall_decomposition(unified_dataframe):
    analyzer = ProfitabilityTrendAnalyzer(unified_dataframe)
    wf = analyzer.compute_profitability_waterfall("2025-Q1", "2025-Q4")
    assert wf["total_variance"] < 0
    assert len(wf["waterfall_steps"]) == 7
    assert "Operations (COGS & Scrap & Logistics)" in wf["department_headwind_shares"]


def test_correlations(unified_dataframe):
    engine = CrossFunctionalRelationshipEngine(unified_dataframe)
    corr_df = engine.compute_correlation_matrix("net_margin")
    assert not corr_df.empty
    assert "pearson_r" in corr_df.columns
    assert "spearman_rho" in corr_df.columns


def test_anomaly_detection(unified_dataframe):
    detector = AnomalyDetector(unified_dataframe)
    anomalies = detector.detect_anomalies(["2025-Q2", "2025-Q3", "2025-Q4"])
    assert len(anomalies) > 0
    mkt_anomalies = [a for a in anomalies if a["department"] == "Marketing"]
    assert len(mkt_anomalies) > 0


def test_root_cause_engine(unified_dataframe):
    engine = CrossFunctionalRootCauseEngine(unified_dataframe)
    res = engine.run_investigation()
    assert len(res["root_causes"]) == 3
    assert len(res["recommendations"]) >= 3
    assert res["root_causes"][0]["id"] == "RC-01"


def test_analyst_agent_queries(unified_dataframe):
    engine = CrossFunctionalRootCauseEngine(unified_dataframe)
    res = engine.run_investigation()
    agent = BusinessAnalystAgent(res, unified_dataframe)
    
    ans_mkt = agent.ask_analyst("Tell me about marketing and CAC")
    assert "CAC" in ans_mkt["response"]
    
    ans_hr = agent.ask_analyst("What happened with HR overtime?")
    assert "Overtime" in ans_hr["response"]


def test_system_evaluator_metrics(unified_dataframe):
    engine = CrossFunctionalRootCauseEngine(unified_dataframe)
    res = engine.run_investigation()
    evaluator = SystemEvaluator()
    eval_metrics = evaluator.evaluate_investigation(res)
    assert eval_metrics["inflection_point_accuracy"] == 1.0
    assert eval_metrics["recall"] == 1.0
    assert eval_metrics["f1_score"] > 0.8
    assert eval_metrics["overall_system_score"] > 85.0
