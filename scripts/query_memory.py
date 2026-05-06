"""
Usage:
  python scripts/query_memory.py --query "how do side bins work"
  python scripts/query_memory.py --query "..." --output full   # JSON: {memory_context, routing_block}
  python scripts/query_memory.py --query "..." --output render  # bare context block for injection
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.memory.graph_router import derive_routing
from src.memory.memory_store import load_memory_graph
from src.memory.query_classifier import classify_query_profile
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
    p.add_argument(
        "--output",
        choices=["human", "render", "full"],
        default="human",
        help=(
            "human: decorated console output; "
            "render: bare context block for injection; "
            "full: JSON with {memory_context, routing_block} for the agent server"
        ),
    )
    args = p.parse_args()

    results = retrieve_nodes(
        query=args.query,
        retrieval_profile=args.profile,
        mode=args.mode,
        top_k=args.top_k,
    )

    if args.output == "render":
        if results:
            print(render_memory_context(build_memory_context(results)))
        return

    if args.output == "full":
        # Derive routing from graph structure of retrieved nodes
        _, edges = load_memory_graph()
        profile_used = args.profile or classify_query_profile(args.query)
        routing = derive_routing(results, edges, profile_used)
        memory_context = render_memory_context(build_memory_context(results)) if results else ""
        print(json.dumps({
            "memory_context": memory_context,
            "routing_block": routing.render_routing_block(),
        }))
        return

    # human output
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
