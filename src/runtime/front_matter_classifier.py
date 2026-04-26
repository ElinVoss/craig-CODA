from __future__ import annotations

from .front_matter_rules import choose_label, load_front_matter_rules, mode_hints, reasoning_hints
from .front_matter_schema import PromptFrontMatter


def classify_prompt(
    prompt: str,
    overrides: dict | None = None,
    config_path: str | None = None,
) -> PromptFrontMatter:
    config = load_front_matter_rules(config_path)
    defaults = config["defaults"]
    rules = config["rules"]
    notes: list[str] = []
    scores: list[int] = []

    values: dict[str, str | float] = {}
    for field in [
        "intent",
        "task_type",
        "domain",
        "style",
        "memory_scope",
        "retrieval_profile",
        "output_format",
        "stakes",
        "privacy_level",
    ]:
        label, score = choose_label(prompt, rules[field], defaults[field])
        values[field] = label
        scores.append(score)
        if score:
            notes.append(f"{field}={label} via keyword match ({score})")

    mode, mode_notes = mode_hints(prompt, config)
    values["mode"] = mode
    notes.extend(mode_notes)
    reasoning_mode, reasoning_notes = reasoning_hints(prompt, config)
    values["reasoning_mode"] = reasoning_mode
    notes.extend(reasoning_notes)

    values["tooling"] = defaults["tooling"]
    values["uncertainty_policy"] = defaults["uncertainty_policy"]

    base = float(config["confidence"]["base"])
    explicit = sum(1 for score in scores if score > 0) * float(config["confidence"]["explicit_keyword_bonus"])
    if values["mode"] != defaults["mode"]:
        explicit += float(config["confidence"]["explicit_mode_bonus"])
    ambiguity_penalty = float(config["confidence"]["ambiguity_penalty"]) if not any(scores) else 0.0
    confidence = max(0.2, min(0.98, base + explicit - ambiguity_penalty))

    values["confidence"] = confidence

    allowed_overrides = set(config["manual_overrides"]["allowed_fields"])
    for key, value in (overrides or {}).items():
        if key in allowed_overrides and value is not None:
            values[key] = value
            notes.append(f"manual override applied for {key}")

    if values["task_type"] == "fiction":
        values["mode"] = "elin_fiction"
        values["retrieval_profile"] = "prose"
        notes.append("fiction task_type forced elin_fiction + prose retrieval")
    elif values["task_type"] == "critique":
        values["reasoning_mode"] = "rs1_specialty"
        values["retrieval_profile"] = "critique"
        notes.append("critique task_type forced critique retrieval")
    elif values["memory_scope"] == "constrained":
        values["retrieval_profile"] = "constraints"
        notes.append("constrained memory scope selected constraints retrieval")

    return PromptFrontMatter(
        intent=str(values["intent"]),
        task_type=str(values["task_type"]),
        mode=str(values["mode"]),
        domain=str(values["domain"]),
        style=str(values["style"]),
        reasoning_mode=str(values["reasoning_mode"]),
        memory_scope=str(values["memory_scope"]),
        retrieval_profile=str(values["retrieval_profile"]),
        output_format=str(values["output_format"]),
        tooling=str(values["tooling"]),
        stakes=str(values["stakes"]),
        uncertainty_policy=str(values["uncertainty_policy"]),
        privacy_level=str(values["privacy_level"]),
        confidence=float(values["confidence"]),
        notes=notes,
    )
