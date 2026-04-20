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
    parser = argparse.ArgumentParser(description="Run the local corpus-prep and tokenizer pipeline.")
    parser.add_argument("--python", default=sys.executable)
    args = parser.parse_args()

    py = args.python
    run_step("Prepare corpus", [py, "scripts/prepare_corpus.py"])
    run_step("Train tokenizer", [py, "scripts/train_tokenizer.py"])
    run_step("Inspect tokenizer", [py, "scripts/inspect_tokenizer.py"])
    run_step("Validate outputs", [py, "scripts/validate_data.py"])
    print("Tokenizer pipeline complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

