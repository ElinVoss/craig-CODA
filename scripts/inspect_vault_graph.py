from __future__ import annotations

from collections import Counter
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.memory.memory_store import load_memory_graph


def main() -> int:
    nodes, edges = load_memory_graph()
    print(f"Nodes: {len(nodes)}")
    print(f"Edges: {len(edges)}")
    print("Trust layers:")
    for layer, count in Counter(node.trust_layer for node in nodes).most_common():
        print(f"- {layer}: {count}")
    print("\nSample nodes:")
    for node in nodes[:5]:
        print(f"- {node.id} | {node.trust_layer} | {node.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
