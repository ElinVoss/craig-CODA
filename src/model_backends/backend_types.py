from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


class BackendBase(ABC):
    """Abstract base class for all model backends.

    Concrete backends must implement load(), generate(), is_loaded(),
    and backend_name(). The scratch and pretrained_transformers backends
    both inherit from this class, keeping the generation interface uniform
    while allowing completely different underlying implementations.
    """

    @abstractmethod
    def load(self) -> None:
        """Load model weights and tokenizer into memory."""

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text from prompt. Returns generated text only (no prompt echo)."""

    @abstractmethod
    def is_loaded(self) -> bool:
        """Return True if the model has been loaded and is ready for generation."""

    @abstractmethod
    def backend_name(self) -> str:
        """Return the backend's name as registered in pretrained_backends.yaml."""


@dataclass
class BackendConfig:
    """All configuration fields corresponding to one entry in pretrained_backends.yaml."""

    backend_name: str
    enabled: bool
    backend_type: str
    model_family: str
    model_id_or_local_path: str
    tokenizer_path: str | None = None
    quant_format: str | None = None
    device_preference: str = "cpu"
    dtype_preference: str = "float32"
    max_context_length: int | None = None
    generation_defaults: dict[str, Any] = field(default_factory=dict)
    role: str = "research"
    notes: str = ""

    @classmethod
    def from_dict(cls, data: dict) -> "BackendConfig":
        """Construct a BackendConfig from a raw dict (e.g. parsed from YAML)."""
        return cls(
            backend_name=data["backend_name"],
            enabled=bool(data.get("enabled", False)),
            backend_type=data["backend_type"],
            model_family=data.get("model_family", "unknown"),
            model_id_or_local_path=str(data["model_id_or_local_path"]),
            tokenizer_path=data.get("tokenizer_path") or None,
            quant_format=data.get("quant_format") or None,
            device_preference=str(data.get("device_preference", "cpu")),
            dtype_preference=str(data.get("dtype_preference", "float32")),
            max_context_length=int(data["max_context_length"]) if data.get("max_context_length") else None,
            generation_defaults=dict(data.get("generation_defaults") or {}),
            role=str(data.get("role", "research")),
            notes=str(data.get("notes", "")),
        )


@dataclass
class GenerationResult:
    """Result from a single backend generation call."""

    text: str
    backend_name: str
    prompt_length: int
    tokens_generated: int
    elapsed_seconds: float
    metadata: dict[str, Any] = field(default_factory=dict)
