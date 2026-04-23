from __future__ import annotations

from pathlib import Path

import torch

from .io_utils import write_json


def save_checkpoint(model, tokenizer, optimizer, output_dir: Path, trainer_state: dict) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    model.save_pretrained(output_dir, safe_serialization=True)
    tokenizer.save_pretrained(output_dir)
    torch.save(optimizer.state_dict(), output_dir / "optimizer.pt")
    write_json(output_dir / "trainer_state.json", trainer_state)
    return output_dir


def list_checkpoint_dirs(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted([path for path in root.iterdir() if path.is_dir()])


def latest_checkpoint(root: Path) -> Path | None:
    checkpoints = list_checkpoint_dirs(root)
    if not checkpoints:
        return None
    return checkpoints[-1]


def trim_old_checkpoints(root: Path, keep_last: int) -> None:
    checkpoints = list_checkpoint_dirs(root)
    for path in checkpoints[:-keep_last]:
        for child in path.rglob("*"):
            if child.is_file():
                child.unlink()
        for child in sorted(path.rglob("*"), reverse=True):
            if child.is_dir():
                child.rmdir()
        path.rmdir()

