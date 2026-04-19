from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_step(title: str, command: list[str]) -> None:
    print(f"==> {title}", flush=True)
    result = subprocess.run(command, cwd=ROOT)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the local data pipeline end to end.")
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()

    py = args.python
    run_step("Ingest raw files", [py, "scripts/ingest_raw.py"])
    run_step("Clean staged text", [py, "scripts/clean_text.py"])
    run_step("Build datasets", [py, "scripts/build_datasets.py"])
    run_step("Validate outputs", [py, "scripts/validate_data.py"])
    print("Pipeline complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
