from __future__ import annotations

from pathlib import Path

import yaml

from src.model_backends.load_backend import get_default_backend_name
from src.runtime.mode_router import load_runtime_modes

from .front_matter_schema import PromptFrontMatter, ResponsePlanFrontMatter

ROOT = Path(__file__).resolve().parents[2]
QUERY_PROFILE_PATH = ROOT / "configs" / "memory_query_profiles.yaml"


def _load_query_profiles() -> dict:
    return yaml.safe_load(QUERY_PROFILE_PATH.read_text(encoding="utf-8"))


def build_response_plan(
    front_matter: PromptFrontMatter,
    backend_name: str | None = None,
    mode_name: str | None = None,
    include_context: bool | None = None,
    include_rs1_specialty: bool | None = None,
    include_rs1_creative: bool | None = None,
    retrieval_profile: str | None = None,
    memory_top_k: int | None = None,
) -> ResponsePlanFrontMatter:
    runtime_modes = load_runtime_modes()
    query_profiles = _load_query_profiles()["profiles"]
    selected_mode = mode_name or front_matter.mode or runtime_modes["default_mode"]
    selected_backend = backend_name or get_default_backend_name()
    profile = retrieval_profile or front_matter.retrieval_profile
    profile_cfg = query_profiles.get(profile, query_profiles["technical"])

    rs1_specialty = (
        include_rs1_specialty
        if include_rs1_specialty is not None
        else front_matter.reasoning_mode == "rs1_specialty"
    )
    rs1_creative = (
        include_rs1_creative
        if include_rs1_creative is not None
        else front_matter.reasoning_mode == "rs1_creative"
    )
    if include_context is None:
        include_context_flag = front_matter.memory_scope in {"scoped", "constrained"}
    else:
        include_context_flag = include_context

    include_memory_context = front_matter.memory_scope != "none"
    output_shape = "json" if front_matter.output_format == "json" else "text"
    notes = [
        f"mode={selected_mode}",
        f"backend={selected_backend}",
        f"retrieval_profile={profile}",
    ]
    if rs1_specialty:
        notes.append("rs1_specialty overlay enabled")
    if rs1_creative:
        notes.append("rs1_creative overlay enabled")
    if not include_memory_context:
        notes.append("memory retrieval disabled by memory_scope")

    return ResponsePlanFrontMatter(
        selected_backend=selected_backend,
        selected_mode=selected_mode,
        include_context=include_context_flag,
        include_memory_context=include_memory_context,
        include_rs1_specialty=rs1_specialty,
        include_rs1_creative=rs1_creative,
        retrieval_profile=profile,
        memory_top_k=int(memory_top_k or profile_cfg["top_k"]),
        output_shape=output_shape,
        confidence=front_matter.confidence,
        route_notes=notes,
    )
