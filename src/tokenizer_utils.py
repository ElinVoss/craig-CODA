from __future__ import annotations

import json
from pathlib import Path

from tokenizers import Tokenizer


def load_yaml(path: Path) -> dict:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_tokenizer(path: Path) -> Tokenizer:
    return Tokenizer.from_file(str(path))
