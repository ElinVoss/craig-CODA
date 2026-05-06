"""
Corpus Tokenization Pipeline

Runs three tokenizers over the extracted message corpus and reports stats.

Tokenizers:
  1. sentence-transformers / bert-base (local, already installed)
  2. tiktoken cl100k_base (GPT-4 encoding, fast, no download)
  3. Qwen3-4B HuggingFace tokenizer (downloads tokenizer files ~a few MB, not weights)

Usage:
    python scripts/tokenize_corpus.py
    python scripts/tokenize_corpus.py --corpus data/raw/messages/corpus.txt
    python scripts/tokenize_corpus.py --corpus data/raw/messages/craig_sent.txt
    python scripts/tokenize_corpus.py --out data/raw/messages/token_stats.json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

DEFAULT_CORPUS = Path("data/raw/messages/corpus.txt")
QWEN_MODEL_ID = "Qwen/Qwen3-4B"


def _lines(corpus_path: Path) -> list[str]:
    return [l.strip() for l in corpus_path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _stats(name: str, token_counts: list[int], texts: list[str]) -> dict:
    total_chars = sum(len(t) for t in texts)
    total_tokens = sum(token_counts)
    avg = total_tokens / max(len(token_counts), 1)
    p50 = sorted(token_counts)[len(token_counts) // 2] if token_counts else 0
    p95 = sorted(token_counts)[int(len(token_counts) * 0.95)] if token_counts else 0
    return {
        "tokenizer": name,
        "messages": len(texts),
        "total_chars": total_chars,
        "total_tokens": total_tokens,
        "chars_per_token": round(total_chars / max(total_tokens, 1), 3),
        "avg_tokens_per_message": round(avg, 1),
        "median_tokens_per_message": p50,
        "p95_tokens_per_message": p95,
        "max_tokens": max(token_counts) if token_counts else 0,
    }


def run_sentence_transformers(texts: list[str]) -> dict:
    """Use the bert-base tokenizer bundled with sentence-transformers."""
    from transformers import AutoTokenizer
    print("  Loading sentence-transformers tokenizer (bert-base-uncased)...")
    tok = AutoTokenizer.from_pretrained("bert-base-uncased")
    counts = [len(tok.encode(t, add_special_tokens=False)) for t in texts]
    return _stats("sentence-transformers/bert-base-uncased", counts, texts)


def run_tiktoken(texts: list[str]) -> dict:
    """Use tiktoken cl100k_base (same encoding as GPT-4 / Claude)."""
    import tiktoken
    print("  Loading tiktoken cl100k_base...")
    enc = tiktoken.get_encoding("cl100k_base")
    counts = [len(enc.encode(t)) for t in texts]
    return _stats("tiktoken/cl100k_base", counts, texts)


def run_qwen3(texts: list[str]) -> dict:
    """Download and use the Qwen3-4B tokenizer from HuggingFace (tokenizer only, not weights)."""
    from transformers import AutoTokenizer
    print(f"  Loading Qwen3-4B tokenizer from HuggingFace ({QWEN_MODEL_ID})...")
    print("  (Downloads tokenizer files only — ~a few MB. Weights are NOT downloaded.)")
    tok = AutoTokenizer.from_pretrained(QWEN_MODEL_ID, trust_remote_code=True)
    counts = [len(tok.encode(t, add_special_tokens=False)) for t in texts]
    return _stats(f"HuggingFace/{QWEN_MODEL_ID}", counts, texts)


def print_stats(result: dict) -> None:
    print(f"\n  Tokenizer:               {result['tokenizer']}")
    print(f"  Messages:                {result['messages']:,}")
    print(f"  Total tokens:            {result['total_tokens']:,}")
    print(f"  Total chars:             {result['total_chars']:,}")
    print(f"  Chars per token:         {result['chars_per_token']}")
    print(f"  Avg tokens/message:      {result['avg_tokens_per_message']}")
    print(f"  Median tokens/message:   {result['median_tokens_per_message']}")
    print(f"  P95 tokens/message:      {result['p95_tokens_per_message']}")
    print(f"  Max tokens (single msg): {result['max_tokens']}")


def main() -> None:
    p = argparse.ArgumentParser(description="Tokenize message corpus with three tokenizers.")
    p.add_argument("--corpus", default=str(DEFAULT_CORPUS), help="Path to corpus .txt file")
    p.add_argument("--out", default=None, help="Write JSON stats to this path")
    p.add_argument("--skip-qwen", action="store_true", help="Skip HuggingFace download (offline)")
    args = p.parse_args()

    corpus_path = Path(args.corpus)
    if not corpus_path.exists():
        print(f"ERROR: corpus not found at {corpus_path}", file=sys.stderr)
        print("Run scripts/extract_messages.py first.", file=sys.stderr)
        sys.exit(1)

    texts = _lines(corpus_path)
    print(f"Corpus: {corpus_path} ({len(texts):,} messages)")
    print("=" * 60)

    results = []

    print("\n[1/3] sentence-transformers tokenizer")
    try:
        r = run_sentence_transformers(texts)
        print_stats(r)
        results.append(r)
    except Exception as e:
        print(f"  FAILED: {e}")

    print("\n[2/3] tiktoken cl100k_base")
    try:
        r = run_tiktoken(texts)
        print_stats(r)
        results.append(r)
    except Exception as e:
        print(f"  FAILED: {e}")

    if not args.skip_qwen:
        print(f"\n[3/3] Qwen3-4B HuggingFace tokenizer")
        try:
            r = run_qwen3(texts)
            print_stats(r)
            results.append(r)
        except Exception as e:
            print(f"  FAILED: {e}")
    else:
        print("\n[3/3] Qwen3-4B — skipped (--skip-qwen)")

    print("\n" + "=" * 60)
    print("Summary (chars per token -- higher = more efficient compression):")
    for r in results:
        bar = "#" * int(r["chars_per_token"] * 10)
        name = r["tokenizer"].split("/")[-1]
        print(f"  {name:<30} {r['chars_per_token']:5.2f}  {bar}")

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(results, indent=2), encoding="utf-8")
        print(f"\nStats written: {out_path}")


if __name__ == "__main__":
    main()
