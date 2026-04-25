"""
Minimal Ollama API client — chat with streaming.
No external dependencies beyond the stdlib.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Generator


BASE_URL = "http://localhost:11434"


def is_running() -> bool:
    try:
        urllib.request.urlopen(f"{BASE_URL}/api/tags", timeout=2)
        return True
    except Exception:
        return False


def chat(
    model: str,
    messages: list[dict],
    stream: bool = True,
) -> Generator[str, None, None]:
    """
    Call Ollama /api/chat. Yields content chunks if streaming.
    Each chunk is a plain string (the delta text).
    """
    payload = json.dumps({"model": model, "messages": messages, "stream": stream}).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/api/chat",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        for raw_line in resp:
            line = raw_line.decode("utf-8").strip()
            if not line:
                continue
            obj = json.loads(line)
            delta = obj.get("message", {}).get("content", "")
            if delta:
                yield delta
            if obj.get("done"):
                break


def list_models() -> list[str]:
    with urllib.request.urlopen(f"{BASE_URL}/api/tags", timeout=5) as resp:
        data = json.loads(resp.read())
    return [m["name"] for m in data.get("models", [])]
