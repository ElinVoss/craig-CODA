from __future__ import annotations

from .front_matter_classifier import classify_prompt
from .front_matter_schema import PromptFrontMatter


def build_prompt_front_matter(
    prompt: str,
    overrides: dict | None = None,
    config_path: str | None = None,
) -> PromptFrontMatter:
    return classify_prompt(prompt=prompt, overrides=overrides, config_path=config_path)
