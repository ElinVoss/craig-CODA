"""
convert_to_voice.py — Download public domain texts from Project Gutenberg
and rewrite them into Craig Ramos's voice using the style conversion prompt.

Supports Anthropic (Claude), OpenAI (GPT-4o), and Groq (Llama) providers.
Groq uses parallel chunk processing for maximum throughput.
Has full resume capability — interrupted runs pick up where they left off.

Usage:
    python scripts/convert_to_voice.py
    python scripts/convert_to_voice.py --book moby_dick
    python scripts/convert_to_voice.py --list
    python scripts/convert_to_voice.py --reset moby_dick
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

CONFIG_PATH = ROOT / "configs" / "voice_conversion.yaml"
STYLE_PROMPT_PATH = ROOT / "exports" / "voice" / "style_conversion_prompt.md"


# ---------------------------------------------------------------------------
# Style prompt extraction
# ---------------------------------------------------------------------------

def load_system_prompt(path: Path) -> str:
    """Extract the SYSTEM PROMPT block from the style conversion markdown."""
    text = path.read_text(encoding="utf-8")
    match = re.search(r"## SYSTEM PROMPT\s*\n(.*?)(?=\n## |\Z)", text, re.DOTALL)
    if not match:
        raise ValueError(f"Could not find '## SYSTEM PROMPT' block in {path}")
    return match.group(1).strip()


# ---------------------------------------------------------------------------
# Gutenberg download + cleanup
# ---------------------------------------------------------------------------

GUTENBERG_HEADER_RE = re.compile(
    r"\*{3}\s*START OF (THE |THIS )?PROJECT GUTENBERG.*?\*{3}", re.DOTALL | re.IGNORECASE
)
GUTENBERG_FOOTER_RE = re.compile(
    r"\*{3}\s*END OF (THE |THIS )?PROJECT GUTENBERG.*", re.DOTALL | re.IGNORECASE
)

def download_gutenberg(url: str, retries: int = 3) -> str:
    """Download a Gutenberg text file with retry logic."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; craig-coda-research/1.0)"}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            if attempt < retries - 1:
                print(f"  [retry {attempt+1}] {e}")
                time.sleep(3)
            else:
                raise


def strip_gutenberg_boilerplate(text: str) -> str:
    """Remove Project Gutenberg header and footer."""
    # Remove header (everything up to and including the START line)
    header_match = GUTENBERG_HEADER_RE.search(text)
    if header_match:
        text = text[header_match.end():]

    # Remove footer (everything from END line onward)
    footer_match = GUTENBERG_FOOTER_RE.search(text)
    if footer_match:
        text = text[:footer_match.start()]

    return text.strip()


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------

def chunk_text(text: str, target_words: int = 700) -> list[str]:
    """Split text into chunks of approximately target_words words,
    breaking on paragraph boundaries where possible."""
    paragraphs = re.split(r"\n\s*\n", text)
    chunks: list[str] = []
    current: list[str] = []
    current_words = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        word_count = len(para.split())
        if current_words + word_count > target_words and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_words = word_count
        else:
            current.append(para)
            current_words += word_count

    if current:
        chunks.append("\n\n".join(current))

    return chunks


# ---------------------------------------------------------------------------
# API calls
# ---------------------------------------------------------------------------

def convert_chunk_anthropic(chunk: str, system_prompt: str, model: str, retries: int = 3) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    user_msg = (
        "Rewrite the following text in Craig's voice. Match the appropriate register "
        "(casual / directive / reflective-technical) based on the content. "
        "Do not explain your choices — just deliver the rewrite.\n\n" + chunk
    )
    for attempt in range(retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                system=system_prompt,
                messages=[{"role": "user", "content": user_msg}],
            )
            return response.content[0].text.strip()
        except Exception as e:
            if attempt < retries - 1:
                print(f"    [retry {attempt+1}] Anthropic error: {e}")
                time.sleep(5)
            else:
                raise


