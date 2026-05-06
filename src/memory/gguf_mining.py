from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .node_schema import ExtractionProvenance, VaultNode

MINER_VERSION = "0.1.0"

try:
    from gguf import GGUFReader  # type: ignore
except ImportError:  # pragma: no cover - dependency is optional until mining is used
    GGUFReader = None

LAYER_PATTERN = re.compile(r"(?:blk|layer|layers)[._](\d+)")
HEAD_PATTERN = re.compile(r"(?:head|heads)[._](\d+)")
ROLE_HINTS = {
    "attn": ("reasoning_attention", "attention pathway tensor"),
    "mlp": ("feature_transform", "mlp transformation tensor"),
    "ffn": ("feature_transform", "feed-forward pathway tensor"),
    "embed": ("token_interface", "token embedding tensor"),
    "output": ("decoder_interface", "output projection tensor"),
    "norm": ("stability_control", "normalization tensor"),
}


@dataclass
class TensorDescriptor:
    name: str
    shape: list[int]
    n_elements: int | None
    dtype: str | None


def _ensure_reader() -> None:
    if GGUFReader is None:
        raise RuntimeError(
            "GGUF mining requires the `gguf` package. Install it locally (for example: `pip install gguf`)."
        )


def _to_list_shape(shape: Any) -> list[int]:
    if shape is None:
        return []
    if isinstance(shape, (list, tuple)):
        return [int(x) for x in shape]
    return [int(shape)]


def _extract_descriptor(tensor: Any) -> TensorDescriptor:
    name = str(getattr(tensor, "name", "unknown_tensor"))
    shape = _to_list_shape(getattr(tensor, "shape", []))
    n_elements = getattr(tensor, "n_elements", None)
    if n_elements is None and shape:
        total = 1
        for dim in shape:
            total *= dim
        n_elements = total
    dtype = getattr(tensor, "tensor_type", None)
    return TensorDescriptor(
        name=name,
        shape=shape,
        n_elements=int(n_elements) if n_elements is not None else None,
        dtype=str(dtype) if dtype is not None else None,
    )


def _layer_head_indexes(tensor_name: str) -> tuple[int | None, int | None]:
    layer_match = LAYER_PATTERN.search(tensor_name)
    head_match = HEAD_PATTERN.search(tensor_name)
    layer_index = int(layer_match.group(1)) if layer_match else None
    head_index = int(head_match.group(1)) if head_match else None
    return layer_index, head_index


def _infer_capability(tensor_name: str) -> tuple[str, str]:
    lowered = tensor_name.lower()
    for marker, value in ROLE_HINTS.items():
        if marker in lowered:
            return value
    return "latent_feature", "unclassified tensor feature"


def _node_id(model_name: str, tensor_name: str) -> str:
    raw = f"gguf::{model_name}::{tensor_name}"
    return hashlib.sha1(raw.encode("utf-8")).hexdigest()[:16]


def _summary(capability_kind: str, tensor_name: str, shape: list[int], dtype: str | None) -> str:
    shape_text = "x".join(str(item) for item in shape) if shape else "unknown-shape"
    dtype_text = dtype or "unknown-dtype"
    return f"{capability_kind} seed from {tensor_name} ({shape_text}, {dtype_text})"


def _component_type(tensor_name: str) -> str:
    lowered = tensor_name.lower()
    if "attn" in lowered or "self_attn" in lowered:
        return "attention_head"
    if "mlp" in lowered or "ffn" in lowered:
        return "mlp_neuron"
    if "embed" in lowered or "embd" in lowered:
        return "residual_stream"
    return "unknown"


def _build_capability_node(model_path: Path, descriptor: TensorDescriptor, mined_at: str) -> VaultNode:
    capability_kind, capability_note = _infer_capability(descriptor.name)
    layer_index, head_index = _layer_head_indexes(descriptor.name)
    model_name = model_path.stem
    # Heuristic extraction: confidence is moderate; polysemantic is unknown at this stage.
    # Activation probing (future work) will update these fields with real values.
    provenance = ExtractionProvenance(
        model_name=model_name,
        model_file=model_path.name,
        tensor_name=descriptor.name,
        layer_index=layer_index,
        head_index=head_index,
        component_type=_component_type(descriptor.name),
        activation_pattern=f"heuristic:{capability_kind}",
        extraction_method="heuristic",
        extraction_confidence=0.4,  # heuristic name-matching only; probing will raise this
        polysemantic=True,           # assume polysemantic until probing proves otherwise
        polysemantic_roles=None,     # unknown until activation probing is complete
        mined_at=mined_at,
        miner_version=MINER_VERSION,
    )
    content = (
        f"Capability seed mined from GGUF tensor.\n"
        f"model={model_name}\n"
        f"tensor={descriptor.name}\n"
        f"shape={descriptor.shape}\n"
        f"dtype={descriptor.dtype}\n"
        f"n_elements={descriptor.n_elements}\n"
        f"capability_kind={capability_kind}\n"
        f"note={capability_note}\n"
        "This node is a structural seed and should be validated before promotion into stable runtime layers."
    )
    return VaultNode(
        id=_node_id(model_name, descriptor.name),
        node_type="capability_seed",
        trust_layer="interpretive_maps",
        content=content,
        summary=_summary(capability_kind, descriptor.name, descriptor.shape, descriptor.dtype),
        source_path=str(model_path),
        source_kind="gguf_mining",
        created_at=mined_at,
        time_start=None,
        time_end=None,
        life_phase="current",
        people=[],
        projects=["craig"],
        tags=["gguf", "capability_seed", capability_kind, model_name],
        links=[descriptor.name],
        confidence=0.55,
        privacy_level="internal",
        reinforcement_count=0,
        voice_score=0.2,
        reasoning_score=0.7 if capability_kind == "reasoning_attention" else 0.45,
        prose_score=0.2,
        project_relevance=0.9,
        extracted_from=provenance,
    )


def mine_capability_nodes(model_path: str | Path, limit: int = 256, name_contains: str | None = None) -> list[VaultNode]:
    _ensure_reader()
    path = Path(model_path)
    if not path.is_file():
        raise FileNotFoundError(f"GGUF file not found: {path}")
    reader = GGUFReader(str(path))
    contains = name_contains.lower() if name_contains else None
    mined_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    nodes: list[VaultNode] = []
    for tensor in getattr(reader, "tensors", []):
        descriptor = _extract_descriptor(tensor)
        if contains and contains not in descriptor.name.lower():
            continue
        nodes.append(_build_capability_node(path, descriptor, mined_at))
        if len(nodes) >= limit:
            break
    return nodes
