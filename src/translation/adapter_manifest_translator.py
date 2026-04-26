from __future__ import annotations

from pathlib import Path

import yaml

from src.io_utils import write_json
from src.memory.node_schema import VaultNode

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "adapter_targets.yaml"
OUTPUT_DIR = ROOT / "artifacts" / "translation" / "adapter_manifests"


def build_adapter_manifests(nodes: list[VaultNode]) -> list[dict]:
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    manifests: list[dict] = []
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for target in config["targets"]:
        include_layers = set(target["include_layers"])
        matched = [node for node in nodes if node.trust_layer in include_layers]
        manifest = {
            "name": target["name"],
            "description": target["description"],
            "preferred_modes": target["preferred_modes"],
            "include_layers": target["include_layers"],
            "node_count": len(matched),
            "source_node_ids": [node.id for node in matched],
        }
        write_json(OUTPUT_DIR / f"{target['name']}.json", manifest)
        manifests.append(manifest)
    return manifests