def convert_chunk_openai(chunk: str, system_prompt: str, model: str, retries: int = 6) -> str:
    import openai
    client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    user_msg = (
        "Rewrite the following text in Craig's voice. Match the appropriate register "
        "(casual / directive / reflective-technical) based on the content. "
        "Do not explain your choices — just deliver the rewrite.\n\n" + chunk
    )
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=2048,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            name = type(e).__name__
            is_rate_limit = "RateLimit" in name or "429" in str(e)
            if is_rate_limit:
                # Parse suggested wait time from error message if present
                match = re.search(r"try again in (\d+(?:\.\d+)?)(ms|s)", str(e))
                if match:
                    val, unit = float(match.group(1)), match.group(2)
                    suggested = val / 1000 if unit == "ms" else val
                else:
                    suggested = 2 ** attempt
                wait = max(suggested + 1, 2 ** attempt)
            else:
                wait = 5
            if attempt < retries - 1:
                print(f"    [retry {attempt+1}] {name} — wait {wait:.1f}s", flush=True)
                time.sleep(wait)
            else:
                raise


def convert_chunk_groq(chunk: str, system_prompt: str, model: str, retries: int = 6) -> str:
    from groq import Groq
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
    user_msg = (
        "Rewrite the following text in Craig's voice. Match the appropriate register "
        "(casual / directive / reflective-technical) based on the content. "
        "Do not explain your choices — just deliver the rewrite.\n\n" + chunk
    )
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_msg},
                ],
                max_tokens=2048,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            name = type(e).__name__
            is_rate_limit = "RateLimit" in name or "429" in str(e)
            wait = (2 ** attempt) if is_rate_limit else 5
            if attempt < retries - 1:
                print(f"    [retry {attempt+1}] {name} — wait {wait}s", flush=True)
                time.sleep(wait)
            else:
                raise


def convert_chunk(chunk: str, system_prompt: str, provider: str, model: str, retries: int = 3) -> str:
    if provider == "anthropic":
        return convert_chunk_anthropic(chunk, system_prompt, model, retries)
    elif provider == "openai":
        return convert_chunk_openai(chunk, system_prompt, model, retries)
    elif provider == "groq":
        return convert_chunk_groq(chunk, system_prompt, model, retries)
    else:
        raise ValueError(f"Unknown provider: {provider}")


# ---------------------------------------------------------------------------
# Progress tracking
# ---------------------------------------------------------------------------

