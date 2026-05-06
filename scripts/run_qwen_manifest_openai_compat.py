from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "exports" / "user_model_package" / "method_vault" / "vaultization" / "qwen2_5_omni_7b" / "specimens" / "prompt_set.json"
DEFAULT_OUTPUT = ROOT / "exports" / "user_model_package" / "method_vault" / "vaultization" / "qwen2_5_omni_7b" / "specimens" / "raw_responses.json"


def _normalize_base_url(base_url: str) -> str:
    value = base_url.rstrip("/")
    if not value.endswith("/v1"):
        value = f"{value}/v1"
    return value


def _request_json(url: str, payload: dict[str, Any] | None, api_key: str, timeout: int) -> dict[str, Any]:
    data = None
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = Request(url, data=data, headers=headers, method="POST" if payload is not None else "GET")
    try:
        with urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {body}") from exc
    except URLError as exc:
        raise RuntimeError(f"Could not reach {url}: {exc.reason}") from exc


def _list_models(base_url: str, api_key: str, timeout: int) -> list[str]:
    payload = _request_json(f"{base_url}/models", None, api_key, timeout)
    data = payload.get("data", [])
    return [str(item.get("id")) for item in data if item.get("id")]


def _resolve_model(explicit_model: str | None, base_url: str, api_key: str, timeout: int) -> str:
    if explicit_model:
        return explicit_model
    model_ids = _list_models(base_url, api_key, timeout)
    if len(model_ids) == 1:
        return model_ids[0]
    if not model_ids:
        raise RuntimeError("No models were returned by the local server. Load the Qwen donor in LM Studio first.")
    raise RuntimeError(
        "Multiple models are available on the local server. Re-run with --model and pick one of:\n"
        + "\n".join(model_ids)
    )


def _extract_text(choice: dict[str, Any]) -> str:
    message = choice.get("message") or {}
    content = message.get("content", "")
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        return "".join(parts)
    return str(content)


def run_manifest(
    base_url: str,
    model: str,
    api_key: str,
    input_path: Path,
    output_path: Path,
    timeout: int,
    temperature: float,
    max_tokens: int,
) -> None:
    prompts = json.loads(input_path.read_text(encoding="utf-8"))
    if not isinstance(prompts, list):
        raise RuntimeError(f"Prompt manifest must be a list: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []

    for item in prompts:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": str(item["prompt"])}],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        started = time.time()
        provider_response = _request_json(f"{base_url}/chat/completions", payload, api_key, timeout)
        choice = (provider_response.get("choices") or [{}])[0]
        results.append(
            {
                "specimen_id": item.get("specimen_id"),
                "input_type": item.get("input_type"),
                "prompt_summary": item.get("prompt_summary"),
                "prompt": item.get("prompt"),
                "model": model,
                "provider": "openai_compatible_local",
                "base_url": base_url,
                "elapsed_seconds": round(time.time() - started, 3),
                "created_at": provider_response.get("created"),
                "response": _extract_text(choice),
                "finish_reason": choice.get("finish_reason"),
                "usage": provider_response.get("usage"),
            }
        )
        print(f"[{len(results)}/{len(prompts)}] {item.get('specimen_id')}")

    output_path.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nWrote {len(results)} specimens to {output_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the Qwen2.5-Omni prompt manifest against an OpenAI-compatible local server."
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:1234/v1")
    parser.add_argument("--model", default=None)
    parser.add_argument("--api-key", default="lm-studio")
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT))
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=220)
    parser.add_argument("--list-models", action="store_true")
    args = parser.parse_args()

    base_url = _normalize_base_url(args.base_url)

    if args.list_models:
        model_ids = _list_models(base_url, args.api_key, args.timeout)
        if not model_ids:
            print("No models returned.")
            return 1
        for model_id in model_ids:
            print(model_id)
        return 0

    model = _resolve_model(args.model, base_url, args.api_key, args.timeout)
    run_manifest(
        base_url=base_url,
        model=model,
        api_key=args.api_key,
        input_path=Path(args.input),
        output_path=Path(args.output),
        timeout=args.timeout,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
