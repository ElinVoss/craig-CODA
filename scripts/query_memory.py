"""
Usage:
  python scripts/query_memory.py --query "how do side bins work"
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.memory.retrieve_topk import retrieve_nodes
from src.memory.update_reinforcement import update_reinforcement
from src.translation.runtime_context_translator import build_memory_context, render_memory_context


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--query", required=True)
    p.add_argument("--profile", default=None)
    p.add_argument("--mode", default="craig_default")
    p.add_argument("--top-k", type=int, default=None)
    p.add_argument("--reinforce", action="store_true")
    args = p.parse_args()

    results = retrieve_nodes(
        query=args.query,
        retrieval_profile=args.profile,
        mode=args.mode,
        top_k=args.top_k,
    )

    print(f"\nTop results for: '{args.query}'\n")
    for result in results:
        node = result.node
        print(f"  {result.total_score:.3f}  {node.summary}")
        print(
            f"           trust={node.trust_layer} source={node.source_path} "
            f"reinforced={node.reinforcement_count}x"
        )
    if args.reinforce and results:
        update_reinforcement([result.node.id for result in results])
        print("\nApplied reinforcement to retrieved nodes.")
    if results:
        print("\nRendered Memory Context\n")
        print(render_memory_context(build_memory_context(results)))


if __name__ == "__main__":
    main()
