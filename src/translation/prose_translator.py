from __future__ import annotations

from src.memory.node_schema import VaultNode


def build_prose_shards(nodes: list[VaultNode]) -> list[dict]:
    shards: list[dict] = []
    for node in nodes:
        if node.trust_layer not in {"prose_voice", "stable_core"}:
            continue
        shards.append(
            {
                "mode": "elin_fiction",
                "shard_type": "prose_style",
                "text": node.content,
                "source_node_id": node.id,
                "source_file": node.source_path,
            }
        )
        shards.append(
            {
                "mode": "craig_default",
                "shard_type": "directness_style",
                "text": node.summary,
                "source_node_id": node.id,
                "source_file": node.source_path,
            }
        )
        shards.append(
            {
                "mode": "rs1_specialty",
                "shard_type": "structural_audit",
                "text": f"Surface the structure first: {node.summary}",
                "source_node_id": node.id,
                "source_file": node.source_path,
            }
        )
    return shards
