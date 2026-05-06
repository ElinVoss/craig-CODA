from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

import yaml

from .node_schema import VaultNode
from .normalize_sources import SourceDocument, collect_source_documents

ROOT = Path(__file__).resolve().parents[2]
DATE_PATTERN = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
TAG_PATTERN = re.compile(r"#([A-Za-z0-9_-]+)")
WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]]+)\]\]")
MARKDOWN_LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
MENTION_PATTERN = re.compile(r"@([A-Za-z0-9_-]+)")


def _read_fragments(path: Path, source_kind: str | None = None) -> list[str]:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    if source_kind in {"conversation_export_raw", "conversation_transcript"}:
        return [text]
    if suffix == ".jsonl":
        fragments = []
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                fragments.append(json.dumps(data, indent=2, ensure_ascii=False))
            except json.JSONDecodeError:
                fragments.append(line)
        return fragments
    if suffix in {".yaml", ".yml"}:
        try:
            rendered = yaml.safe_dump(yaml.safe_load(text), sort_keys=False).strip()
            return [rendered] if rendered else []
        except yaml.YAMLError:
            return [text]
    fragments = [fragment.strip() for fragment in re.split(r"\n\s*\n", text) if fragment.strip()]
    return fragments or [text]


def _summary(text: str, limit: int = 180) -> str:
    compact = re.sub(r"\s+", " ", text).strip()
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + "..."


def _extract_dates(text: str, fallback: str) -> tuple[str, str | None, str | None]:
    matches = DATE_PATTERN.findall(text)
    if matches:
        return fallback, matches[0], matches[-1]
    return fallback, None, None


def _life_phase(path: Path, tags: list[str]) -> str:
    lowered_parts = [part.lower() for part in path.parts]
    if "warehouse" in lowered_parts or "warehouse" in tags:
        return "warehouse"
    if "fiction" in lowered_parts or "elin" in tags:
        return "fiction"
    return "current"


def _project_relevance(text: str, path: Path) -> float:
    keywords = ["craig", "elin", "rs-1", "warehouse", "runtime", "prompt", "context", "memory"]
    haystack = f"{path.as_posix()} {text}".lower()
    hits = sum(1 for keyword in keywords if keyword in haystack)
    return min(1.0, 0.2 + hits * 0.1)


def _voice_scores(text: str) -> tuple[float, float, float]:
    lowered = text.lower()
    voice = 0.7 if any(word in lowered for word in ["direct", "inspectable", "concise"]) else 0.45
    reasoning = 0.75 if any(word in lowered for word in ["constraint", "because", "lesson", "audit"]) else 0.45
    prose = 0.8 if any(word in lowered for word in ["shadow", "scene", "breath", "light"]) else 0.35
    return voice, reasoning, prose


def _node_type(path: Path, text: str) -> str:
    lowered = f"{path.as_posix()} {text}".lower()
    if "constraint" in lowered:
        return "constraint_note"
    if "event" in lowered or DATE_PATTERN.search(text):
        return "event_note"
    if "prose" in lowered or "scene" in lowered:
        return "prose_fragment"
    if "hypothesis:" in lowered:
        return "interpretive_note"
    if "profile" in lowered or "identity" in lowered:
        return "identity_note"
    return "note"


def extract_nodes(documents: list[SourceDocument] | None = None) -> list[VaultNode]:
    source_documents = documents if documents is not None else collect_source_documents()
    nodes: list[VaultNode] = []
    for document in source_documents:
        modified = datetime.utcfromtimestamp(document.path.stat().st_mtime).replace(microsecond=0).isoformat()
        for index, fragment in enumerate(_read_fragments(document.path, document.source_kind), start=1):
            tags = sorted(set(document.root_tags + TAG_PATTERN.findall(fragment)))
            links = sorted(set(WIKI_LINK_PATTERN.findall(fragment) + MARKDOWN_LINK_PATTERN.findall(fragment)))
            people = sorted(set(MENTION_PATTERN.findall(fragment)))
            projects = sorted({tag for tag in tags if tag in {"craig", "elin", "warehouse", "runtime", "rs1"}})
            created_at, time_start, time_end = _extract_dates(fragment, modified)
            voice_score, reasoning_score, prose_score = _voice_scores(fragment)
            raw_id = f"{document.path.as_posix()}::{index}::{fragment}"
            node_id = hashlib.sha1(raw_id.encode("utf-8")).hexdigest()[:16]
            nodes.append(
                VaultNode(
                    id=node_id,
                    node_type=_node_type(document.path, fragment),
                    trust_layer="episodic_events",
                    content=fragment,
                    summary=_summary(fragment),
                    source_path=str(document.path.relative_to(ROOT).as_posix()),
                    source_kind=document.source_kind,
                    created_at=created_at,
                    time_start=time_start,
                    time_end=time_end,
                    life_phase=_life_phase(document.path, tags),
                    people=people,
                    projects=projects,
                    tags=tags,
                    links=links,
                    confidence=0.74,
                    privacy_level="standard",
                    reinforcement_count=0,
                    voice_score=voice_score,
                    reasoning_score=reasoning_score,
                    prose_score=prose_score,
                    project_relevance=_project_relevance(fragment, document.path),
                )
            )
    return nodes
