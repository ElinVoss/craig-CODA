"""
Audit the vault edge graph before enabling spreading activation.

Reports:
  - Edge count by type
  - Degree distribution (mean, max, p95) per edge type
  - Top 20 hub nodes with summaries
  - Isolated nodes (zero edges)
  - Top 10 tags driving the most shared_tag edges
  - Propagation-eligible vs ineligible edge counts
"""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.memory.memory_store import load_memory_graph

PROPAGATION_ELIGIBLE = {"shared_link", "shared_project"}


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    idx = int(len(sorted_vals) * pct / 100)
    return sorted_vals[min(idx, len(sorted_vals) - 1)]


def main() -> None:
    print("Loading vault graph...")
    nodes, edges = load_memory_graph()
    nodes_by_id = {n.id: n for n in nodes}

    # --- Edge counts by type ---
    by_type: dict[str, list] = defaultdict(list)
    for edge in edges:
        by_type[edge.edge_type].append(edge)

    print(f"\n{'='*60}")
    print(f"EDGE AUDIT REPORT")
    print(f"{'='*60}")
    print(f"\nTotal edges : {len(edges):,}")
    print(f"Total nodes : {len(nodes):,}")
    print(f"\nEdge counts by type:")
    for etype, elist in sorted(by_type.items(), key=lambda x: -len(x[1])):
        eligible = "propagation-eligible" if etype in PROPAGATION_ELIGIBLE else "blocked"
        print(f"  {etype:<20} {len(elist):>8,}   [{eligible}]")

    # --- Degree distribution ---
    degree: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for edge in edges:
        degree[edge.edge_type][edge.source_id] += 1
        degree[edge.edge_type][edge.target_id] += 1

    print(f"\nDegree distribution per edge type (mean / p95 / max):")
    for etype in sorted(by_type.keys()):
        vals = list(degree[etype].values())
        if not vals:
            continue
        mean = sum(vals) / len(vals)
        p95 = percentile(vals, 95)
        mx = max(vals)
        print(f"  {etype:<20}  mean={mean:5.1f}  p95={p95:5.0f}  max={mx:5}")

    # --- Overall degree (all edge types combined) ---
    overall_degree: dict[str, int] = defaultdict(int)
    for edge in edges:
        overall_degree[edge.source_id] += 1
        overall_degree[edge.target_id] += 1

    isolated = [n.id for n in nodes if n.id not in overall_degree]
    print(f"\nIsolated nodes (zero edges): {len(isolated):,}")

    # --- Top 20 hub nodes ---
    top_hubs = sorted(overall_degree.items(), key=lambda x: -x[1])[:20]
    print(f"\nTop 20 hub nodes (all edge types):")
    print(f"  {'degree':>6}  {'node_id':<20}  {'type':<20}  summary")
    print(f"  {'-'*6}  {'-'*20}  {'-'*20}  {'-'*40}")
    for node_id, deg in top_hubs:
        node = nodes_by_id.get(node_id)
        if node:
            summary = node.summary[:60].replace("\n", " ") if node.summary else node.content[:60].replace("\n", " ")
            print(f"  {deg:>6}  {node_id:<20}  {node.node_type:<20}  {summary}")
        else:
            print(f"  {deg:>6}  {node_id:<20}  (node not found in vault)")

    # --- Tags driving most shared_tag edges ---
    tag_edge_counts: Counter = Counter()
    for edge in by_type.get("shared_tag", []):
        tag_edge_counts[edge.rationale] += 1

    print(f"\nTop 10 tags driving shared_tag edges (hub risk):")
    for rationale, count in tag_edge_counts.most_common(10):
        tag = rationale.replace("shared tag: ", "")
        # count nodes with this tag
        nodes_with_tag = sum(1 for n in nodes if tag in n.tags)
        print(f"  {count:>6,} edges   {nodes_with_tag:>5} nodes   tag={tag!r}")

    # --- Propagation-eligible summary ---
    eligible_count = sum(len(v) for k, v in by_type.items() if k in PROPAGATION_ELIGIBLE)
    blocked_count = len(edges) - eligible_count

    eligible_degree: dict[str, int] = defaultdict(int)
    for edge in edges:
        if edge.edge_type in PROPAGATION_ELIGIBLE:
            eligible_degree[edge.source_id] += 1
            eligible_degree[edge.target_id] += 1

    print(f"\nPropagation eligibility summary:")
    print(f"  Eligible edges  : {eligible_count:,}  ({100*eligible_count/max(1,len(edges)):.1f}%)")
    print(f"  Blocked edges   : {blocked_count:,}  ({100*blocked_count/max(1,len(edges)):.1f}%)")
    if eligible_degree:
        vals = list(eligible_degree.values())
        print(f"  Eligible degree : mean={sum(vals)/len(vals):.1f}  max={max(vals)}")
    print()


if __name__ == "__main__":
    main()
