from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "conversation_exports" / "markdown_export_raw"
CLEAN_THREADS_DIR = ROOT / "data" / "clean" / "conversation_exports" / "markdown_export_raw" / "threads"
SFT_DIR = ROOT / "data" / "sft" / "conversation_exports" / "markdown_export_raw"
PRETRAIN_DIR = ROOT / "data" / "pretrain" / "conversation_exports" / "markdown_export_raw"

TITLE_RE = re.compile(r"^- title_source: (.*)$", re.MULTILINE)
CONV_ID_RE = re.compile(r"^- conversation_id: (.*)$", re.MULTILINE)


def load_conversation(path: Path) -> tuple[dict[str, Any], str, str]:
    text = path.read_text(encoding="utf-8")
    fence_start = text.find("```json")
    if fence_start == -1:
        raise ValueError(f"No JSON block found in {path}")
    json_start = text.find("\n", fence_start)
    fence_end = text.rfind("\n```")
    if json_start == -1 or fence_end == -1 or fence_end <= json_start:
        raise ValueError(f"Malformed JSON fence in {path}")
    payload = json.loads(text[json_start:fence_end].strip())
    title = (TITLE_RE.search(text).group(1).strip() if TITLE_RE.search(text) else "")
    conv_id = (CONV_ID_RE.search(text).group(1).strip() if CONV_ID_RE.search(text) else payload.get("conversation_id", ""))
    return payload, conv_id, title


def _stringify_part(part: Any) -> str:
    if isinstance(part, str):
        return part
    return json.dumps(part, ensure_ascii=False)


def extract_messages(payload: dict[str, Any]) -> list[dict[str, Any]]:
    mapping = payload.get("mapping", {}) or {}
    messages: list[dict[str, Any]] = []

    for node in mapping.values():
        message = (node or {}).get("message") or {}
        author = (message.get("author") or {}).get("role") or "unknown"
        content = message.get("content") or {}
        parts = content.get("parts")
        text = ""

        if isinstance(parts, list) and parts:
            rendered = [_stringify_part(part).strip() for part in parts if _stringify_part(part).strip()]
            text = "\n\n".join(rendered).strip()
        elif isinstance(content.get("text"), str) and content.get("text", "").strip():
            text = content["text"].strip()

        if not text:
            continue

        messages.append(
            {
                "id": message.get("id") or node.get("id"),
                "role": author,
                "create_time": message.get("create_time") or 0,
                "text": text,
            }
        )

    messages.sort(key=lambda item: (float(item.get("create_time") or 0), str(item.get("id") or "")))
    return messages


def render_thread(conv_id: str, title: str, messages: list[dict[str, Any]]) -> str:
    lines = [
        f"CONVERSATION_ID: {conv_id}",
        f"TITLE: {title}",
        f"MESSAGE_COUNT: {len(messages)}",
        "",
    ]
    for msg in messages:
        role = str(msg["role"]).upper()
        lines.append(f"[{role}]")
        lines.append(msg["text"].strip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_reply_pairs(conv_id: str, title: str, source_file: str, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    pairs: list[dict[str, Any]] = []
    for index in range(1, len(messages)):
        prev = messages[index - 1]
        curr = messages[index]
        if prev["role"] == "user" and curr["role"] == "assistant":
            pairs.append(
                {
                    "id": f"{conv_id}-turn-{index:04d}",
                    "conversation_id": conv_id,
                    "title": title,
                    "turn_index": index,
                    "system": "Continue the conversation naturally from the preceding user turn while preserving continuity and tone.",
                    "input": prev["text"],
                    "output": curr["text"],
                    "source": "markdown_export_raw",
                    "source_file": source_file,
                }
            )
    return pairs


def normalize_corpus() -> dict[str, int]:
    CLEAN_THREADS_DIR.mkdir(parents=True, exist_ok=True)
    SFT_DIR.mkdir(parents=True, exist_ok=True)
    PRETRAIN_DIR.mkdir(parents=True, exist_ok=True)

    transcripts: list[str] = []
    utterances: list[str] = []
    reply_pairs: list[dict[str, Any]] = []
    thread_count = 0

    for path in sorted(RAW_DIR.glob("*.md")):
        if path.name.startswith("0000-"):
            continue
        payload, conv_id, title = load_conversation(path)
        messages = extract_messages(payload)
        if not messages:
            continue

        thread_text = render_thread(conv_id, title, messages)
        out_path = CLEAN_THREADS_DIR / f"{path.stem}.txt"
        out_path.write_text(thread_text, encoding="utf-8")
        transcripts.append(thread_text.strip())
        utterances.extend(msg["text"].replace("\r\n", "\n").strip() for msg in messages if msg["text"].strip())
        reply_pairs.extend(build_reply_pairs(conv_id, title, out_path.relative_to(ROOT).as_posix(), messages))
        thread_count += 1

    (PRETRAIN_DIR / "conversation_threads.txt").write_text("\n\n".join(transcripts).strip() + "\n", encoding="utf-8")
    (PRETRAIN_DIR / "conversation_utterances.txt").write_text("\n".join(utterances).strip() + "\n", encoding="utf-8")

    with (SFT_DIR / "reply_pairs.jsonl").open("w", encoding="utf-8") as handle:
        for pair in reply_pairs:
            handle.write(json.dumps(pair, ensure_ascii=False) + "\n")

    manifest = {
        "threads": thread_count,
        "utterances": len(utterances),
        "reply_pairs": len(reply_pairs),
        "raw_source": str(RAW_DIR),
        "thread_dir": str(CLEAN_THREADS_DIR),
        "pretrain_threads": str(PRETRAIN_DIR / "conversation_threads.txt"),
        "pretrain_utterances": str(PRETRAIN_DIR / "conversation_utterances.txt"),
        "sft_pairs": str(SFT_DIR / "reply_pairs.jsonl"),
    }
    (PRETRAIN_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return {"threads": thread_count, "utterances": len(utterances), "reply_pairs": len(reply_pairs)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize markdown_export_raw conversations into transcript corpora.")
    _ = parser.parse_args()
    stats = normalize_corpus()
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
