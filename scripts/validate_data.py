from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_DIRS = [
    "configs",
    "data/raw",
    "data/clean",
    "data/sft",
    "data/prefs",
    "data/pretrain",
    "data/eval",
    "scripts",
    "src",
    "notebooks",
    "logs",
    "checkpoints",
    "exports",
]

SCHEMAS = {
    "sft": {
        "path": ROOT / "data/sft/sample.jsonl",
        "required": ["id", "system", "input", "output", "tags"],
    },
    "prefs": {
        "path": ROOT / "data/prefs/sample.jsonl",
        "required": ["id", "prompt", "chosen", "rejected", "notes"],
    },
    "eval": {
        "path": ROOT / "data/eval/sample.jsonl",
        "required": ["id", "task", "input", "expected_characteristics", "notes"],
    },
}


def read_jsonl(path: Path) -> list[dict]:
    records = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}: line {line_no}: invalid JSON: {exc.msg}") from exc
            if not isinstance(value, dict):
                raise ValueError(f"{path}: line {line_no}: expected JSON object")
            records.append(value)
    if not records:
        raise ValueError(f"{path}: no records found")
    return records


def validate_required_fields(path: Path, records: list[dict], required: list[str]) -> None:
    for index, record in enumerate(records, start=1):
        missing = [field for field in required if field not in record]
        if missing:
            raise ValueError(f"{path}: record {index}: missing fields: {', '.join(missing)}")


def main() -> int:
    print(f"Validating repository at {ROOT}")
    errors: list[str] = []

    for relative in REQUIRED_DIRS:
        path = ROOT / relative
        if not path.is_dir():
            errors.append(f"Missing directory: {relative}")

    for name, spec in SCHEMAS.items():
        path = spec["path"]
        if not path.is_file():
            errors.append(f"Missing sample file: {path.relative_to(ROOT)}")
            continue
        try:
            records = read_jsonl(path)
            validate_required_fields(path, records, spec["required"])
            print(f"OK {name}: {len(records)} records")
        except ValueError as exc:
            errors.append(str(exc))

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

