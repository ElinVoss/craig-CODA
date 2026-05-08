"""pulse.py — Craig-CODA client heartbeat loop.

Runs on the client machine. Each pulse cycle:
  1. Probes LM Studio server (192.168.4.25:1234).
  2. Runs the async vault indexer (if not recently run).
  3. Logs a heartbeat entry to .coda/pulse.log.
  4. Sleeps until the next cycle.

This loop maintains client-side cognition regardless of server state.
Server inference is an accelerator; the pulse continues without it.

Usage:
    python scripts/pulse.py               # runs forever
    python scripts/pulse.py --once        # single cycle, then exit
    python scripts/pulse.py --interval 60 # override cycle interval (seconds)

Environment variables:
    CODA_PULSE_INTERVAL_SECS  — cycle interval (default 300)
    CODA_STATE_DIR            — .coda state dir (default D:\\craig-CODA\\.coda)
    LMSTUDIO_SERVER           — server base URL (default http://192.168.4.25:1234)
    PROJECT_ROOT              — repo root (default D:\\craig-CODA)
"""
from __future__ import annotations

import argparse
import datetime
import os
import subprocess
import sys
import time
import urllib.request

# ── Paths ─────────────────────────────────────────────────────────────────────
_HERE        = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get("PROJECT_ROOT", os.path.dirname(_HERE))
CODA_DIR     = os.environ.get("CODA_STATE_DIR", os.path.join(PROJECT_ROOT, ".coda"))
PULSE_LOG    = os.path.join(CODA_DIR, "pulse.log")
SERVER_URL   = os.environ.get("LMSTUDIO_SERVER", "http://192.168.4.25:1234")
INTERVAL     = int(os.environ.get("CODA_PULSE_INTERVAL_SECS", "300"))
PYTHON       = sys.executable


# ── Utilities ─────────────────────────────────────────────────────────────────
def _log(message: str) -> None:
    ts = datetime.datetime.now().isoformat(timespec="seconds")
    line = f"[{ts}] {message}"
    print(line, flush=True)
    os.makedirs(CODA_DIR, exist_ok=True)
    with open(PULSE_LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def _probe_server() -> bool:
    """Return True if LM Studio server is reachable."""
    try:
        req = urllib.request.Request(
            SERVER_URL.rstrip("/") + "/v1/models",
            headers={"Authorization": "Bearer lm-studio"},
        )
        urllib.request.urlopen(req, timeout=3)
        return True
    except Exception:
        return False


def _run_indexer() -> str:
    """Run the async vault indexer (one-shot) and return status line."""
    indexer = os.path.join(PROJECT_ROOT, "scripts", "run_async_indexer.py")
    if not os.path.exists(indexer):
        return "indexer not found — skipped"
    try:
        result = subprocess.run(
            [PYTHON, indexer, "--once"],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=PROJECT_ROOT,
        )
        if result.returncode == 0:
            return "indexer: OK"
        return f"indexer: exit {result.returncode} — {result.stderr.strip()[:120]}"
    except subprocess.TimeoutExpired:
        return "indexer: timeout (120s)"
    except Exception as exc:
        return f"indexer: error — {exc}"


# ── Single pulse cycle ─────────────────────────────────────────────────────────
def pulse_once() -> None:
    server_online = _probe_server()
    server_status = "ONLINE" if server_online else "OFFLINE"
    indexer_status = _run_indexer()
    _log(f"PULSE  server={server_status}  {indexer_status}")


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    parser = argparse.ArgumentParser(description="Craig-CODA heartbeat pulse loop")
    parser.add_argument("--once",     action="store_true", help="Run one cycle and exit")
    parser.add_argument("--interval", type=int, default=INTERVAL, help="Cycle interval in seconds")
    args = parser.parse_args()

    _log(f"PULSE START  server={SERVER_URL}  interval={args.interval}s  state={CODA_DIR}")

    if args.once:
        pulse_once()
        return

    while True:
        try:
            pulse_once()
        except Exception as exc:
            _log(f"PULSE ERROR  {exc}")
        time.sleep(args.interval)


if __name__ == "__main__":
    main()
