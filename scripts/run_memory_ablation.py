from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.memory.retrieve_topk import retrieve_nodes
from src.memory.score_fusion import load_query_profiles


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect how each retrieval score dimension affects ranking.")
    parser.add_argument("--query", required=True)
    parser.add_argument("--profile", default="technical")
    parser.add_argument("--mode", default="craig_default")
    args = parser.parse_args()

    results = retrieve_nodes(query=args.query, retrieval_profile=args.profile, mode=args.mode, top_k=6)
    weights = load_query_profiles()["profiles"][args.profile]["weights"]
    print(f"Baseline results for profile={args.profile}\n")
    for result in results:
        print(f"- {result.total_score:.3f} {result.node.summary}")

    print("\nAblation deltas")
    for dimension, weight in weights.items():
        print(f"\nWithout {dimension}:")
        rescored = []
        for result in results:
            contribution = weight * result.breakdown[dimension] * result.breakdown["trust_multiplier"]
            rescored.append((result.total_score - contribution, result.node.summary))
        for score, summary in sorted(rescored, key=lambda item: item[0], reverse=True):
            print(f"- {score:.3f} {summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
