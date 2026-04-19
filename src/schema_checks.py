from __future__ import annotations


REQUIRED_SCHEMAS = {
    "sft": ["id", "system", "input", "output", "tags", "source_file"],
    "prefs": ["id", "prompt", "chosen", "rejected", "notes", "source_file"],
    "eval": ["id", "task", "input", "expected_characteristics", "notes", "source_file"],
}


def validate_required_fields(record: dict, required_fields: list[str]) -> list[str]:
    return [field for field in required_fields if field not in record]

