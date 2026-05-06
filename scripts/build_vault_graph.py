from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.memory.build_edges import build_edges
from src.memory.classify_nodes import classify_nodes
from src.memory.extract_nodes import extract_nodes
from src.memory.memory_store import save_memory_graph
from src.memory.node_schema import VaultNode
from src.memory.normalize_sources import collect_source_documents

MINED_NODES_DIR = ROOT / "artifacts" / "vault" / "mined_nodes"


def load_mined_nodes() -> list[VaultNode]:
    """Load all pre-built VaultNode records from artifacts/vault/mined_nodes/."""
    nodes: list[VaultNode] = []
    if not MINED_NODES_DIR.is_dir():
        return nodes
    for jsonl_path in sorted(MINED_NODES_DIR.glob("*.jsonl")):
        for line in jsonl_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                nodes.append(VaultNode.from_dict(json.loads(line)))
    return nodes


def main() -> int:
    documents = collect_source_documents()
    print(f"Collected {len(documents)} source documents.")
    source_nodes = classify_nodes(extract_nodes(documents))

    mined = load_mined_nodes()
    if mined:
        # Deduplicate: mined nodes take precedence if ID collides with a source node.
        seen: dict[str, VaultNode] = {n.id: n for n in source_nodes}
        merged_count = 0
        for node in mined:
            if node.id not in seen:
                seen[node.id] = node
                merged_count += 1
        nodes = list(seen.values())
        print(f"Merged {merged_count} mined nodes ({len(mined)} total in mined_nodes/).")
    else:
        nodes = source_nodes

    edges = build_edges(nodes)
    output = save_memory_graph(nodes, edges)
    print(f"Built {len(nodes)} nodes and {len(edges)} edges.")
    print(f"Nodes: {output['nodes_path']}")
    print(f"Edges: {output['edges_path']}")
    print(f"Index report: {output['report_path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
