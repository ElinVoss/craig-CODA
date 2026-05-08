"""LM Studio adapter.

Wraps the LM Studio OpenAI-compatible HTTP API running on the server GPU
(default: http://192.168.4.25:1234/v1).

This adapter is the primary remote-inference path for Craig-CODA.
It probes the server before every call and returns an offline-safe error
response when the server is unreachable — the client never crashes on
a missing cable.

Backend name format: "lmstudio:{model_name}", e.g. "lmstudio:qwen2.5-7b-instruct".
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any, Generator

from src.adapters.base import BaseAdapter
from src.coda_ir import CodaRequest, CodaResponse

_DEFAULT_BASE = os.environ.get("LMSTUDIO_SERVER", "http://192.168.4.25:1234")
_PROBE_TIMEOUT = 2   # seconds — fast fail so offline mode kicks in quickly
_CALL_TIMEOUT  = 120


class LMStudioAdapter(BaseAdapter):
    """Adapter for models served via LM Studio's OpenAI-compatible API."""

    def __init__(
        self,
        model: str = "qwen2.5-7b-instruct",
        base_url: str | None = None,
        api_key: str = "lm-studio",
    ) -> None:
        self._model    = model
        self._base_url = (base_url or _DEFAULT_BASE).rstrip("/")
        self._api_key  = api_key

    @property
    def backend_name(self) -> str:
        return f"lmstudio:{self._model}"

    @property
    def backend_type(self) -> str:
        return "lmstudio"

    def _headers(self) -> dict[str, str]:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self._api_key}",
        }

    def format_request(self, request: CodaRequest) -> dict[str, Any]:
        params: dict[str, Any] = {
            "model": self._model,
            "messages": request.messages_for_api(),
            "stream": False,
        }
        if request.generation_params:
            gp = request.generation_params
            if "temperature"        in gp: params["temperature"]         = gp["temperature"]
            if "top_p"              in gp: params["top_p"]               = gp["top_p"]
            if "max_new_tokens"     in gp: params["max_tokens"]          = gp["max_new_tokens"]
            if "repetition_penalty" in gp: params["frequency_penalty"]   = gp["repetition_penalty"] - 1.0
        return params

    def parse_response(self, raw: dict[str, Any], request: CodaRequest) -> CodaResponse:
        text  = raw.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = raw.get("usage", {})
        return CodaResponse(
            text=text,
            backend_name=self.backend_name,
            request_id=request.request_id,
            vault_profile=request.vault_profile,
            usage={
                "input_tokens":  usage.get("prompt_tokens", 0),
                "output_tokens": usage.get("completion_tokens", 0),
            },
        )

    def call(self, request: CodaRequest) -> CodaResponse:
        if not self.health_check():
            return CodaResponse(
                text="",
                backend_name=self.backend_name,
                request_id=request.request_id,
                vault_profile=request.vault_profile,
                error="LM Studio server unreachable — running in offline mode",
            )

        payload = json.dumps(self.format_request(request)).encode()
        req = urllib.request.Request(
            f"{self._base_url}/v1/chat/completions",
            data=payload,
            headers=self._headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=_CALL_TIMEOUT) as resp:
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
        """Yield response chunks via LM Studio streaming (SSE)."""
        if not self.health_check():
            yield "[LMStudioAdapter: server unreachable — offline mode active]"
            return

        payload = json.dumps({**self.format_request(request), "stream": True}).encode()
        req = urllib.request.Request(
            f"{self._base_url}/v1/chat/completions",
            data=payload,
            headers=self._headers(),
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=_CALL_TIMEOUT) as resp:
                for raw_line in resp:
                    line = raw_line.decode("utf-8").strip()
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data)
                        delta = chunk["choices"][0]["delta"].get("content", "")
                        if delta:
                            yield delta
                    except (json.JSONDecodeError, KeyError, IndexError):
                        continue
        except Exception as exc:
            yield f"[LMStudioAdapter stream error: {exc}]"

    def health_check(self) -> bool:
        """Probe /v1/models — fast, non-destructive."""
        try:
            req = urllib.request.Request(
                f"{self._base_url}/v1/models",
                headers=self._headers(),
                method="GET",
            )
            urllib.request.urlopen(req, timeout=_PROBE_TIMEOUT)
            return True
        except Exception:
            return False
