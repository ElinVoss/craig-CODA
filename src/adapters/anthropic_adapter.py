"""Anthropic adapter.

Wraps the Anthropic messages API. Requires the ANTHROPIC_API_KEY
environment variable. The anthropic package is already in requirements.txt.

Backend name format: "anthropic:{model_name}",
e.g. "anthropic:claude-3-haiku-20240307".
"""
from __future__ import annotations

from typing import Any, Generator

from src.adapters.base import BaseAdapter
from src.coda_ir import CodaRequest, CodaResponse

_DEFAULT_MAX_TOKENS = 1024


class AnthropicAdapter(BaseAdapter):
    """Adapter for Anthropic API models (Claude family)."""

    def __init__(self, model: str = "claude-3-haiku-20240307") -> None:
        self._model = model
        self._client = None   # lazy-loaded on first call

    def _get_client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic()
        return self._client

    @property
    def backend_name(self) -> str:
        return f"anthropic:{self._model}"

    @property
    def backend_type(self) -> str:
        return "anthropic"

    def format_request(self, request: CodaRequest) -> dict[str, Any]:
        """Anthropic requires system content as a separate top-level field."""
        messages = []
        for m in request.history:
            messages.append({"role": m.role, "content": m.content})
        messages.append({"role": "user", "content": request.message})

        params: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "max_tokens": request.generation_params.get("max_tokens", _DEFAULT_MAX_TOKENS),
        }
        if request.system_prompt:
            params["system"] = request.system_prompt
        if "temperature" in request.generation_params:
            params["temperature"] = request.generation_params["temperature"]
        return params

    def parse_response(self, raw: Any, request: CodaRequest) -> CodaResponse:
        text = raw.content[0].text if raw.content else ""
        usage = {
            "input_tokens": getattr(raw.usage, "input_tokens", 0),
            "output_tokens": getattr(raw.usage, "output_tokens", 0),
        }
        return CodaResponse(
            text=text,
            backend_name=self.backend_name,
            request_id=request.request_id,
            vault_profile=request.vault_profile,
            usage=usage,
        )

    def call(self, request: CodaRequest) -> CodaResponse:
        try:
            client = self._get_client()
            params = self.format_request(request)
            raw = client.messages.create(**params)
            return self.parse_response(raw, request)
        except Exception as exc:
            return CodaResponse(
                text="",
                backend_name=self.backend_name,
                request_id=request.request_id,
                vault_profile=request.vault_profile,
                error=str(exc),
            )

    def stream(self, request: CodaRequest) -> Generator[str, None, None]:
        """Yield response chunks via Anthropic streaming API."""
        try:
            client = self._get_client()
            params = self.format_request(request)
            with client.messages.stream(**params) as stream_ctx:
                yield from stream_ctx.text_stream
        except Exception as exc:
            yield f"[AnthropicAdapter error: {exc}]"

    def health_check(self) -> bool:
        try:
            self._get_client()
            return True
        except Exception:
            return False
