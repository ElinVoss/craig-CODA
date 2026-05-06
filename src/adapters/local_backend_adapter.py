"""Local backend adapter.

Wraps a src/model_backends BackendBase instance (scratch or pretrained
local transformers) behind the CODA adapter contract.

Since BackendBase.generate() takes a plain prompt string and returns a
plain string, this adapter uses CodaRequest.prompt_for_completion() to
collapse conversation history into the format local models expect.
stream() yields the full response in one chunk (local inference is not
incrementally streamed).

Backend name format: "local:{backend_name}",
e.g. "local:tiny-qwen3-scratch".

Lifecycle: the wrapped BackendBase is lazy-loaded on the first call()
to avoid loading weights at import or registry registration time.
"""
from __future__ import annotations

import time
from typing import Any, Generator

from src.adapters.base import BaseAdapter
from src.coda_ir import CodaRequest, CodaResponse


class LocalBackendAdapter(BaseAdapter):
    """Adapter wrapping a src/model_backends BackendBase for local inference."""

    def __init__(self, backend_name_key: str, cfg_path: str | None = None) -> None:
        """
        Args:
            backend_name_key: the backend_name as declared in pretrained_backends.yaml
            cfg_path: optional path override for pretrained_backends.yaml
        """
        self._backend_name_key = backend_name_key
        self._cfg_path = cfg_path
        self._backend = None   # lazy-loaded on first call

    def _get_backend(self):
        if self._backend is None:
            from src.model_backends.load_backend import load_backend
            from pathlib import Path
            cfg = Path(self._cfg_path) if self._cfg_path else None
            self._backend = load_backend(self._backend_name_key, cfg_path=cfg)
            if not self._backend.is_loaded():
                self._backend.load()
        return self._backend

    @property
    def backend_name(self) -> str:
        return f"local:{self._backend_name_key}"

    @property
    def backend_type(self) -> str:
        return "local_scratch"

    def format_request(self, request: CodaRequest) -> str:
        """Collapse the conversation into a single prompt string."""
        return request.prompt_for_completion()

    def parse_response(self, raw: Any, request: CodaRequest) -> CodaResponse:
        text = str(raw)
        return CodaResponse(
            text=text,
            backend_name=self.backend_name,
            request_id=request.request_id,
            vault_profile=request.vault_profile,
            usage={"input_tokens": 0, "output_tokens": 0},
        )

    def call(self, request: CodaRequest) -> CodaResponse:
        try:
            backend = self._get_backend()
            prompt = self.format_request(request)
            t0 = time.monotonic()
            raw = backend.generate(prompt, **request.generation_params)
            elapsed = time.monotonic() - t0
            response = self.parse_response(raw, request)
            response.metadata["elapsed_seconds"] = round(elapsed, 3)
            return response
        except Exception as exc:
            return CodaResponse(
                text="",
                backend_name=self.backend_name,
                request_id=request.request_id,
                vault_profile=request.vault_profile,
                error=str(exc),
            )

    def stream(self, request: CodaRequest) -> Generator[str, None, None]:
        """Local inference is not streamed — yields the full response in one chunk."""
        response = self.call(request)
        if response.text:
            yield response.text

    def health_check(self) -> bool:
        try:
            backend = self._get_backend()
            return backend.is_loaded()
        except Exception:
            return False
