from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_runtime_modes(config_path: str | Path | None = None) -> dict:
    if config_path is None:
        config_path = ROOT / "configs" / "runtime_modes.yaml"
    path = Path(config_path)
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def resolve_mode_files(
    mode_name: str,
    include_context: bool = False,
    include_rs1_specialty: bool = False,
    include_rs1_creative: bool = False,
    config_path: str | Path | None = None,
) -> list[Path]:
    config = load_runtime_modes(config_path)
    if mode_name not in config["modes"]:
        raise ValueError(f"Unknown mode: {mode_name}")
    mode_cfg = config["modes"][mode_name]
    selected = [ROOT / rel for rel in mode_cfg["base_files"]]
    if include_context:
        selected.extend(ROOT / rel for rel in mode_cfg.get("optional_context_files", []))
    if include_rs1_specialty:
        selected.append(ROOT / config["overlays"]["rs1_specialty"]["path"])
    if include_rs1_creative:
        selected.append(ROOT / config["overlays"]["rs1_creative"]["path"])

    forbidden = set(config["forbidden_auto_load_folders"])
    for path in selected:
        parts = set(path.relative_to(ROOT / "exports" / "user_model_package").parts) if "exports" in path.parts else set()
        if forbidden.intersection(parts):
            raise ValueError(f"Forbidden auto-load path selected: {path}")
    return selected

