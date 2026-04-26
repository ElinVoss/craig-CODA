from __future__ import annotations

from src.memory.node_schema import VaultNode


def _fluffy_variant(text: str) -> str:
    return f"It may be useful to gently consider a broad version of this idea: {text}"


def build_preference_records(nodes: list[VaultNode]) -> list[dict]:
    records: list[dict] = []
    for index, node in enumerate(nodes, start=1):
        if node.trust_layer not in {"stable_core", "project_constraints", "episodic_events"}:
            continue
        records.append(
            {
                "id": f"context-pref-{index:04d}",
                "prompt": f"Choose the better response style for guidance drawn from {node.source_path}.",
                "chosen": node.summary,
                "rejected": _fluffy_variant(node.summary),
                "notes": "Chosen response is more direct. Rejected variant is too soft / too generic / too fluffy.",
                "source_file": node.source_path,
                "source_node_id": node.id,
            }
        )
    return records
