"""
Usage:
  python scripts/query_memory.py \
    --query "how do side bins work" \
    --emotional 0.6 \
    --circumstantial 0.8 \
    --phase 0.7
"""
import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.episodic.store import EpisodicStore
from src.episodic.retriever import retrieve

ROOT = Path(__file__).parents[1]
cfg = yaml.safe_load((ROOT / "configs/episodic.yaml").read_text())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True)
    p.add_argument("--emotional", type=float, default=0.5)
    p.add_argument("--circumstantial", type=float, default=0.5)
    p.add_argument("--phase", type=float, default=0.5)
    args = p.parse_args()

    store = EpisodicStore(ROOT / "artifacts/episodic/memory.db")
    results = retrieve(
        args.query, store, cfg["weights"], cfg["semantic_model"],
        top_k=cfg["top_k"],
        emotional=args.emotional,
        circumstantial=args.circumstantial,
        developmental_phase=args.phase,
    )

    print(f"\nTop results for: '{args.query}'\n")
    for node, score in results:
        crystal = " [crystallized]" if node.crystallized else ""
        print(f"  {score:.3f}  {node.content[:80]}{crystal}")
        print(f"           domain={node.domain} ctx={node.context_tag} "
              f"reinforced={node.reinforce_count}x")


if __name__ == "__main__":
    main()
