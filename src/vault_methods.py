from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any

import yaml

from .io_utils import write_json

ROOT = Path(__file__).resolve().parents[1]
METHOD_VAULT_ROOT = ROOT / "exports" / "user_model_package" / "method_vault"
METHOD_FILE_NAME = "_method.md"
METHOD_ARTIFACT_DIR = ROOT / "artifacts" / "methods"

STAGE_PATHS: dict[str, Path] = {
    "corpus": Path("corpus") / "conversation",
    "tokenizer": Path("tokenizer") / "default",
    "scratch": Path("weights") / "scratch",
    "sft": Path("weights") / "sft",
}


def _split_front_matter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith("---\n"):
        return {}, text.strip()
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text.strip()
    front_matter = text[4:end]
    body = text[end + 4 :].strip()
    data = yaml.safe_load(front_matter) or {}
    if not isinstance(data, dict):
        raise ValueError("Method front matter must be a mapping")
    return data, body


def _merge_values(base: Any, overlay: Any) -> Any:
    if isinstance(base, dict) and isinstance(overlay, dict):
        merged = deepcopy(base)
        for key, value in overlay.items():
            if key in merged:
                merged[key] = _merge_values(merged[key], value)
            else:
                merged[key] = deepcopy(value)
        return merged
    if isinstance(base, list) and isinstance(overlay, list):
        merged = list(base)
        for item in overlay:
            if item not in merged:
                merged.append(item)
        return merged
    return deepcopy(overlay)


def _collect_method_files(stage: str, vault_root: Path | None = None) -> list[Path]:
    root = vault_root or METHOD_VAULT_ROOT
    stage_path = STAGE_PATHS[stage]
    files: list[Path] = []

    current = root
    root_method = current / METHOD_FILE_NAME
    if root_method.is_file():
        files.append(root_method)

    for part in stage_path.parts:
        current = current / part
        method_path = current / METHOD_FILE_NAME
        if method_path.is_file():
            files.append(method_path)

    return files


def _collect_architecture_files(profile: str, vault_root: Path | None = None) -> list[Path]:
    root = vault_root or METHOD_VAULT_ROOT
    walk = [
        Path("weights"),
        Path("weights") / "architecture",
        Path("weights") / "architecture" / profile,
    ]
    files: list[Path] = []

    root_method = root / METHOD_FILE_NAME
    if root_method.is_file():
        files.append(root_method)

    for path in walk:
        method_path = root / path / METHOD_FILE_NAME
        if method_path.is_file():
            files.append(method_path)

    return files


def resolve_stage_config(stage: str, base_config: dict[str, Any], vault_root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    if stage not in STAGE_PATHS:
        raise KeyError(f"Unknown method stage: {stage}")

    root = vault_root or METHOD_VAULT_ROOT
    resolved = deepcopy(base_config)
    applied_prompts: list[dict[str, Any]] = []

    for method_path in _collect_method_files(stage, root):
        front_matter, body = _split_front_matter(method_path.read_text(encoding="utf-8"))
        applies_to = [str(value) for value in front_matter.get("applies_to", ["*"])]
        if "*" not in applies_to and stage not in applies_to:
            continue
        config_patch = front_matter.get("config", {})
        if config_patch and not isinstance(config_patch, dict):
            raise ValueError(f"{method_path}: front matter 'config' must be a mapping")
        resolved = _merge_values(resolved, config_patch or {})
        applied_prompts.append(
            {
                "path": method_path.relative_to(ROOT).as_posix(),
                "title": str(front_matter.get("title", method_path.parent.name)),
                "applies_to": applies_to,
                "config": config_patch or {},
                "prompt": body,
            }
        )

    report = {
        "stage": stage,
        "vault_root": root.relative_to(ROOT).as_posix() if root.is_absolute() and root.exists() else str(root),
        "stage_path": STAGE_PATHS[stage].as_posix(),
        "applied_prompts": applied_prompts,
        "resolved_config": resolved,
    }
    return resolved, report


def resolve_architecture_config(profile: str, vault_root: Path | None = None) -> tuple[dict[str, Any], dict[str, Any]]:
    root = vault_root or METHOD_VAULT_ROOT
    resolved: dict[str, Any] = {}
    applied_prompts: list[dict[str, Any]] = []

    for method_path in _collect_architecture_files(profile, root):
        front_matter, body = _split_front_matter(method_path.read_text(encoding="utf-8"))
        applies_to = [str(v) for v in front_matter.get("applies_to", ["*"])]
        if "*" not in applies_to and "architecture" not in applies_to:
            continue
        config_patch = front_matter.get("config", {})
        if config_patch and not isinstance(config_patch, dict):
            raise ValueError(f"{method_path}: front matter 'config' must be a mapping")
        resolved = _merge_values(resolved, config_patch or {})
        applied_prompts.append(
            {
                "path": method_path.relative_to(ROOT).as_posix(),
                "title": str(front_matter.get("title", method_path.parent.name)),
                "applies_to": applies_to,
                "config": config_patch or {},
                "prompt": body,
            }
        )

    if not resolved:
        raise ValueError(
            f"No architecture config resolved for profile '{profile}'. "
            f"Check that vault note exists at: weights/architecture/{profile}/_method.md"
        )

    report = {
        "stage": "architecture",
        "profile": profile,
        "vault_root": root.relative_to(ROOT).as_posix() if root.is_absolute() and root.exists() else str(root),
        "walk_path": f"weights/architecture/{profile}",
        "applied_prompts": applied_prompts,
        "resolved_config": resolved,
    }
    return resolved, report


def write_stage_resolution(stage: str, report: dict[str, Any]) -> Path:
    path = METHOD_ARTIFACT_DIR / f"{stage}_resolution.json"
    write_json(path, report)
    return path


def write_architecture_resolution(profile: str, report: dict[str, Any]) -> Path:
    path = METHOD_ARTIFACT_DIR / f"architecture_{profile}_resolution.json"
    write_json(path, report)
    return path
