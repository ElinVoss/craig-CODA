from __future__ import annotations

from .runtime_context_translator import build_memory_context
from src.memory.node_schema import VaultNode


def build_sft_records(nodes: list[VaultNode]) -> list[dict]:
    records: list[dict] = []
    for index, node in enumerate(nodes, start=1):
        if node.trust_layer not in {"stable_core", "project_constraints", "episodic_events"}:
            continue
        records.append(
            {
                "id": f"context-sft-{index:04d}",
                "system": "You are a direct local-first assistant.",
                "input": f"Summarize the key guidance from this {node.trust_layer} node.",
                "output": node.summary,
                "tags": [node.trust_layer, node.node_type, "instruction_response"],
                "source_file": node.source_path,
                "source_node_id": node.id,
            }
        )
        records.append(
            {
                "id": f"context-sft-{index:04d}-rewrite",
                "system": "You rewrite content to be more direct without changing the meaning.",
                "input": f"Rewrite this content more clearly:\n\n{node.summary}",
                "output": node.summary,
                "tags": [node.trust_layer, node.node_type, "rewrite_correction"],
                "source_file": node.source_path,
                "source_node_id": node.id,
            }
        )
        records.append(
            {
                "id": f"context-sft-{index:04d}-critique",
                "system": "You critique weak plans by surfacing the concrete constraint first.",
                "input": f"What is the first concrete constraint to surface from this node?\n\n{node.content}",
                "output": node.summary,
                "tags": [node.trust_layer, node.node_type, "critique_first"],
                "source_file": node.source_path,
                "source_node_id": node.id,
            }
        )
        if node.project_relevance >= 0.6:
            records.append(
                {
                    "id": f"context-sft-{index:04d}-transfer",
                    "system": "You transfer a concrete lesson from one domain into another without losing structure.",
                    "input": f"Apply the lesson from this node to a related runtime problem:\n\n{node.summary}",
                    "output": f"Carry over the concrete constraint first: {node.summary}",
                    "tags": [node.trust_layer, node.node_type, "analogical_transfer"],
                    "source_file": node.source_path,
                    "source_node_id": node.id,
                }
            )
    return records
