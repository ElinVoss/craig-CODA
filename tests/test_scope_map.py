from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.handoff.scope_map import load_scope_map, resolve_scope, validate_scope_map


def _write_scope_map(tmp_path: Path, body: str) -> Path:
    tmp_path.mkdir(parents=True, exist_ok=True)
    path = tmp_path / "SCOPE_MAP.yaml"
    path.write_text(body.strip() + "\n", encoding="utf-8")
    return path


def test_resolve_scope_alias_and_fallback(tmp_path: Path):
    config_path = _write_scope_map(
        tmp_path,
        """
        scopes:
          handoff:
            summary: "Default handoff path."
            aliases:
              - "check out what ive got going"
            read_order:
              - README.md
            work_from: README.md
          vault:
            summary: "Vault path."
            aliases:
              - "method vault"
            read_order:
              - README.md
            work_from: README.md
        """,
    )
    data = load_scope_map(config_path)

    assert resolve_scope("vault", data) == "vault"
    assert resolve_scope("method vault", data) == "vault"
    assert resolve_scope("check out what ive got going", data) == "handoff"
    assert resolve_scope("something unknown", data) == "handoff"


def test_validate_scope_map_reports_missing_paths(tmp_path: Path):
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / "README.md").write_text("# test\n", encoding="utf-8")
    config_path = _write_scope_map(
        tmp_path,
        """
        scopes:
          handoff:
            summary: "Default handoff path."
            aliases: []
            read_order:
              - README.md
              - MISSING.md
            work_from: README.md
        """,
    )

    errors = validate_scope_map(config_path, tmp_path, check_paths=True)
    assert any("MISSING.md" in error for error in errors), errors


def test_root_handoff_files_exist():
    required = [
        ROOT / "SCOPE_MAP.yaml",
        ROOT / "CURRENT_STATE.md",
        ROOT / "DECISIONS.md",
        ROOT / "NEXT_STEPS.md",
        ROOT / "ARTIFACTS.md",
        ROOT / "LIVE_HANDOFF.md",
        ROOT / "HANDOFF_PROMPT.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == [], f"Missing root handoff files: {missing}"


def test_scope_map_has_required_scopes_without_path_checks():
    scope_map_path = ROOT / "SCOPE_MAP.yaml"
    data = load_scope_map(scope_map_path)
    for scope_name in [
        "handoff",
        "vault",
        "tokenizer",
        "weights",
        "memory",
        "runtime",
        "frontend",
        "agent",
        "configs",
        "artifacts",
        "data",
    ]:
        assert scope_name in data["scopes"], f"Missing scope '{scope_name}'"
    assert resolve_scope("check out what ive got going", data) == "handoff"
    assert validate_scope_map(scope_map_path, ROOT, check_paths=False) == []


def test_knowledge_branch_docs_exist():
    required = [
        ROOT / "exports/user_model_package/method_vault/AGENTS.md",
        ROOT / "exports/user_model_package/method_vault/README.md",
        ROOT / "configs/AGENTS.md",
        ROOT / "configs/README.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == [], f"Missing knowledge-branch docs: {missing}"


def test_operational_branch_docs_exist():
    required = [
        ROOT / "scripts/AGENTS.md",
        ROOT / "scripts/README.md",
        ROOT / "src/AGENTS.md",
        ROOT / "src/README.md",
        ROOT / "src/memory/AGENTS.md",
        ROOT / "src/memory/README.md",
        ROOT / "runtime/AGENTS.md",
        ROOT / "runtime/README.md",
        ROOT / "src/runtime/AGENTS.md",
        ROOT / "src/runtime/README.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == [], f"Missing operational branch docs: {missing}"


def test_interaction_and_data_branch_docs_exist():
    required = [
        ROOT / "frontend/AGENTS.md",
        ROOT / "frontend/README.md",
        ROOT / "agent/AGENTS.md",
        ROOT / "agent/README.md",
        ROOT / "data/AGENTS.md",
        ROOT / "data/README.md",
        ROOT / "artifacts/AGENTS.md",
        ROOT / "artifacts/README.md",
    ]
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    assert missing == [], f"Missing interaction/data branch docs: {missing}"


def test_repo_scope_map_is_strictly_valid():
    scope_map_path = ROOT / "SCOPE_MAP.yaml"
    errors = validate_scope_map(scope_map_path, ROOT, check_paths=True)
    assert errors == [], f"Strict scope-map validation failed: {errors}"


if __name__ == "__main__":
    test_dir = Path(tempfile.mkdtemp(prefix="scope-map-tests-"))
    test_resolve_scope_alias_and_fallback(test_dir / "alias")
    test_validate_scope_map_reports_missing_paths(test_dir / "missing")
    test_root_handoff_files_exist()
    test_scope_map_has_required_scopes_without_path_checks()
    test_knowledge_branch_docs_exist()
    test_operational_branch_docs_exist()
    test_interaction_and_data_branch_docs_exist()
    test_repo_scope_map_is_strictly_valid()
    print("scope-map tests passed")
