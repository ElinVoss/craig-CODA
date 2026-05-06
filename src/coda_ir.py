"""CODA intermediate representation.

CodaRequest and CodaResponse are the normalized data contracts that flow
through the CODA runtime. They sit between CodaRuntime (which assembles
vault + memory context) and BaseAdapter (which translates to each
backend's native wire format).

Design rules:
- The caller (CodaRuntime or equivalent) compiles system_prompt from vault
  directives + episodic memory BEFORE constructing a CodaRequest. Adapters
  never reach back into the vault.
- history contains only "user" and "assistant" roles. system_prompt is the
  only system-layer input and travels as its own field.
- Adapters return CodaResponse on failure (error field set), never raise.
- Stable usage keys: input_tokens, output_tokens.
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class CodaMessage:
    """A single prior turn (user or assistant only — no system roles in history)."""

    role: str   # "user" | "assistant"
    content: str


@dataclass
class CodaRequest:
    """Normalized request flowing from CODA runtime to a backend adapter.

    The caller is responsible for:
    - resolving the vault profile and compiling system_prompt from it
    - injecting retrieved memory_nodes into system_prompt
    - populating vault_directives for provenance

    target_backend uses the canonical format "{type}:{model_name}" for API
    backends (e.g. "ollama:dolphin-llama3", "anthropic:claude-3-haiku-20240307")
    and "local:{backend_name}" for BackendBase wrappers (e.g. "local:tiny-qwen3-scratch").
    """

    message: str
    system_prompt: str = ""
    history: list[CodaMessage] = field(default_factory=list)
    vault_profile: str | None = None
    vault_directives: dict[str, Any] = field(default_factory=dict)
    memory_nodes: list[dict[str, Any]] = field(default_factory=list)
    target_backend: str = "ollama:dolphin-llama3"
    generation_params: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    request_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def messages_for_api(self) -> list[dict[str, str]]:
        """Assemble as an OpenAI-compatible message list.

        Order: system (if set) → prior history turns → current user message.
        Suitable for Ollama, Anthropic, OpenAI, and Groq chat APIs.
        """
        msgs: list[dict[str, str]] = []
        if self.system_prompt:
            msgs.append({"role": "system", "content": self.system_prompt})
        for m in self.history:
            msgs.append({"role": m.role, "content": m.content})
        msgs.append({"role": "user", "content": self.message})
        return msgs

    def prompt_for_completion(self, turn_sep: str = "\n") -> str:
        """Collapse the conversation into a single prompt string.

        Used by backends that only accept a plain text prompt (BackendBase.generate).
        Format: system block (if set) → history turns as Speaker: text → User: message
        """
        parts: list[str] = []
        if self.system_prompt:
            parts.append(f"[System]\n{self.system_prompt}")
        for m in self.history:
            label = "User" if m.role == "user" else "Assistant"
            parts.append(f"{label}: {m.content}")
        parts.append(f"User: {self.message}")
        parts.append("Assistant:")
        return turn_sep.join(parts)


@dataclass
class CodaResponse:
    """Normalized response from any backend adapter.

    error is set (non-None) if generation failed. Callers should check ok
    before using text. Usage keys are stable: input_tokens, output_tokens.
    """

    text: str
    backend_name: str
    request_id: str = ""
    vault_profile: str | None = None
    usage: dict[str, int] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    @property
    def ok(self) -> bool:
        """True if the response completed without error."""
        return self.error is None
