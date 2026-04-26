from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.runtime.front_matter_builder import build_prompt_front_matter
from src.runtime.front_matter_renderer import render_front_matter, render_response_plan
from src.runtime.response_plan_builder import build_response_plan


SAMPLE_PROMPTS = [
    "Explain the runtime routing constraints for Craig mode and keep it direct.",
    "Write a short Elin scene in the warehouse aisle with vivid prose.",
    "Critique this brittle system design and surface the structural failure mode.",
]


def main() -> int:
    for prompt in SAMPLE_PROMPTS:
        front_matter = build_prompt_front_matter(prompt)
        plan = build_response_plan(front_matter)
        print("=" * 72)
        print(f"Prompt: {prompt}")
        print(f"Confidence: {front_matter.confidence:.2f}")
        print("\nPrompt Front Matter")
        print(render_front_matter(front_matter))
        print("\nResponse Plan")
        print(render_response_plan(plan))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
