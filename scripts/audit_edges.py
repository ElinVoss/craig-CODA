from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.memory.memory_store import load_memory_graph
from src.memory.spreading_activation import edge_is_effectively_propagation_eligible


def build_report() -> dict:
    nodes, edges = load_memory_graph()
    node_by_id = {node.id: node for node in nodes}

    by_type: dict[str, list] = defaultdict(list)
    by_layer_pair: Counter[tuple[str, str]] = Counter()
    eligible_degree: Counter[str] = Counter()
    total_degree: Counter[str] = Counter()

    for edge in edges:
        by_type[edge.edge_type].append(edge)
        left = node_by_id.get(edge.source_id)
        right = node_by_id.get(edge.target_id)
        if left is not None and right is not None:
            pair = tuple(sorted((left.trust_layer, right.trust_layer)))
            by_layer_pair[pair] += 1
        total_degree[edge.source_id] += 1
        total_degree[edge.target_id] += 1
        if edge_is_effectively_propagation_eligible(edge, node_by_id):
            eligible_degree[edge.source_id] += 1
            eligible_degree[edge.target_id] += 1

    edge_type_report = []
    for edge_type, grouped in sorted(by_type.items()):
        weights = [edge.weight for edge in grouped]
        eligible = [edge for edge in grouped if edge_is_effectively_propagation_eligible(edge, node_by_id)]
        edge_type_report.append(
            {
                "edge_type": edge_type,
                "count": len(grouped),
                "eligible_count": len(eligible),
                "eligible_ratio": round(len(eligible) / max(1, len(grouped)), 3),
                "min_weight": round(min(weights), 3),
                "avg_weight": round(sum(weights) / len(weights), 3),
                "max_weight": round(max(weights), 3),
            }
        )

    top_hubs = []
    for node_id, degree in total_degree.most_common(10):
        node = node_by_id.get(node_id)
        if node is None:
            continue
        top_hubs.append(
            {
                "node_id": node_id,
                "summary": node.summary[:80],
                "trust_layer": node.trust_layer,
                "source_path": node.source_path,
                "total_degree": degree,
                "eligible_degree": eligible_degree.get(node_id, 0),
            }
        )

    return {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "eligible_edge_count": sum(
            1 for edge in edges if edge_is_effectively_propagation_eligible(edge, node_by_id)
        ),
        "edge_types": edge_type_report,
        "layer_pairs": [
            {"layer_pair": list(pair), "count": count}
            for pair, count in by_layer_pair.most_common()
        ],
        "top_hubs": top_hubs,
    }


def render_human(report: dict) -> str:
    lines = [
        "Vault Edge Audit",
        "",
        f"Nodes: {report['node_count']}",
        f"Edges: {report['edge_count']}",
        f"Propagation-eligible edges: {report['eligible_edge_count']}",
        "",
        "By edge type:",
    ]
    for item in report["edge_types"]:
        lines.append(
            f"- {item['edge_type']}: count={item['count']} eligible={item['eligible_count']} "
            f"ratio={item['eligible_ratio']:.3f} weight[min/avg/max]={item['min_weight']:.3f}/"
            f"{item['avg_weight']:.3f}/{item['max_weight']:.3f}"
        )
    lines.append("")
    lines.append("Top hubs:")
    for item in report["top_hubs"]:
        lines.append(
            f"- {item['node_id'][:8]} trust={item['trust_layer']} total={item['total_degree']} "
            f"eligible={item['eligible_degree']} source={item['source_path']} summary={item['summary']}"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Inspect vault graph edges before propagation work.")
    parser.add_argument("--output", choices=["human", "json"], default="human")
    args = parser.parse_args()

    report = build_report()
    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render_human(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
