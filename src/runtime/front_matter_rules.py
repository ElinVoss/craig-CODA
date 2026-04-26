from __future__ import annotations

from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "prompt_front_matter.yaml"


def load_front_matter_rules(config_path: str | Path | None = None) -> dict:
    path = Path(config_path) if config_path is not None else CONFIG_PATH
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def keyword_score(text: str, keywords: list[str]) -> int:
    normalized = normalize_text(text)
    return sum(1 for keyword in keywords if keyword.lower() in normalized)


def choose_label(text: str, options: dict[str, list[str]], default: str) -> tuple[str, int]:
    best_label = default
    best_score = 0
    for label, keywords in options.items():
        score = keyword_score(text, keywords)
        if score > best_score:
            best_label = label
            best_score = score
    return best_label, best_score


def mode_hints(text: str, config: dict) -> tuple[str, list[str]]:
    normalized = normalize_text(text)
    notes: list[str] = []
    mode = config["defaults"]["mode"]
    fiction_hits = keyword_score(normalized, config["routing"]["fiction_mode_keywords"])
    if fiction_hits:
        mode = "elin_fiction"
        notes.append("fiction keywords selected elin_fiction")
    return mode, notes


def reasoning_hints(text: str, config: dict) -> tuple[str, list[str]]:
    normalized = normalize_text(text)
    notes: list[str] = []
    specialty_hits = keyword_score(normalized, config["routing"]["rs1_specialty_keywords"])
    creative_hits = keyword_score(normalized, config["routing"]["rs1_creative_keywords"])
    if specialty_hits >= creative_hits and specialty_hits > 0:
        notes.append("audit-style keywords selected rs1_specialty")
        return "rs1_specialty", notes
    if creative_hits > 0:
        notes.append("creative keywords selected rs1_creative")
        return "rs1_creative", notes
    return config["defaults"]["reasoning_mode"], notes
