"""
Frame access policy — gates which entity frames are queryable at each project stage.

Reads configs/frame_access_policy.yaml and returns the set of allowed frame IDs
for a given stage. Used by session.py and the episodic retriever.

Usage:
    from src.runtime.frame_policy import FramePolicy
    from pathlib import Path

    policy = FramePolicy(Path("projects/my_project/configs/frame_access_policy.yaml"))
    allowed = policy.allowed_frames(stage="phase_2")
    # allowed = {"public", "internal"}
"""
from __future__ import annotations

from pathlib import Path
import yaml


class FramePolicy:
    def __init__(self, policy_path: Path):
        if not policy_path.exists():
            raise FileNotFoundError(f"Frame access policy not found: {policy_path}")
        self._raw = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
        self._stages = {s["id"]: s for s in self._raw.get("stages", [])}
        self._frames = self._raw.get("frames", [])
        self._default_stage = self._raw.get("defaults", {}).get("active_stage", "")
        self._deny_unlisted = self._raw.get("defaults", {}).get("deny_unlisted", True)

    def allowed_frames(self, stage: str) -> set[str]:
        """
        Returns the set of frame IDs accessible at the given stage.
        Frames with allowed_stages: ["*"] are always included.
        """
        # Validate stage exists
        if stage and stage not in self._stages:
            raise ValueError(
                f"Unknown stage '{stage}'. Valid stages: {list(self._stages.keys())}"
            )

        active = stage or self._default_stage
        allowed: set[str] = set()

        for frame in self._frames:
            frame_id = frame.get("id", "")
            if not frame_id or frame_id.startswith("{{"):
                continue  # template placeholder — skip

            allowed_stages = frame.get("allowed_stages", [])

            if "*" in allowed_stages:
                allowed.add(frame_id)
            elif active in allowed_stages:
                allowed.add(frame_id)

        return allowed

    def is_frame_allowed(self, frame_id: str, stage: str) -> bool:
        return frame_id in self.allowed_frames(stage)

    def unlock_message(self, frame_id: str) -> str | None:
        """Returns the unlock message for a frame, if defined."""
        for frame in self._frames:
            if frame.get("id") == frame_id:
                return frame.get("unlock_message")
        return None

    def current_stage_sequence(self, stage: str) -> int:
        """Returns the numeric sequence of a stage for ordering."""
        s = self._stages.get(stage, {})
        return s.get("sequence", 0)

    def stages_before(self, stage: str) -> list[str]:
        """Returns all stage IDs with sequence < current stage."""
        current_seq = self.current_stage_sequence(stage)
        return [
            sid for sid, s in self._stages.items()
            if s.get("sequence", 0) < current_seq
        ]