def load_progress(progress_file: Path) -> dict[str, set[int]]:
    """Load completed chunk indices per book."""
    done: dict[str, set[int]] = {}
    if not progress_file.exists():
        return done
    with open(progress_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                entry = json.loads(line)
                book_id = entry["book_id"]
                done.setdefault(book_id, set()).add(entry["chunk_index"])
    return done


def record_progress(progress_file: Path, book_id: str, chunk_index: int) -> None:
    with open(progress_file, "a", encoding="utf-8") as f:
        f.write(json.dumps({"book_id": book_id, "chunk_index": chunk_index}) + "\n")


def reset_progress(progress_file: Path, book_id: str) -> None:
    if not progress_file.exists():
        return
    lines = progress_file.read_text(encoding="utf-8").splitlines()
    kept = [l for l in lines if l.strip() and json.loads(l).get("book_id") != book_id]
    progress_file.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    print(f"Reset progress for '{book_id}'")


# ---------------------------------------------------------------------------
# Book processing
# ---------------------------------------------------------------------------

def process_book(book: dict, config: dict, system_prompt: str, progress: dict[str, set[int]]) -> Path | None:
    book_id = book["id"]
    provider = book["provider"]
    output_dir = ROOT / config["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{book_id}.txt"
    progress_file = ROOT / config["progress_file"]
    progress_file.parent.mkdir(parents=True, exist_ok=True)

    done_chunks = progress.get(book_id, set())

    print(f"\n{'='*56}")
    print(f"  {book['title']}  [{provider} / {book['model']}]")
    print(f"{'='*56}")

    # Check API key
    key_vars = {
        "anthropic": "ANTHROPIC_API_KEY",
        "openai":    "OPENAI_API_KEY",
        "groq":      "GROQ_API_KEY",
    }
    key_var = key_vars.get(provider, f"{provider.upper()}_API_KEY")
    if not os.environ.get(key_var):
        print(f"  [SKIP] {key_var} not set")
        return None

    # Download
    print(f"  Downloading from Gutenberg...")
    try:
        raw = download_gutenberg(book["gutenberg_url"])
    except Exception as e:
        print(f"  [ERROR] Download failed: {e}")
        return None

    clean = strip_gutenberg_boilerplate(raw)
    chunks = chunk_text(clean, int(config["chunk_words"]))
    total = len(chunks)
    print(f"  {len(clean.split()):,} words → {total} chunks")

    if done_chunks:
        print(f"  Resuming — {len(done_chunks)}/{total} chunks already done")

    # Load existing partial output if resuming
    existing_parts: dict[int, str] = {}
    parts_file = output_dir / f"{book_id}.parts.jsonl"
    if parts_file.exists():
        with open(parts_file, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    entry = json.loads(line)
                    existing_parts[entry["chunk_index"]] = entry["text"]

    pending = [i for i in range(total) if i not in done_chunks]

    if provider in ("groq", "openai"):
        _process_chunks_parallel(
            pending, chunks, book_id, book, config, system_prompt,
            existing_parts, progress_file, total
        )
    else:
        _process_chunks_sequential(
            pending, chunks, book_id, book, config, system_prompt,
            existing_parts, parts_file, progress_file, total
        )

    # Assemble final file if all chunks done
    done_now = load_progress(progress_file).get(book_id, set())
    if len(done_now) >= total:
        # reload parts
        all_parts: dict[int, str] = {}
        if parts_file.exists():
            with open(parts_file, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        entry = json.loads(line)
                        all_parts[entry["chunk_index"]] = entry["text"]
        all_parts.update(existing_parts)
        ordered = [all_parts[i] for i in range(total) if i in all_parts]
        full_text = "\n\n".join(ordered)
        output_file.write_text(full_text, encoding="utf-8")
        parts_file.unlink(missing_ok=True)
        kb = len(full_text.encode("utf-8")) // 1024
        print(f"\n  ✓ Complete → {output_file.name} ({kb:,} KB)")
        return output_file
    else:
        remaining = total - len(done_now)
        print(f"\n  Partial — {remaining} chunks remaining. Re-run to continue.")
        return None


def _process_chunks_sequential(
    pending: list[int], chunks: list[str], book_id: str, book: dict,
    config: dict, system_prompt: str, existing_parts: dict[int, str],
    parts_file: Path, progress_file: Path, total: int
) -> None:
    session_start = time.time()
    COOLDOWN_INTERVAL = 30 * 60
    COOLDOWN_PAUSE    =  5 * 60

    for i in pending:
        elapsed = time.time() - session_start
        if elapsed >= COOLDOWN_INTERVAL:
            print(f"  [cooldown] 30 min elapsed -- pausing 5 min...", flush=True)
            time.sleep(COOLDOWN_PAUSE)
            session_start = time.time()
            print("  [cooldown] resuming", flush=True)

        chunk = chunks[i]
        word_count = len(chunk.split())
        print(f"  chunk {i+1}/{total} ({word_count}w)...", end=" ", flush=True)

        try:
            converted = convert_chunk(
                chunk, system_prompt,
                book["provider"], book["model"],
                retries=int(config["max_retries"])
            )
        except Exception as e:
            print(f"FAILED — {e}")
            print("  Saving partial output and stopping this book.")
            break

        existing_parts[i] = converted
        record_progress(progress_file, book_id, i)
        with open(parts_file, "a", encoding="utf-8") as pf:
            pf.write(json.dumps({"chunk_index": i, "text": converted}) + "\n")

        words_out = len(converted.split())
        print(f"done ({words_out}w out)")
        time.sleep(0.5)


PARALLEL_MAX_WORKERS = {"groq": 8, "openai": 3, "anthropic": 2}


def _process_chunks_parallel(
    pending: list[int], chunks: list[str], book_id: str, book: dict,
    config: dict, system_prompt: str, existing_parts: dict[int, str],
    progress_file: Path, total: int
) -> None:
    parts_file = progress_file.parent / f"{book_id}.parts.jsonl"
    lock = threading.Lock()
    done_count = [len(existing_parts)]  # mutable counter
    failed: list[int] = []
    provider = book["provider"]
    max_workers = PARALLEL_MAX_WORKERS.get(provider, 4)

    def do_chunk(i: int) -> tuple[int, str]:
        chunk = chunks[i]
        return i, convert_chunk(
            chunk, system_prompt,
            book["provider"], book["model"],
            retries=int(config.get("max_retries", 3))
        )

    print(f"  [parallel] {len(pending)} chunks, {max_workers} workers", flush=True)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(do_chunk, i): i for i in pending}
        for future in as_completed(futures):
            i = futures[future]
            try:
                idx, converted = future.result()
                with lock:
                    existing_parts[idx] = converted
                    done_count[0] += 1
                    record_progress(progress_file, book_id, idx)
                    with open(parts_file, "a", encoding="utf-8") as pf:
                        pf.write(json.dumps({"chunk_index": idx, "text": converted}) + "\n")
                    words_out = len(converted.split())
                    print(f"  chunk {idx+1}/{total} ✓ ({words_out}w) [{done_count[0]}/{total} done]", flush=True)
            except Exception as e:
                failed.append(i)
                print(f"  chunk {i+1}/{total} FAILED — {e}", flush=True)

    if failed:
        print(f"  [warn] {len(failed)} chunks failed: {failed}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Convert public domain texts to Craig's voice.")
    parser.add_argument("--book", help="Process only this book ID")
    parser.add_argument("--list", action="store_true", help="List all configured books and exit")
    parser.add_argument("--reset", metavar="BOOK_ID", help="Reset progress for a book and re-process")
    parser.add_argument("--config", default=str(CONFIG_PATH))
    args = parser.parse_args()

    config = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    system_prompt = load_system_prompt(STYLE_PROMPT_PATH)
    progress_file = ROOT / config["progress_file"]

    if args.list:
        print(f"{'ID':<25} {'Provider':<12} {'Title'}")
        print("-" * 70)
        for b in config["books"]:
            print(f"{b['id']:<25} {b['provider']:<12} {b['title']}")
        return 0

    if args.reset:
        reset_progress(progress_file, args.reset)
        out = ROOT / config["output_dir"] / f"{args.reset}.txt"
        parts = ROOT / config["output_dir"] / f"{args.reset}.parts.jsonl"
        for f in [out, parts]:
            if f.exists():
                f.unlink()
                print(f"Deleted {f.name}")
        return 0

    books = config["books"]
    if args.book:
        books = [b for b in books if b["id"] == args.book]
        if not books:
            print(f"No book with id '{args.book}'. Use --list to see options.")
            return 1

    progress = load_progress(progress_file)
    completed = []

    for book in books:
        result = process_book(book, config, system_prompt, progress)
        if result:
            completed.append(book["id"])
        # reload progress after each book
        progress = load_progress(progress_file)

    print(f"\n{'='*56}")
    print(f"  Done. {len(completed)}/{len(books)} books fully converted.")
    if completed:
        print(f"  Outputs in: {ROOT / config['output_dir']}")
        print(f"\n  Next steps:")
        print(f"    1. python scripts/clean_text.py --ingest-root data/raw/converted --clean-root data/clean/converted")
        print(f"    2. python scripts/prepare_corpus.py")
        print(f"    3. python scripts/train_tokenizer.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
