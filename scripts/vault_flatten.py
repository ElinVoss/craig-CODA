"""
vault_flatten.py — Step 1 of the craig-CODA Obsidian vault build.

Walks the entire repo and produces a flat node manifest of every meaningful
file and directory. Output: exports/obsidian_vault/_graph/manifest.json

Story roles assigned:
  world_rule   — governing docs: DECISIONS.md, SCOPE_MAP.yaml, etc.
  timeline     — LIVE_HANDOFF.md
  lore         — _method.md notes, config YAMLs
  character    — Python source modules (src/, scripts/, runtime/, graph/)
  guardian     — test files (tests/**/)
  location     — directories
  artifact     — generated outputs under artifacts/, exports/ (non-vault)

The vault's own output directory (exports/obsidian_vault/) is hard-excluded
to prevent self-ingestion on re-runs.
"""

import ast
import hashlib
import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
OUTPUT_DIR = REPO_ROOT / "exports" / "obsidian_vault"
MANIFEST_PATH = OUTPUT_DIR / "_graph" / "manifest.json"

# Relative paths (always forward-slash) that are fully excluded from scanning
EXCLUDE_REL_PREFIXES = {
    "exports/obsidian_vault",
    ".git",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".mypy_cache",
    "dist",
    "build",
}

# Directory *names* that are excluded wherever they appear in the tree
EXCLUDE_DIR_NAMES = {
    "node_modules", "__pycache__", ".git",
    ".pytest_cache", ".mypy_cache", "dist", "build",
}

EXCLUDE_EXTENSIONS = {
    ".pyc", ".pyo",
    ".bin", ".safetensors", ".pt", ".pth", ".pkl", ".pickle",
    ".h5", ".hdf5", ".npy", ".npz",
    ".zip", ".tar", ".gz", ".7z",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot",
}

INCLUDE_EXTENSIONS = {".py", ".yaml", ".yml", ".md", ".txt", ".json", ".toml"}

WORLD_RULE_NAMES = {
    "DECISIONS.md", "CURRENT_STATE.md", "HANDOFF_PROMPT.md",
    "SCOPE_MAP.yaml", "AGENTS.md", "NEXT_STEPS.md", "README.md",
    "CLAUDE.md", "ARTIFACTS.md",
}

GENERATOR_VERSION = "1.0"


def rel_forward(path: Path) -> str:
    """Repo-relative path with forward slashes."""
    return str(path.relative_to(REPO_ROOT)).replace("\\", "/")


def make_stable_id(rel: str) -> str:
    """
    Convert a repo-relative path to a stable, unique node ID.

    Segments joined with '--', dots replaced with '-'.
    Example: src/adapters/ollama_adapter.py → src--adapters--ollama_adapter-py
    """
    parts = Path(rel).parts
    return "--".join(p.replace(".", "-") for p in parts)


def assign_story_role(rel: str, file_type: str) -> str:
    p = Path(rel)
    parts = set(p.parts)

    if p.name == "LIVE_HANDOFF.md":
        return "timeline"

    if p.name in WORLD_RULE_NAMES:
        return "world_rule"

    # Guardian: any test file anywhere in tests/
    if "tests" in parts and p.name.startswith("test_") and p.suffix == ".py":
        return "guardian"

    # Lore: method vault _method.md notes
    if "method_vault" in parts and p.name == "_method.md":
        return "lore"

    # Lore: configs/*.yaml
    if "configs" in parts and p.suffix in (".yaml", ".yml"):
        return "lore"

    # Character: Python source in known code dirs
    code_dirs = {"src", "scripts", "runtime", "graph", "agent", "eval"}
    if parts & code_dirs and p.suffix == ".py":
        return "character"

    # Artifact: anything under artifacts/
    if "artifacts" in parts:
        return "artifact"

    # Artifact: exports/ that isn't the method vault
    if "exports" in parts and "method_vault" not in parts:
        return "artifact"

    # Data
    if "data" in parts:
        return "artifact"

    # Remaining markdown
    if p.suffix == ".md":
        return "world_rule"

    return "artifact"


def extract_python_metadata(path: Path) -> dict:
    try:
        source = path.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except Exception:
        return {"functions": [], "classes": [], "imports": [], "docstring": ""}

    docstring = ast.get_docstring(tree) or ""
    functions, classes, imports = [], [], []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.col_offset == 0:
                functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return {
        "functions": functions[:25],
        "classes": classes[:15],
        "imports": list(dict.fromkeys(imports))[:30],  # dedupe, preserve order
        "docstring": docstring[:500],
    }


def extract_yaml_front_matter(path: Path) -> dict:
    try:
        import yaml
        content = path.read_text(encoding="utf-8", errors="replace")
        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                return yaml.safe_load(content[3:end]) or {}
    except Exception:
        pass
    return {}


