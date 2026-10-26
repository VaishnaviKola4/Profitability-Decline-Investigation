"""CLI Entrypoint for the Profitability Decline Investigator.

Usage:
    python -m src.profit_investigator.cli --action investigate
    python -m src.profit_investigator.cli --action generate-data
    python -m src.profit_investigator.cli --action evaluate
    python -m src.profit_investigator.cli --action query --prompt "Why did marketing fail?"
"""

import argparse
import io
import json
import os
import sys
from pathlib import Path

# Fix Windows console UTF-8 output encoding
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Add project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from src.profit_investigator.data.generator import generate_enterprise_data
from src.profit_investigator.data.integrator import CrossFunctionalDataIntegrator
from src.profit_investigator.analytics.root_cause import CrossFunctionalRootCauseEngine
from src.profit_investigator.llm.analyst_agent import BusinessAnalystAgent
from src.profit_investigator.evaluation.evaluator import SystemEvaluator


def main():
    parser = argparse.ArgumentParser(
        description="Profitability Decline Investigation - Cross-Functional AI Business Analyst"
    )
    parser.add_argument(
        "--action",
        choices=["generate-data", "integrate", "investigate", "evaluate", "query"],
        default="investigate",
        help="Action to execute"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="What caused the profitability decline over the last three quarters?",
        help="Query to ask the analyst agent (used with --action query)"
    )

    args = parser.parse_args()

    if args.action == "generate-data":
        print(">> Generating synthetic enterprise datasets...")
        generate_enterprise_data()
        print(">> Generation complete in data/raw.")

    elif args.action == "integrate":
        print(">> Harmonizing departmental data...")
        integrator = CrossFunctionalDataIntegrator()
        df = integrator.aggregate_and_harmonize()
        out = integrator.save_processed()
        print(f">> Harmonization complete. Saved {df.shape[0]} quarters and {df.shape[1]} metrics to {out}.")

    elif args.action == "investigate":
        print(">> Running Full Cross-Functional Investigation...")
        integrator = CrossFunctionalDataIntegrator()
        df = integrator.aggregate_and_harmonize()
        engine = CrossFunctionalRootCauseEngine(df)
        results = engine.run_investigation()
        agent = BusinessAnalystAgent(results, df)
        briefing = agent.generate_executive_briefing()
        print("\n" + briefing)

    elif args.action == "evaluate":
        print(">> Evaluating System Performance...")
        integrator = CrossFunctionalDataIntegrator()
        df = integrator.aggregate_and_harmonize()
        engine = CrossFunctionalRootCauseEngine(df)
        results = engine.run_investigation()
        evaluator = SystemEvaluator()
        metrics = evaluator.evaluate_investigation(results)
        print("\n=== SYSTEM BENCHMARK RESULTS ===")
        print(json.dumps(metrics, indent=2))

    elif args.action == "query":
        integrator = CrossFunctionalDataIntegrator()
        df = integrator.aggregate_and_harmonize()
        engine = CrossFunctionalRootCauseEngine(df)
        results = engine.run_investigation()
        agent = BusinessAnalystAgent(results, df)
        ans = agent.ask_analyst(args.prompt)
        print(f"\nUser Query: {args.prompt}\n")
        print("Analyst Assessment:")
        print(ans["response"])


if __name__ == "__main__":
    main()
