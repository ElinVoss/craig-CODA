"""Ollama adapter.

Wraps the local Ollama HTTP API. Complements the existing
src/runtime/ollama_client.py streaming helper — this adapter exposes
both a synchronous call() (non-streaming) and a streaming stream()
that delegates to ollama_client.chat().

Backend name format: "ollama:{model_name}", e.g. "ollama:dolphin-llama3".
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any, Generator

from src.adapters.base import BaseAdapter
from src.coda_ir import CodaRequest, CodaResponse

_OLLAMA_BASE = "http://localhost:11434"


class OllamaAdapter(BaseAdapter):
    """Adapter for models served via local Ollama."""

    def __init__(self, model: str = "dolphin-llama3") -> None:
        self._model = model

    @property
    def backend_name(self) -> str:
        return f"ollama:{self._model}"

    @property
    def backend_type(self) -> str:
        return "ollama"

    def format_request(self, request: CodaRequest) -> dict[str, Any]:
        params = {
            "model": self._model,
            "messages": request.messages_for_api(),
            "stream": False,
        }
        if request.generation_params:
            params["options"] = request.generation_params
        return params

    def parse_response(self, raw: dict[str, Any], request: CodaRequest) -> CodaResponse:
        text = raw.get("message", {}).get("content", "")
        usage = {
            "input_tokens": raw.get("prompt_eval_count", 0),
            "output_tokens": raw.get("eval_count", 0),
        }
        return CodaResponse(
            text=text,
            backend_name=self.backend_name,
            request_id=request.request_id,
            vault_profile=request.vault_profile,
            usage=usage,
        )

    def call(self, request: CodaRequest) -> CodaResponse:
        payload = json.dumps(self.format_request(request)).encode()
        req = urllib.request.Request(
            f"{_OLLAMA_BASE}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw: dict[str, Any] = json.loads(resp.read())
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
        """Yield response text chunks via Ollama streaming API."""
        from src.runtime.ollama_client import chat as ollama_chat

        try:
            yield from ollama_chat(
                model=self._model,
                messages=request.messages_for_api(),
                stream=True,
            )
        except Exception as exc:
            yield f"[OllamaAdapter error: {exc}]"

    def health_check(self) -> bool:
        try:
            urllib.request.urlopen(f"{_OLLAMA_BASE}/api/tags", timeout=2)
            return True
        except Exception:
            return False
