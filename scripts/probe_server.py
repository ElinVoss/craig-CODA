"""probe_server.py — Test connectivity to the LM Studio server.

Usage:
    python scripts/probe_server.py              # uses LMSTUDIO_SERVER env var
    python scripts/probe_server.py --url http://192.168.4.25:1234

Exit codes:
    0  — server reachable and ready
    1  — server unreachable or not responding

Designed to be called by pulse.py and startup scripts.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request


def probe(base_url: str, timeout: int = 3) -> tuple[bool, str]:
    """Return (reachable, message)."""
    url = base_url.rstrip("/") + "/v1/models"
    try:
        req = urllib.request.Request(url, headers={"Authorization": "Bearer lm-studio"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read())
            models = [m.get("id", "?") for m in data.get("data", [])]
            model_str = ", ".join(models) if models else "(no models listed)"
            return True, f"OK — models: {model_str}"
    except Exception as exc:
        return False, str(exc)


def main() -> None:
    parser = argparse.ArgumentParser(description="Probe LM Studio server connectivity")
    parser.add_argument(
        "--url",
        default=os.environ.get("LMSTUDIO_SERVER", "http://192.168.4.25:1234"),
        help="LM Studio base URL (default: LMSTUDIO_SERVER env var or http://192.168.4.25:1234)",
    )
    parser.add_argument("--timeout", type=int, default=3, help="Probe timeout in seconds")
    parser.add_argument("--quiet", action="store_true", help="Suppress output (use exit code only)")
    args = parser.parse_args()

    reachable, message = probe(args.url, args.timeout)

    if not args.quiet:
        status = "ONLINE " if reachable else "OFFLINE"
        print(f"[probe] {args.url}  →  {status}  {message}")

    sys.exit(0 if reachable else 1)


if __name__ == "__main__":
    main()
