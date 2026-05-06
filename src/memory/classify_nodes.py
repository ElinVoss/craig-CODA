from __future__ import annotations

from pathlib import Path

import yaml

from .node_schema import VaultNode

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "node_schema.yaml"


def load_node_schema(config_path: str | Path | None = None) -> dict:
    path = Path(config_path) if config_path is not None else CONFIG_PATH
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def classify_nodes(nodes: list[VaultNode], config_path: str | Path | None = None) -> list[VaultNode]:
    schema = load_node_schema(config_path)
    path_rules = schema.get("path_rules", [])
    content_rules = schema.get("content_rules", {})
    classified: list[VaultNode] = []
    for node in nodes:
        lowered_path = node.source_path.lower()
        lowered_content = node.content.lower()
        trust_layer = node.trust_layer
        node_type = node.node_type
        privacy_level = node.privacy_level
        for rule in path_rules:
            marker = str(rule["contains"]).lower()
            if marker in lowered_path:
                trust_layer = str(rule["trust_layer"])
                node_type = str(rule["node_type"])
                privacy_level = str(rule["privacy_level"])
                break
        if any(marker in lowered_content for marker in content_rules.get("review_markers", [])):
            trust_layer = "review_only"
            privacy_level = "restricted"
        elif trust_layer != "review_only" and any(
            marker in lowered_content for marker in content_rules.get("interpretive_markers", [])
        ):
            trust_layer = "interpretive_maps"
        # DF-01: curated_memory nodes tagged #stable_core are identity/preference facts,
        # not episodic events — promote regardless of folder path.
        if node.source_kind == "curated_memory" and "#stable_core" in node.content:
            trust_layer = "stable_core"
        node.trust_layer = trust_layer
        node.node_type = node_type
        node.privacy_level = privacy_level
        classified.append(node)
    return classified
