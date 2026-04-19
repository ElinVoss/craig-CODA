from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .text_cleaning import split_paragraphs


@dataclass(frozen=True)
class IngestedDocument:
    source_file: str
    source_type: str
    text: str


def build_pretrain_corpus(documents: Iterable[IngestedDocument]) -> str:
    chunks: list[str] = []
    for doc in documents:
        if doc.text.strip():
            chunks.append(f"### Source: {doc.source_file}\n{doc.text.strip()}")
    return "\n\n".join(chunks).strip() + ("\n" if chunks else "")


def _tags_for_document(doc: IngestedDocument) -> list[str]:
    tags = [doc.source_type, "placeholder"]
    if doc.source_file.lower().endswith(".md"):
        tags.append("markdown")
    return tags


def build_sft_records(documents: Iterable[IngestedDocument]) -> list[dict]:
    records: list[dict] = []
    for index, doc in enumerate(documents, start=1):
        paragraphs = split_paragraphs(doc.text)
        if not paragraphs:
            continue
        first = paragraphs[0]
        summary = first if len(first) <= 240 else first[:237].rstrip() + "..."
        records.append(
            {
                "id": f"sft-{index:04d}",
                "system": "You are a concise local writing assistant.",
                "input": f"Summarize the following source fragment from {doc.source_file}.",
                "output": summary,
                "tags": _tags_for_document(doc) + ["summary"],
                "source_file": doc.source_file,
                "created_by_pipeline": "placeholder_rule_based_v1",
                "notes": "Generated from the first paragraph of cleaned source text.",
            }
        )
    return records


def build_pref_records(documents: Iterable[IngestedDocument]) -> list[dict]:
    records: list[dict] = []
    for index, doc in enumerate(documents, start=1):
        paragraphs = split_paragraphs(doc.text)
        if len(paragraphs) < 2:
            continue
        chosen = paragraphs[0]
        rejected = paragraphs[1]
        records.append(
            {
                "id": f"pref-{index:04d}",
                "prompt": f"Select the better continuation for {doc.source_file}.",
                "chosen": chosen,
                "rejected": rejected,
                "notes": "Placeholder preference pair created from the first two paragraphs of the same source file.",
                "source_file": doc.source_file,
                "created_by_pipeline": "placeholder_rule_based_v1",
            }
        )
    return records


def build_eval_records(documents: Iterable[IngestedDocument]) -> list[dict]:
    records: list[dict] = []
    for index, doc in enumerate(documents, start=1):
        paragraphs = split_paragraphs(doc.text)
        if not paragraphs:
            continue
        text = paragraphs[0]
        records.append(
            {
                "id": f"eval-{index:04d}",
                "task": "describe_source",
                "input": f"What is the main idea of {doc.source_file}?",
                "expected_characteristics": ["accurate", "concise", "grounded in the source text"],
                "notes": "Placeholder eval item derived from the first paragraph of the cleaned source.",
                "source_file": doc.source_file,
                "created_by_pipeline": "placeholder_rule_based_v1",
                "reference_snippet": text[:200],
            }
        )
    return records

