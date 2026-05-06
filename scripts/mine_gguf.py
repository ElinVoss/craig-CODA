"""
GGUF Mining Pipeline — Gap 1

Reads tensor metadata from a GGUF model file, groups tensors by block and
component type, applies layer-position heuristics to assign capability labels,
and writes VaultNode records (with full NodeProvenance) to a JSONL file.

Extraction method: structural_heuristic (does not require running the model).
Activation-based labeling (extraction_method: activation_analysis) would require
running inference — that is a future upgrade once a backend is available.

Usage:
    python scripts/mine_gguf.py --gguf D:\\gguf-models\\Qwen3-4B-Instruct-2507-Q4_K_M.gguf
    python scripts/mine_gguf.py --gguf D:\\gguf-models\\Qwen3-14B-Q4_K_M.gguf --dry-run

Output:
    artifacts/vault/mined_nodes/<model_basename>.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from gguf import GGUFReader

from src.memory.node_schema import NodeProvenance, VaultNode

# ---------------------------------------------------------------------------
# Layer-position heuristics (based on transformer interpretability literature)
# ---------------------------------------------------------------------------

# (layer_fraction_start, layer_fraction_end, attn_label, ffn_label)
_LAYER_BANDS: list[tuple[float, float, str, str]] = [
    (0.00, 0.33, "syntactic_context_integration",    "surface_pattern_storage"),
    (0.33, 0.67, "semantic_composition_attention",   "world_knowledge_retrieval"),
    (0.67, 1.00, "instruction_following_attention",  "task_reasoning_fact_access"),
]

_COMPONENT_TAGS = {
    "attention_block": ["#extracted_capability", "#attention", "#transformer"],
    "ffn_block":       ["#extracted_capability", "#ffn", "#transformer"],
    "token_embedding": ["#extracted_capability", "#embedding", "#transformer"],
    "output_projection": ["#extracted_capability", "#output", "#transformer"],
}


def _capability_label(layer_idx: int, total_layers: int, component: str) -> str:
    frac = layer_idx / max(total_layers - 1, 1)
    for lo, hi, attn_label, ffn_label in _LAYER_BANDS:
        if lo <= frac < hi or (hi == 1.00 and frac >= lo):
            return attn_label if component == "attention_block" else ffn_label
    return "unknown"


def _node_id(model_name: str, layer: int, component: str) -> str:
    raw = f"{model_name}::blk{layer}::{component}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def _read_model_meta(fields: dict) -> dict:
    def _str_field(key: str) -> str:
        if key not in fields:
            return ""
        raw = fields[key].parts[-1].tolist()
        if isinstance(raw, list):
            try:
                return bytes(raw).decode("utf-8", errors="replace")
            except Exception:
                return str(raw)
        return str(raw)

    def _int_field(key: str) -> int:
        if key not in fields:
            return 0
        val = fields[key].parts[-1].tolist()
        return int(val[0]) if isinstance(val, list) else int(val)

    arch = _str_field("general.architecture")
    return {
        "name":        _str_field("general.name") or _str_field("general.basename"),
        "architecture": arch,
        "block_count": _int_field(f"{arch}.block_count"),
        "head_count":  _int_field(f"{arch}.attention.head_count"),
        "head_count_kv": _int_field(f"{arch}.attention.head_count_kv"),
        "embed_length": _int_field(f"{arch}.embedding_length"),
        "ffn_length":  _int_field(f"{arch}.feed_forward_length"),
    }


def _group_tensors(tensors) -> dict[str, dict]:
    """Group tensor names by block index and component type."""
    blocks: dict[int, dict[str, list[str]]] = {}
    global_tensors: dict[str, list[str]] = {"token_embedding": [], "output_projection": []}

    for t in tensors:
        name = t.name
        if name.startswith("blk."):
            parts = name.split(".")
            layer = int(parts[1])
            rest = ".".join(parts[2:])
            if layer not in blocks:
                blocks[layer] = {"attention_block": [], "ffn_block": []}
            if rest.startswith("attn"):
                blocks[layer]["attention_block"].append(name)
            elif rest.startswith("ffn"):
                blocks[layer]["ffn_block"].append(name)
        elif "token_embd" in name or "embed_tokens" in name:
            global_tensors["token_embedding"].append(name)
        elif "output" in name:
            global_tensors["output_projection"].append(name)

    return {"blocks": blocks, "global": global_tensors}


def mine(gguf_path: Path, dry_run: bool = False) -> list[VaultNode]:
    reader = GGUFReader(str(gguf_path))
    fields = dict(reader.fields)
    meta = _read_model_meta(fields)
    grouped = _group_tensors(reader.tensors)

    total_layers = meta["block_count"] or max(grouped["blocks"].keys(), default=0) + 1
    model_name = meta["name"] or gguf_path.stem
    model_file = gguf_path.name
    timestamp = datetime.now(timezone.utc).isoformat()

    nodes: list[VaultNode] = []

    # --- Per-block nodes ---
    for layer_idx in sorted(grouped["blocks"].keys()):
        for component, tensor_names in grouped["blocks"][layer_idx].items():
            label = _capability_label(layer_idx, total_layers, component)
            frac = layer_idx / max(total_layers - 1, 1)
            band = "early" if frac < 0.33 else ("mid" if frac < 0.67 else "late")

            provenance = NodeProvenance(
                model_name=model_name,
                model_path=str(gguf_path),
                layer_index=layer_idx,
                head_index=None,
                tensor_name="; ".join(sorted(tensor_names)),
                activation_pattern=f"{band}_layer_{component}",
                capability_label=label,
                mining_timestamp=timestamp,
                mining_method="gguf_tensor",
                model_file=model_file,
                component_type=component,
                extraction_method="structural_heuristic",
                extraction_confidence=0.40,
                polysemantic=False,
            )

            shape_desc = f"{len(tensor_names)} tensors"
            content = (
                f"Model: {model_name}\n"
                f"Layer: {layer_idx}/{total_layers - 1} ({band})\n"
                f"Component: {component}\n"
                f"Capability: {label}\n"
                f"Tensors: {', '.join(sorted(tensor_names))}\n"
                f"Extraction: structural_heuristic (confidence=0.40)\n"
                f"Note: Activate with activation_analysis for verified labeling."
            )

            node = VaultNode(
                id=_node_id(model_name, layer_idx, component),
                node_type="extracted_capability",
                trust_layer="project_constraints",
                content=content,
                summary=f"{model_name} blk{layer_idx} {component}: {label}",
                source_path=str(gguf_path),
                source_kind="gguf_extraction",
                created_at=timestamp,
                time_start=None,
                time_end=None,
                life_phase="current",
                tags=_COMPONENT_TAGS.get(component, ["#extracted_capability"]) + [f"#layer_{band}"],
                confidence=0.40,
                privacy_level="internal",
                reasoning_score=0.60,
                extracted_from=provenance.to_dict(),
            )
            nodes.append(node)

    # --- Global nodes (embedding, output) ---
    for component, tensor_names in grouped["global"].items():
        if not tensor_names:
            continue
        provenance = NodeProvenance(
            model_name=model_name,
            model_path=str(gguf_path),
            layer_index=None,
            tensor_name="; ".join(sorted(tensor_names)),
            capability_label=component,
            mining_timestamp=timestamp,
            mining_method="gguf_tensor",
            model_file=model_file,
            component_type=component,
            extraction_method="structural_heuristic",
            extraction_confidence=0.50,
            polysemantic=False,
        )
        label_map = {
            "token_embedding": "vocabulary_token_encoding",
            "output_projection": "vocabulary_output_decoding",
        }
        content = (
            f"Model: {model_name}\n"
            f"Component: {component}\n"
            f"Capability: {label_map.get(component, component)}\n"
            f"Tensors: {', '.join(sorted(tensor_names))}\n"
            f"Extraction: structural_heuristic (confidence=0.50)"
        )
        node = VaultNode(
            id=_node_id(model_name, -1 if component == "token_embedding" else -2, component),
            node_type="extracted_capability",
            trust_layer="project_constraints",
            content=content,
            summary=f"{model_name} {component}: {label_map.get(component, component)}",
            source_path=str(gguf_path),
            source_kind="gguf_extraction",
            created_at=timestamp,
            time_start=None,
            time_end=None,
            life_phase="current",
            tags=_COMPONENT_TAGS.get(component, ["#extracted_capability"]),
            confidence=0.50,
            privacy_level="internal",
            reasoning_score=0.55,
            extracted_from=provenance.to_dict(),
        )
        nodes.append(node)

    return nodes


def main() -> None:
    p = argparse.ArgumentParser(description="Mine VaultNode records from a GGUF file.")
    p.add_argument("--gguf", required=True, help="Path to GGUF model file")
    p.add_argument("--out-dir", default="artifacts/vault/mined_nodes",
                   help="Output directory for JSONL (default: artifacts/vault/mined_nodes)")
    p.add_argument("--dry-run", action="store_true",
                   help="Print node count and first node; do not write output")
    args = p.parse_args()

    gguf_path = Path(args.gguf).resolve()
    if not gguf_path.exists():
        print(f"ERROR: GGUF file not found: {gguf_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Mining: {gguf_path.name}")
    nodes = mine(gguf_path)
    print(f"Generated {len(nodes)} nodes")

    if args.dry_run:
        print("\n--- First node ---")
        print(json.dumps(nodes[0].to_dict(), indent=2))
        return

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{gguf_path.stem}.jsonl"
    with out_file.open("w", encoding="utf-8") as f:
        for node in nodes:
            f.write(json.dumps(node.to_dict()) + "\n")

    print(f"Written: {out_file}")
    print(f"  Block nodes: {sum(1 for n in nodes if n.node_type == 'extracted_capability' and n.extracted_from and n.extracted_from.get('layer_index') is not None)}")
    print(f"  Global nodes: {sum(1 for n in nodes if n.extracted_from and n.extracted_from.get('layer_index') is None)}")


if __name__ == "__main__":
    main()
