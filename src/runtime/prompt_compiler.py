from __future__ import annotations

from pathlib import Path

import yaml

from .mode_router import resolve_mode_files

ROOT = Path(__file__).resolve().parents[2]


def _render_file(path: Path) -> str:
    suffix = path.suffix.lower()
    text = path.read_text(encoding="utf-8").strip()
    if suffix in {".yaml", ".yml"}:
        data = yaml.safe_load(text)
        rendered = yaml.safe_dump(data, sort_keys=False).strip()
        return f"[{path.name}]\n{rendered}"
    return f"[{path.name}]\n{text}"


def compile_mode_prompt(
    mode_name: str,
    include_context: bool = False,
    include_rs1_specialty: bool = False,
    include_rs1_creative: bool = False,
    memory_context: str | None = None,
) -> tuple[str, list[Path]]:
    files = resolve_mode_files(
        mode_name=mode_name,
        include_context=include_context,
        include_rs1_specialty=include_rs1_specialty,
        include_rs1_creative=include_rs1_creative,
    )
    missing = [path for path in files if not path.is_file()]
    if missing:
        raise FileNotFoundError("Missing prompt files: " + ", ".join(str(path) for path in missing))
    blocks = [_render_file(path) for path in files]
    if memory_context:
        blocks.append(f"[memory_context]\n{memory_context.strip()}")
    prompt = "\n\n".join(blocks)
    print("Prompt compiler included:")
    for path in files:
        print(f"- {path}")
    return prompt, files
