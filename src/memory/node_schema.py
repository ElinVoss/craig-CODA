from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass
class NodeProvenance:
    """Tracks the origin of a node extracted from a model artifact."""
    model_name: str
    model_path: str
    layer_index: Optional[int] = None
    head_index: Optional[int] = None
    tensor_name: Optional[str] = None
    activation_pattern: Optional[str] = None
    capability_label: Optional[str] = None
    mining_timestamp: Optional[str] = None
    mining_method: str = "manual"  # manual | gguf_tensor | activation_analysis
    # Extended extraction metadata
    model_file: str = ""                       # GGUF filename (no path)
    component_type: str = ""                   # attention_block | ffn_block | token_embedding | output_projection
    extraction_method: str = "structural_heuristic"  # structural_heuristic | activation_analysis | manual
    extraction_confidence: float = 0.5         # 0.0-1.0; structural_heuristic ≈ 0.4, activation_analysis ≈ 0.85
    polysemantic: bool = False                 # True if head/unit is known to serve multiple task types

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict) -> "NodeProvenance":
        return cls(**value)


@dataclass
class VaultNode:
    id: str
    node_type: str
    trust_layer: str
    content: str
    summary: str
    source_path: str
    source_kind: str
    created_at: str
    time_start: str | None
    time_end: str | None
    life_phase: str
    people: list[str] = field(default_factory=list)
    projects: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    links: list[str] = field(default_factory=list)
    confidence: float = 0.75
    privacy_level: str = "standard"
    reinforcement_count: int = 0
    voice_score: float = 0.5
    reasoning_score: float = 0.5
    prose_score: float = 0.5
    project_relevance: float = 0.5
    extracted_from: Optional[dict] = None  # serialized NodeProvenance, None for human-authored nodes

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict) -> "VaultNode":
        return cls(**value)


@dataclass
class VaultEdge:
    source_id: str
    target_id: str
    edge_type: str
    weight: float
    rationale: str
    propagation_eligible: bool = True

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict) -> "VaultEdge":
        return cls(**value)
