from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class PromptFrontMatter:
    intent: str
    task_type: str
    mode: str
    domain: str
    style: str
    reasoning_mode: str
    memory_scope: str
    retrieval_profile: str
    output_format: str
    tooling: str
    stakes: str
    uncertainty_policy: str
    privacy_level: str
    confidence: float
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class ResponsePlanFrontMatter:
    selected_backend: str
    selected_mode: str
    include_context: bool
    include_memory_context: bool
    include_rs1_specialty: bool
    include_rs1_creative: bool
    retrieval_profile: str
    memory_top_k: int
    output_shape: str
    confidence: float
    route_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
