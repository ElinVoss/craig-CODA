"""
Craig session management — SESSION START / SESSION CLOSE protocol.

Enforces the structured session workflow derived from the OmniMeta MasterMind protocol:
  1. Load knowledge index and verify foundation SHA pins
  2. Set active frame policy for current stage
  3. Execute task
  4. Record outputs and advance state
  5. Emit CONTINUE FROM directive

Usage:
    from src.runtime.session import Session

    session = Session(project_root=Path("projects/my_project"))
    session.start(task="Generate output N03", stage="phase_2")
    # ... do work ...
    session.close(outputs_created=["04_Outputs/bibles/N03_title.md"])
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class Session:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.index_path = project_root / "knowledge_index.json"
        self.ledger_path = project_root / "05_Continuity" / "hashes" / "foundation.sha256.txt"
        self.stage: str | None = None
        self.task: str | None = None
        self.started_at: datetime | None = None
        self._index: dict[str, Any] = {}

    # ------------------------------------------------------------------
    # SESSION START
    # ------------------------------------------------------------------

    def start(self, task: str, stage: str) -> dict[str, Any]:
        """
        Load knowledge index, verify foundation SHA pins, set active stage.
        Returns the session header dict for logging/display.
        """
        self.task = task
        self.stage = stage
        self.started_at = datetime.now(timezone.utc)

        self._index = self._load_index()
        integrity = self._verify_foundation()

        header = {
            "event": "SESSION START",
            "knowledge_index_sha": self._index.get("_meta", {}).get("commit_sha", "unknown"),
            "foundation_verified": integrity["ok"],
            "foundation_failures": integrity["failures"],
            "active_stage": stage,
            "task": task,
            "started_at": self.started_at.isoformat(),
        }

        if not integrity["ok"]:
            raise RuntimeError(
                f"Foundation integrity check failed for {len(integrity['failures'])} node(s). "
                f"Halt before proceeding.\n{integrity['failures']}"
            )

        self._print_header(header)
        return header

    # ------------------------------------------------------------------
    # SESSION CLOSE
    # ------------------------------------------------------------------

    def close(self, outputs_created: list[str], next_task: str = "") -> dict[str, Any]:
        """
        Record outputs created, emit CONTINUE FROM directive.
        """
        closed_at = datetime.now(timezone.utc)

        summary = {
            "event": "SESSION COMPLETE",
            "files_created": outputs_created,
            "stage": self.stage,
            "task": self.task,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "closed_at": closed_at.isoformat(),
            "continue_from": next_task or "— not set —",
        }

        self._print_close(summary)
        return summary

    # ------------------------------------------------------------------
    # FOUNDATION INTEGRITY
    # ------------------------------------------------------------------

    def _verify_foundation(self) -> dict[str, Any]:
        """
        Re-hash all foundation nodes and compare against SHA pins in knowledge_index.json.
        Returns dict with ok: bool and list of failures.
        """
        failures = []
        nodes = self._index.get("nodes", [])

        for node in nodes:
            if node.get("layer") != "foundation":
                continue
            sha_pin = node.get("sha_pin", "")
            if not sha_pin or sha_pin.startswith("{{"):
                continue  # template placeholder — skip

            file_path = self.project_root / node["path"]
            if not file_path.exists():
                failures.append({"id": node["id"], "reason": "file not found", "path": str(file_path)})
                continue

            actual_sha = hashlib.sha256(file_path.read_bytes()).hexdigest()
            if actual_sha != sha_pin:
                failures.append({
                    "id": node["id"],
                    "reason": "sha mismatch",
                    "expected": sha_pin,
                    "actual": actual_sha,
                    "path": str(file_path),
                })

        return {"ok": len(failures) == 0, "failures": failures}

    # ------------------------------------------------------------------
    # CONTEXT CHAIN
    # ------------------------------------------------------------------

    def get_context_chain(self, output_type: str, current_sequence_n: int) -> list[dict]:
        """
        Returns all previous output nodes of the given type, ordered by sequence_n.
        Inject these as context before generating the current output unit.
        """
        nodes = self._index.get("nodes", [])
        chain = [
            n for n in nodes
            if n.get("layer") == "output"
            and n.get("sequence_n", 0) < current_sequence_n
        ]
        return sorted(chain, key=lambda n: n.get("sequence_n", 0))

    # ------------------------------------------------------------------
    # ALLOWED NODES FOR CURRENT STAGE
    # ------------------------------------------------------------------

    def get_allowed_nodes(self, frame_policy: dict | None = None) -> list[dict]:
        """
        Returns nodes permitted for the current stage, applying frame access policy.
        """
        from src.runtime.frame_policy import FramePolicy

        policy = FramePolicy(self.project_root / "configs" / "frame_access_policy.yaml")
        allowed_frames = policy.allowed_frames(self.stage or "")

        nodes = self._index.get("nodes", [])
        return [
            n for n in nodes
            if n.get("frame") == "universal" or n.get("frame") in allowed_frames
        ]

    # ------------------------------------------------------------------
    # INTERNAL
    # ------------------------------------------------------------------

    def _load_index(self) -> dict[str, Any]:
        if not self.index_path.exists():
            raise FileNotFoundError(f"knowledge_index.json not found at {self.index_path}")
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def _print_header(self, header: dict) -> None:
        print("\n" + "=" * 60)
        print("[SESSION START]")
        print(f"  Knowledge index SHA : {header['knowledge_index_sha']}")
        print(f"  Foundation verified : {header['foundation_verified']}")
        print(f"  Active stage        : {header['active_stage']}")
        print(f"  Task                : {header['task']}")
        print("=" * 60 + "\n")

    def _print_close(self, summary: dict) -> None:
        print("\n" + "=" * 60)
        print("[SESSION COMPLETE]")
        print("Files created:")
        for f in summary["files_created"]:
            print(f"  • {f}")
        print(f"\nCONTINUE FROM: {summary['continue_from']}")
        print("=" * 60 + "\n")