def extract_markdown_metadata(path: Path) -> dict:
    try:
        import yaml
        content = path.read_text(encoding="utf-8", errors="replace")
        front_matter = {}
        body = content

        if content.startswith("---"):
            end = content.find("---", 3)
            if end > 0:
                try:
                    front_matter = yaml.safe_load(content[3:end]) or {}
                except Exception:
                    pass
                body = content[end + 3:]

        title = front_matter.get("title", "")
        if not title:
            m = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            if m:
                title = m.group(1).strip()

        # Backtick file references
        file_refs = re.findall(r"`([^`]+\.[a-zA-Z]+)`", body)
        # Explicit path refs like `src/foo.py`
        path_refs = re.findall(r"`([a-zA-Z0-9_./\\-]+/[a-zA-Z0-9_./\\-]+)`", body)

        return {
            "front_matter": front_matter,
            "title": title or path.stem,
            "file_refs": list(dict.fromkeys(file_refs + path_refs))[:30],
            "summary": body.strip()[:400],
        }
    except Exception:
        return {"front_matter": {}, "title": path.stem, "file_refs": [], "summary": ""}


def content_hash(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except Exception:
        return "unknown"


def is_excluded(rel: str) -> bool:
    for prefix in EXCLUDE_REL_PREFIXES:
        if rel == prefix or rel.startswith(prefix + "/"):
            return True
    # Exclude any path that contains an excluded directory name as a path segment
    if set(Path(rel).parts) & EXCLUDE_DIR_NAMES:
        return True
    return False


def walk_repo() -> list:
    nodes = []

    for root_str, dirs, files in os.walk(REPO_ROOT):
        root_path = Path(root_str)
        rel_root = rel_forward(root_path)

        if is_excluded(rel_root):
            dirs.clear()
            continue

        # Prune excluded subdirs in-place so os.walk doesn't descend into them
        dirs[:] = [
            d for d in dirs
            if not is_excluded(rel_root + "/" + d if rel_root != "." else d)
            and not d.startswith(".")
        ]
        dirs.sort()

        # Directory node (skip the repo root itself)
        if rel_root != ".":
            nodes.append({
                "id": make_stable_id(rel_root),
                "path": rel_root,
                "node_type": "directory",
                "file_type": "directory",
                "story_role": "location",
                "display_name": root_path.name,
                "metadata": {},
                "content_hash": None,
            })

        for fname in sorted(files):
            fpath = root_path / fname
            rel = rel_forward(fpath)

            if is_excluded(rel):
                continue
            if fpath.suffix.lower() in EXCLUDE_EXTENSIONS:
                continue
            if fpath.suffix.lower() not in INCLUDE_EXTENSIONS:
                continue

            ext = fpath.suffix.lower()
            if ext == ".py":
                file_type = "python_module"
                if fpath.name.startswith("test_"):
                    file_type = "test_module"
                metadata = extract_python_metadata(fpath)
                display_name = fpath.stem
            elif ext in (".yaml", ".yml"):
                file_type = "method_note" if fpath.name == "_method.md" else "config_yaml"
                raw_fm = extract_yaml_front_matter(fpath)
                metadata = {"front_matter": raw_fm}
                display_name = raw_fm.get("title", "") or fpath.stem
            elif ext == ".md":
                file_type = "method_note" if fpath.name == "_method.md" else "markdown_doc"
                metadata = extract_markdown_metadata(fpath)
                display_name = metadata.get("title", "") or fpath.stem
            else:
                file_type = "artifact_data"
                metadata = {}
                display_name = fpath.name

            story_role = assign_story_role(rel, file_type)

            nodes.append({
                "id": make_stable_id(rel),
                "path": rel,
                "node_type": "file",
                "file_type": file_type,
                "story_role": story_role,
                "display_name": display_name or fpath.stem,
                "metadata": metadata,
                "content_hash": content_hash(fpath),
            })

    return nodes


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "_graph").mkdir(exist_ok=True)

    nodes = walk_repo()

    manifest = {
        "schema_version": "1.0",
        "generator_version": GENERATOR_VERSION,
        "repo_root": str(REPO_ROOT),
        "node_count": len(nodes),
        "nodes": nodes,
    }

    MANIFEST_PATH.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    by_role: dict = {}
    for n in nodes:
        by_role[n["story_role"]] = by_role.get(n["story_role"], 0) + 1

    print(f"vault_flatten: {len(nodes)} nodes written to {MANIFEST_PATH}")
    for role, count in sorted(by_role.items()):
        print(f"  {role:15s} {count}")


if __name__ == "__main__":
    main()
