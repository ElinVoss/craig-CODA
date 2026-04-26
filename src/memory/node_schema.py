from __future__ import annotations

from dataclasses import asdict, dataclass, field


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

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict) -> "VaultEdge":
        return cls(**value)
