from __future__ import annotations

import time

from .backend_types import BackendBase, GenerationResult


def run_generation(
    backend: BackendBase,
    prompt: str,
    **overrides,
) -> GenerationResult:
    """Run a single generation call through a loaded backend.

    Times the call and returns a GenerationResult. The backend must already
    be loaded (backend.is_loaded() == True) before calling this function.
    """
    if not backend.is_loaded():
        raise RuntimeError(
            f"Backend '{backend.backend_name()}' is not loaded. "
            "Call backend.load() before run_generation()."
        )

    prompt_length = len(prompt)
    start = time.monotonic()
    text = backend.generate(prompt, **overrides)
    elapsed = time.monotonic() - start

    return GenerationResult(
        text=text,
        backend_name=backend.backend_name(),
        prompt_length=prompt_length,
        tokens_generated=len(text.split()),  # word-count approximation
        elapsed_seconds=round(elapsed, 3),
        metadata={"overrides": overrides},
    )


def run_comparison(
    backends: list[BackendBase],
    prompt: str,
    **overrides,
) -> list[GenerationResult]:
    """Run the same prompt through each backend and return all results.

    Each backend must already be loaded before calling this function.
    Results are returned in the same order as the backends list.
    """
    results: list[GenerationResult] = []
    for backend in backends:
        result = run_generation(backend, prompt, **overrides)
        results.append(result)
    return results
