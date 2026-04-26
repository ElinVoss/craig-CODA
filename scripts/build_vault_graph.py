from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.memory.build_edges import build_edges
from src.memory.classify_nodes import classify_nodes
from src.memory.extract_nodes import extract_nodes
from src.memory.memory_store import save_memory_graph
from src.memory.normalize_sources import collect_source_documents


def main() -> int:
    documents = collect_source_documents()
    print(f"Collected {len(documents)} source documents.")
    nodes = classify_nodes(extract_nodes(documents))
    edges = build_edges(nodes)
    output = save_memory_graph(nodes, edges)
    print(f"Built {len(nodes)} nodes and {len(edges)} edges.")
    print(f"Nodes: {output['nodes_path']}")
    print(f"Edges: {output['edges_path']}")
    print(f"Index report: {output['report_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
