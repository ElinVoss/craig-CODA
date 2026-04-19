from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CleaningOptions:
    lowercase: bool = False
    remove_short_lines: bool = False
    min_line_length: int = 3
    remove_duplicate_lines: bool = False
    preserve_blank_lines: bool = False
    max_blank_lines: int = 2


def normalize_line_endings(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def clean_text(text: str, options: CleaningOptions) -> str:
    text = normalize_line_endings(text)
    lines = [line.strip() for line in text.split("\n")]

    cleaned: list[str] = []
    seen: set[str] = set()
    blank_run = 0

    for line in lines:
        if options.lowercase:
            line = line.lower()
        if not line:
            blank_run += 1
            if options.preserve_blank_lines and blank_run <= options.max_blank_lines:
                cleaned.append("")
            continue

        blank_run = 0
        if options.remove_short_lines and len(line) < options.min_line_length:
            continue
        if options.remove_duplicate_lines:
            key = line.lower()
            if key in seen:
                continue
            seen.add(key)
        cleaned.append(line)

    if not options.preserve_blank_lines:
        collapsed: list[str] = []
        previous_blank = False
        for line in cleaned:
            is_blank = not line
            if is_blank and previous_blank:
                continue
            collapsed.append(line)
            previous_blank = is_blank
        cleaned = collapsed

    return "\n".join(cleaned).strip() + ("\n" if cleaned else "")


def split_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    buffer: list[str] = []
    for line in normalize_line_endings(text).split("\n"):
        stripped = line.strip()
        if not stripped:
            if buffer:
                paragraphs.append(" ".join(buffer).strip())
                buffer = []
            continue
        buffer.append(stripped)
    if buffer:
        paragraphs.append(" ".join(buffer).strip())
    return [paragraph for paragraph in paragraphs if paragraph]
