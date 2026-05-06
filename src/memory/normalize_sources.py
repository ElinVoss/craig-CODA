from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "configs" / "vault_translation.yaml"


@dataclass(frozen=True)
class SourceDocument:
    path: Path
    source_kind: str
    root_tags: list[str]


def load_translation_config(config_path: str | Path | None = None) -> dict:
    path = Path(config_path) if config_path is not None else CONFIG_PATH
    if not path.is_absolute():
        path = ROOT / path
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def collect_source_documents(config_path: str | Path | None = None) -> list[SourceDocument]:
    config = load_translation_config(config_path)
    documents: list[SourceDocument] = []
    for root in config["source_roots"]:
        if not root.get("enabled", True):
            continue
        base = ROOT / root["path"]
        if not base.exists():
            continue
        include_extensions = {suffix.lower() for suffix in root.get("include_extensions", [])}
        exclude_globs = [str(pattern) for pattern in root.get("exclude_globs", [])]
        pattern = "**/*" if root.get("recursive", True) else "*"
        for path in sorted(base.glob(pattern)):
            if not path.is_file():
                continue
            if include_extensions and path.suffix.lower() not in include_extensions:
                continue
            relative = path.relative_to(base)
            if any(relative.match(glob) or path.name == glob for glob in exclude_globs):
                continue
            documents.append(
                SourceDocument(
                    path=path,
                    source_kind=str(root["source_kind"]),
                    root_tags=[str(tag) for tag in root.get("tags", [])],
                )
            )
    return documents
