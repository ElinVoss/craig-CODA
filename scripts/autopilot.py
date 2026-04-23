"""
autopilot.py — Fully unattended pipeline runner.

Converts all pending OpenAI books one at a time, then after each one:
  1. Cleans the output
  2. Rebuilds the corpus
  3. Retrains the tokenizer
  4. If training has finished, starts a new 2000-step run from the latest checkpoint

Run once and leave it. Safe to interrupt and re-run — everything resumes.

Usage:
    python scripts/autopilot.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = str(ROOT / ".venv" / "Scripts" / "python.exe")
TRAINING_PID_FILE = ROOT / "artifacts" / "checkpoints" / "tiny-qwen3-scratch" / "training.pid"
LOG_FILE = ROOT / "logs" / "autopilot.log"


def log(msg: str) -> None:
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    log(f"RUN: {' '.join(args)}")
    result = subprocess.run(args, cwd=str(ROOT))
    if check and result.returncode != 0:
        log(f"FAILED (exit {result.returncode}): {' '.join(args)}")
        raise RuntimeError(f"Command failed: {' '.join(args)}")
    return result


def pending_books() -> list[str]:
    """Return book IDs (openai or groq) that haven't been fully converted yet."""
    import yaml
    config = yaml.safe_load((ROOT / "configs" / "voice_conversion.yaml").read_text(encoding="utf-8"))
    output_dir = ROOT / config["output_dir"]

    pending = []
    for book in config["books"]:
        if book["provider"] not in ("openai", "groq"):
            continue
        final = output_dir / f"{book['id']}.txt"
        if final.exists():
            continue
        pending.append(book["id"])
    return pending


def training_is_running() -> bool:
    """Check if a training process is still active."""
    if not TRAINING_PID_FILE.exists():
        return False
    try:
        pid = int(TRAINING_PID_FILE.read_text().strip())
        # On Windows, check if process exists
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            capture_output=True, text=True
        )
        return str(pid) in result.stdout
    except Exception:
        return False


def latest_checkpoint() -> Path | None:
    ckpt_root = ROOT / "artifacts" / "checkpoints" / "tiny-qwen3-scratch"
    dirs = sorted([d for d in ckpt_root.iterdir() if d.is_dir() and d.name.startswith("step_")])
    return dirs[-1] if dirs else None


def start_training(resume_from: Path) -> None:
    log(f"Starting new training run from {resume_from.name}")
    proc = subprocess.Popen(
        [PYTHON, "scripts/run_scratch_train.py", "--resume", str(resume_from)],
        cwd=str(ROOT)
    )
    TRAINING_PID_FILE.write_text(str(proc.pid))
    log(f"Training started (PID {proc.pid})")


def rebuild_pipeline() -> None:
    log("--- Cleaning converted texts ---")
    run([PYTHON, "scripts/clean_text.py",
         "--ingest-root", "data/raw/converted",
         "--clean-root", "data/clean/converted"])

    log("--- Rebuilding corpus ---")
    run([PYTHON, "scripts/prepare_corpus.py"])

    log("--- Retraining tokenizer ---")
    run([PYTHON, "scripts/train_tokenizer.py"])
    log("--- Pipeline rebuild complete ---")


def main() -> int:
    has_openai = bool(os.environ.get("OPENAI_API_KEY"))
    has_groq   = bool(os.environ.get("GROQ_API_KEY"))
    if not has_openai and not has_groq:
        log("ERROR: Set OPENAI_API_KEY or GROQ_API_KEY before running autopilot.")
        return 1

    log("=== AUTOPILOT STARTED ===")

    while True:
        books = pending_books()

        if not books:
            log("All books converted.")
            break

        book_id = books[0]
        log(f"Converting: {book_id} ({len(books)} remaining after this)")

        try:
            run([PYTHON, "scripts/convert_to_voice.py", "--book", book_id])
        except RuntimeError:
            log(f"Conversion failed for {book_id} — skipping and continuing")
            time.sleep(10)
            continue

        # Rebuild corpus + tokenizer after each book
        try:
            rebuild_pipeline()
        except RuntimeError as e:
            log(f"Pipeline rebuild failed: {e} — continuing anyway")

        # If training finished, start a new run
        if not training_is_running():
            ckpt = latest_checkpoint()
            if ckpt:
                log(f"Training not running. Starting new run from {ckpt.name}")
                start_training(ckpt)
            else:
                log("No checkpoint found — skipping training restart")

        time.sleep(5)

    log("=== AUTOPILOT COMPLETE ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
