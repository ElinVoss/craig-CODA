from __future__ import annotations

from collections import Counter
from pathlib import Path

import yaml

from src.io_utils import read_jsonl, write_json, write_jsonl

from .node_schema import VaultEdge, VaultNode

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "memory_retrieval.yaml"


def load_memory_config(config_path: str | Path | None = None) -> dict:
    path = Path(config_path) if config_path is not None else CONFIG_PATH
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_memory_graph(nodes: list[VaultNode], edges: list[VaultEdge], config_path: str | Path | None = None) -> dict:
    config = load_memory_config(config_path)
    nodes_path = ROOT / config["artifacts"]["nodes_path"]
    edges_path = ROOT / config["artifacts"]["edges_path"]
    index_dir = ROOT / config["artifacts"]["index_report_dir"]
    index_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(nodes_path, [node.to_dict() for node in nodes])
    write_jsonl(edges_path, [edge.to_dict() for edge in edges])
    report = {
        "node_count": len(nodes),
        "edge_count": len(edges),
        "trust_layers": dict(Counter(node.trust_layer for node in nodes)),
        "source_kinds": dict(Counter(node.source_kind for node in nodes)),
        "top_tags": Counter(tag for node in nodes for tag in node.tags).most_common(10),
    }
    write_json(index_dir / "graph_summary.json", report)
    return {
        "nodes_path": str(nodes_path),
        "edges_path": str(edges_path),
        "report_path": str(index_dir / "graph_summary.json"),
    }


def load_memory_graph(config_path: str | Path | None = None) -> tuple[list[VaultNode], list[VaultEdge]]:
    config = load_memory_config(config_path)
    nodes_path = ROOT / config["artifacts"]["nodes_path"]
    edges_path = ROOT / config["artifacts"]["edges_path"]
    if not nodes_path.is_file() or not edges_path.is_file():
        raise FileNotFoundError("Vault graph artifacts are missing. Run scripts/build_vault_graph.py first.")
    nodes = [VaultNode.from_dict(record) for record in read_jsonl(nodes_path)]
    edges = [VaultEdge.from_dict(record) for record in read_jsonl(edges_path)]
    return nodes, edges
