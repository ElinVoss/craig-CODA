"""CODA adapter contract.

BaseAdapter is the abstract base class every backend adapter must implement.
An adapter wraps one model backend (local BackendBase or remote API) and
provides a uniform call() / stream() interface to the CODA runtime.

Lifecycle rule: adapters lazy-load any heavyweight resources (weights,
API clients) on the first call(), not at construction time. The registry
holds one adapter instance per backend_name.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generator

from src.coda_ir import CodaRequest, CodaResponse


class BaseAdapter(ABC):
    """Abstract adapter: normalize CodaRequest → backend → CodaResponse.

    Subclasses must implement backend_name, backend_type, format_request,
    parse_response, call, and health_check.

    stream() has a default implementation that calls call() and yields the
    full text as a single chunk. Adapters with native streaming support
    (Ollama, Anthropic) should override stream() for real chunk delivery.
    """

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Canonical backend identifier.

        Format: "{type}:{model_name}" for API backends, e.g.:
          "ollama:dolphin-llama3"
          "anthropic:claude-3-haiku-20240307"
        Format: "local:{backend_name}" for BackendBase wrappers, e.g.:
          "local:tiny-qwen3-scratch"
        """

    @property
    @abstractmethod
    def backend_type(self) -> str:
        """Transport/provider category.

        One of: "ollama", "anthropic", "openai", "groq", "local_scratch",
        "pretrained_local".
        """

    @abstractmethod
    def format_request(self, request: CodaRequest) -> Any:
        """Translate CodaRequest to the backend's native input format.

        For chat APIs: returns a dict suitable for the provider's messages endpoint.
        For completion-only backends: returns a prompt string.
        """

    @abstractmethod
    def parse_response(self, raw: Any, request: CodaRequest) -> CodaResponse:
        """Translate the backend's native response to CodaResponse.

        Stable usage keys: input_tokens, output_tokens.
        On error: set error=str(exc), text="". Do not raise.
        """

    @abstractmethod
    def call(self, request: CodaRequest) -> CodaResponse:
        """Execute one full request-response round-trip synchronously.

        Returns CodaResponse. Sets error field on failure; never raises.
        """

    def stream(self, request: CodaRequest) -> Generator[str, None, None]:
        """Yield response text as chunks. Default: one chunk from call().

        Adapters with native streaming (Ollama, Anthropic) should override
        this method to yield real incremental chunks.
        """
        response = self.call(request)
        if response.text:
            yield response.text

    @abstractmethod
    def health_check(self) -> bool:
        """Return True if the backend is reachable and ready for calls."""
