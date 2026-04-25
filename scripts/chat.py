"""
Craig CODA — interactive chat CLI.

Usage:
    python scripts/chat.py
    python scripts/chat.py --model dolphin-llama3 --show-context
    python scripts/chat.py --db artifacts/episodic/memory.db

Commands during chat:
    /reset     — clear conversation history
    /context   — toggle showing retrieved memory nodes
    /quit      — exit
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))


def main():
    ap = argparse.ArgumentParser(description="Craig CODA interactive chat")
    ap.add_argument("--model", default="dolphin-llama3", help="Ollama model name")
    ap.add_argument("--db", default="artifacts/episodic/memory.db", help="Episodic DB path")
    ap.add_argument("--show-context", action="store_true", help="Print retrieved memory nodes each turn")
    args = ap.parse_args()

    from src.runtime.ollama_client import is_running
    if not is_running():
        print("Ollama is not running. Start it with: ollama serve")
        sys.exit(1)

    from src.runtime.coda import CodaRuntime
    coda = CodaRuntime(
        db_path=ROOT / args.db,
        model=args.model,
    )

    show_context = args.show_context

    print(f"\nCraig CODA — {args.model}")
    print("Commands: /reset  /context  /quit")
    print("-" * 40)

    while True:
        try:
            user_input = input("\nyou: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not user_input:
            continue

        if user_input == "/quit":
            break
        elif user_input == "/reset":
            coda.reset()
            print("[history cleared]")
            continue
        elif user_input == "/context":
            show_context = not show_context
            print(f"[context display: {'on' if show_context else 'off'}]")
            continue

        print("\ncoda: ", end="", flush=True)
        try:
            for chunk in coda.chat(user_input, show_context=show_context):
                print(chunk, end="", flush=True)
        except Exception as e:
            print(f"\n[error: {e}]")
        print()


if __name__ == "__main__":
    main()
