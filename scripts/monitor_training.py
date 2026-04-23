"""
Live training monitor — reads training_log.jsonl and renders a refreshing
ASCII dashboard in the terminal.

Usage:
    python scripts/monitor_training.py
    python scripts/monitor_training.py --interval 5
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG_PATH = ROOT / "artifacts" / "checkpoints" / "tiny-qwen3-scratch" / "training_log.jsonl"
CHECKPOINT_DIR = ROOT / "artifacts" / "checkpoints" / "tiny-qwen3-scratch"


def read_log(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    entries.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return entries


def sparkline(values: list[float], width: int = 40) -> str:
    if not values:
        return "-" * width
    bars = "▁▂▃▄▅▆▇█"
    lo, hi = min(values), max(values)
    span = hi - lo or 1
    # sample down to width
    if len(values) > width:
        step = len(values) / width
        values = [values[int(i * step)] for i in range(width)]
    chars = [bars[int((v - lo) / span * (len(bars) - 1))] for v in values]
    return "".join(chars)


def progress_bar(step: int, max_steps: int, width: int = 40) -> str:
    pct = step / max_steps
    filled = int(pct * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {step}/{max_steps} ({pct*100:.1f}%)"


def latest_checkpoints() -> list[str]:
    dirs = sorted(CHECKPOINT_DIR.glob("step_*"))
    return [d.name for d in dirs]


def clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def render(entries: list[dict]) -> None:
    clear()
    print("=" * 56)
    print("  MODEL LAB — TRAINING MONITOR")
    print("=" * 56)

    if not entries:
        print("\n  Waiting for training to start...")
        print(f"  Watching: {LOG_PATH}")
        return

    last = entries[-1]
    step = last["step"]
    max_steps = last.get("max_steps", 2000)
    loss = last["loss"]
    losses = [e["loss"] for e in entries]
    avg = sum(losses) / len(losses)
    best = min(losses)

    print(f"\n  Progress:  {progress_bar(step, max_steps)}")
    print(f"\n  Loss now:  {loss:.4f}")
    print(f"  Best:      {best:.4f}   Avg: {avg:.4f}")

    # sparkline — invert so high loss = tall bar visually makes sense
    # actually show loss going DOWN as graph goes down (use raw values, high=start)
    spark = sparkline(losses)
    print(f"\n  Loss curve (left=early, right=now):")
    print(f"  hi {losses[0]:.2f} |{spark}| {loss:.2f} lo")

    ckpts = latest_checkpoints()
    print(f"\n  Checkpoints saved: {len(ckpts)}")
    for c in ckpts[-3:]:
        print(f"    · {c}")

    print(f"\n  Log entries: {len(entries)}   Last update: {time.strftime('%H:%M:%S')}")
    print("\n  [Ctrl+C to exit monitor — training continues in background]")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--interval", type=float, default=10,
                        help="Refresh interval in seconds (default: 10)")
    parser.add_argument("--once", action="store_true",
                        help="Print once and exit (no live loop)")
    args = parser.parse_args()

    if args.once:
        render(read_log(LOG_PATH))
        return

    print(f"Monitoring {LOG_PATH} — refreshing every {args.interval}s  (Ctrl+C to stop)")
    try:
        while True:
            entries = read_log(LOG_PATH)
            render(entries)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nMonitor stopped. Training continues in background.")


if __name__ == "__main__":
    main()
