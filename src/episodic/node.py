from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class MemoryNode:
    content: str
    keywords: list[str] = field(default_factory=list)

    # Lane scores — 0.0 to 1.0
    emotional: float = 0.5
    circumstantial: float = 0.5
    developmental_phase: float = 0.5  # 0=novice, 1=expert in domain

    # Auto-managed
    id: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)
    reinforce_count: int = 0
    crystallized: bool = False

    # Context tags (free-form)
    mood_tag: str = ""
    context_tag: str = ""  # e.g. "floor_shift", "problem_solving", "creative"
    domain: str = ""       # e.g. "warehouse", "fiction", "code"
