from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

REQUIRED_SCOPE_KEYS = ("summary", "read_order", "work_from")


def normalize_phrase(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def load_scope_map(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict) or not isinstance(data.get("scopes"), dict):
        raise ValueError("SCOPE_MAP.yaml must contain a top-level 'scopes' mapping")
    return data


def resolve_scope(query: str, scope_map: dict[str, Any]) -> str:
    scopes = scope_map["scopes"]
    normalized = normalize_phrase(query)
    for scope_name in scopes:
        if normalized == normalize_phrase(scope_name):
            return scope_name
    for scope_name, scope_cfg in scopes.items():
        aliases = [normalize_phrase(alias) for alias in scope_cfg.get("aliases", [])]
        if normalized in aliases:
            return scope_name
    if "handoff" in scopes:
        return "handoff"
    raise KeyError("No scope matched query and no 'handoff' fallback scope exists")


def validate_scope_map(
    config_path: Path,
    root: Path,
    check_paths: bool = True,
) -> list[str]:
    errors: list[str] = []
    data = load_scope_map(config_path)
    scopes = data["scopes"]

    for scope_name, scope_cfg in scopes.items():
        if not isinstance(scope_cfg, dict):
            errors.append(f"{scope_name}: scope config must be a mapping")
            continue
        for key in REQUIRED_SCOPE_KEYS:
            if key not in scope_cfg:
                errors.append(f"{scope_name}: missing required key '{key}'")
        read_order = scope_cfg.get("read_order", [])
        if not isinstance(read_order, list) or not all(isinstance(item, str) for item in read_order):
            errors.append(f"{scope_name}: read_order must be a list of relative path strings")
            continue
        work_from = scope_cfg.get("work_from")
        if not isinstance(work_from, str):
            errors.append(f"{scope_name}: work_from must be a relative path string")
            continue
        if work_from not in read_order:
            errors.append(f"{scope_name}: work_from must also appear in read_order")
        aliases = scope_cfg.get("aliases", [])
        if aliases and (not isinstance(aliases, list) or not all(isinstance(item, str) for item in aliases)):
            errors.append(f"{scope_name}: aliases must be a list of strings")
        if not check_paths:
            continue
        for rel_path in read_order:
            target = root / rel_path
            if not target.exists():
                errors.append(f"{scope_name}: missing path '{rel_path}'")

    return errors
