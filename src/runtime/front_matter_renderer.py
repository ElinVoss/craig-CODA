from __future__ import annotations

import yaml

from .front_matter_schema import PromptFrontMatter, ResponsePlanFrontMatter


def render_front_matter(front_matter: PromptFrontMatter) -> str:
    return yaml.safe_dump(front_matter.to_dict(), sort_keys=False).strip()


def render_response_plan(plan: ResponsePlanFrontMatter) -> str:
    return yaml.safe_dump(plan.to_dict(), sort_keys=False).strip()
