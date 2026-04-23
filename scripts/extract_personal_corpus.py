"""
Extract personal corpus from user-authored sources.

Sources:
  - conversations.json (ChatGPT export): user messages only
  - OneDrive docx files: personal writing documents (confluencechronicles)
  - mylessonlearned OneDrive: root-level docs + recovered drive files
  - Personal txt/md files from known locations
  - Pallet Positions field notes
  - Existing user_model_package artifacts

Output: data/raw/personal/ with one file per source category.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OUTPUT_DIR = ROOT / "data" / "raw" / "personal"

CONVERSATIONS_JSON = Path(r"C:\Users\NeverAMoment\Desktop\slight failures\conversations.json")

FACEBOOK_ZIP = Path(r"C:\Users\NeverAMoment\Downloads\facebook-DCI577419-2026-04-22-QoBL34Zw.zip")
FACEBOOK_SENDER_NAME = "Craig Ramos"  # only extract messages sent by this name

ONEDRIVE_DOCS = Path(r"C:\Users\Never A Moment\OneDrive\Documents")

# mylessonlearned OneDrive — root-level unique docs (not duplicates of Documents/ folder)
# Note: Document 3/4 and 6.docx had 0 paragraphs (image-only or corrupt) — skipped
MYLESSONLEARNED_ROOT_DOCS: list[Path] = []

RECOVERED_DRIVE = Path(
    r"C:\Users\NeverAMoment\OneDrive\Desktop\ther drive befire i wiped\Recovered Types(0)\Document Files"
)

# Files in the recovered drive that must never enter the corpus (contain credentials or sensitive data)
RECOVERED_SKIP_FILES = {"00030.docx", "00030.doc"}  # contains stored passwords

PERSONAL_FILES = [
    Path(r"C:\Users\NeverAMoment\Downloads\Craig_Ramos_Self_Perceived_Cognitive_System.txt"),
    Path(r"C:\Users\NeverAMoment\Downloads\craig_ramos_user_model.md"),
    Path(r"C:\Users\NeverAMoment\Desktop\Pallet Positions and Painful Lesson.txt"),
    Path(r"C:\Users\NeverAMoment\Downloads\how about now_.md"),
    Path(r"C:\Users\NeverAMoment\Downloads\Pasted markdown.md"),
]

USER_MODEL_PACKAGE = ROOT / "exports" / "user_model_package"

# Docx files to skip (Samsung backup, fiction, financial)
DOCX_SKIP_PATTERNS = ["Samsung", "SmartSwitch", "backup", "Flaw", "flaw", "Novel", "novel",
                      "book", "Book", "draft", "Draft"]

# Warehouse/fiction exclusions from downloads
SKIP_FILENAME_PATTERNS = [
    "warehouse", "move-list", "MoveList", "ConsolidationPlan", "bin_map",
    "N01_", "N02_", "JHACE", "novella", "Novella", "chronicles", "Chronicles",
    "manuscript", "Grip", "grip", "WarehouseAgent",
]


def is_warehouse_or_fiction(path: Path) -> bool:
    name = path.name
    return any(p in name for p in SKIP_FILENAME_PATTERNS)


def clean_text(text: str) -> str:
    # Collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading/trailing whitespace per line
    lines = [ln.rstrip() for ln in text.splitlines()]
    return "\n".join(lines).strip()


def extract_chatgpt_user_messages(path: Path) -> str:
    """Extract only user-authored messages from ChatGPT export JSON."""
    print(f"  Loading {path.name} ({path.stat().st_size // (1024*1024)} MB)...")
    with open(path, encoding="utf-8", errors="replace") as f:
        data = json.load(f)

    messages = []
    for conversation in data:
        mapping = conversation.get("mapping", {})
        for node in mapping.values():
            msg = node.get("message")
            if not msg:
                continue
            author = msg.get("author", {})
            if author.get("role") != "user":
                continue
            content = msg.get("content", {})
            parts = content.get("parts", [])
            for part in parts:
                if isinstance(part, str) and part.strip():
                    messages.append(part.strip())

    combined = "\n\n".join(messages)
    print(f"  Extracted {len(messages):,} user messages ({len(combined):,} chars)")
    return combined


def extract_docx(path: Path) -> str:
    """Extract text from a .docx file."""
    try:
        from docx import Document
        doc = Document(str(path))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n\n".join(paragraphs)
    except Exception as e:
        print(f"  [warn] Could not read {path.name}: {e}")
        return ""


def extract_onedrive_docs(base: Path) -> str:
    """Extract text from personal docx files in OneDrive/Documents."""
    if not base.exists():
        print(f"  [skip] OneDrive docs path not found: {base}")
        return ""

    parts = []
    for docx in sorted(base.glob("*.docx")) + sorted(base.glob("*.odt")):
        if any(skip in str(docx) for skip in DOCX_SKIP_PATTERNS):
            continue
        text = extract_docx(docx)
        if text.strip():
            print(f"  + {docx.name} ({len(text):,} chars)")
            parts.append(f"# {docx.stem}\n\n{text}")
    return "\n\n---\n\n".join(parts)


def extract_rtf_text(path: Path) -> str:
    """Extract plain text from an RTF file by stripping RTF control codes."""
    try:
        raw = path.read_bytes().decode("latin-1", errors="replace")
        # Strip RTF header and control words
        text = re.sub(r"\\[a-z]+\d*\s?", " ", raw)
        text = re.sub(r"[{}\\]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
    except Exception as e:
        print(f"  [warn] Could not read RTF {path.name}: {e}")
        return ""


def extract_recovered_drive(base: Path) -> str:
    """Extract text from recovered drive docx and rtf files."""
    if not base.exists():
        print(f"  [skip] Recovered drive path not found: {base}")
        return ""

    parts = []

    # Docx files are in a named subfolder
    docx_dir = base / "(.docx) MS Office 2007 WORD Document"
    if docx_dir.exists():
        for f in sorted(docx_dir.glob("*.docx")):
            if f.name in RECOVERED_SKIP_FILES:
                print(f"  [SKIP - sensitive] {f.name}")
                continue
            text = extract_docx(f)
            if text and len(text.strip()) > 100:
                print(f"  + {f.name} ({len(text):,} chars)")
                parts.append(text.strip())

    # RTF files in their subfolder
    rtf_dir = base / "(.rtf) Rich Text Format Document"
    if rtf_dir.exists():
        for f in sorted(rtf_dir.glob("*.rtf")):
            if f.name in RECOVERED_SKIP_FILES:
                print(f"  [SKIP - sensitive] {f.name}")
                continue
            text = extract_rtf_text(f)
            if text and len(text.strip()) > 100:
                print(f"  + {f.name} ({len(text):,} chars)")
                parts.append(text.strip())

    return "\n\n---\n\n".join(parts)


def extract_mylessonlearned_docs(root_docs: list[Path]) -> str:
    """Extract text from root-level mylessonlearned OneDrive docs."""
    parts = []
    for p in root_docs:
        if not p.exists():
            print(f"  [skip] {p.name} not found")
            continue
        if any(skip in p.name for skip in DOCX_SKIP_PATTERNS):
            print(f"  [skip] {p.name} (fiction/excluded)")
            continue
        text = extract_docx(p)
        if text and text.strip():
            print(f"  + {p.name} ({len(text):,} chars)")
            parts.append(f"# {p.stem}\n\n{text.strip()}")
    return "\n\n---\n\n".join(parts)


def extract_user_model_package(base: Path) -> str:
    """Extract all text artifacts from user_model_package."""
    if not base.exists():
        return ""
    parts = []
    for ext in ["*.txt", "*.md"]:
        for f in sorted(base.rglob(ext)):
            text = f.read_text(encoding="utf-8", errors="replace").strip()
            if text:
                parts.append(f"# {f.stem}\n\n{text}")
    return "\n\n---\n\n".join(parts)


def extract_facebook_messages(zip_path: Path, sender_name: str) -> str:
    """Extract user-sent messages from Facebook data export ZIP.

    Reads all message_N.json files in inbox/ and other_folder/, keeps only
    messages where sender_name matches the user.  Automated system messages
    (e.g. 'You marked the listing as Sold.') are filtered out.
    """
    import zipfile

    if not zip_path.exists():
        print(f"  [skip] Facebook ZIP not found: {zip_path}")
        return ""

    system_patterns = re.compile(
        r"^(You (marked|changed|updated|set|added|removed|created|left|named)|"
        r"[\w\s]+ (named the group|set the nickname|changed the group))",
        re.IGNORECASE,
    )

    parts = []
    thread_count = 0
    message_count = 0

    with zipfile.ZipFile(zip_path, "r") as zf:
        msg_entries = [
            e for e in zf.infolist()
            if re.search(r"(inbox|other_folder|filtered_threads)/.+/message_\d+\.json", e.filename)
        ]
        print(f"  Found {len(msg_entries)} message JSON files")

        for entry in msg_entries:
            try:
                with zf.open(entry) as f:
                    raw = f.read().decode("utf-8", errors="replace")
                data = json.loads(raw)
            except Exception as e:
                print(f"  [warn] Could not read {entry.filename}: {e}")
                continue

            thread_messages = []
            for msg in data.get("messages", []):
                if msg.get("sender_name") != sender_name:
                    continue
                content = msg.get("content", "")
                if not isinstance(content, str) or not content.strip():
                    continue
                if system_patterns.match(content.strip()):
                    continue
                thread_messages.append(content.strip())

            if thread_messages:
                thread_count += 1
                message_count += len(thread_messages)
                parts.extend(thread_messages)

    print(f"  Extracted {message_count:,} messages from {thread_count} threads")
    return "\n\n".join(parts)


def write_source(name: str, text: str) -> Path | None:
    text = clean_text(text)
    if not text:
        print(f"  [skip] {name} — no content")
        return None
    out = OUTPUT_DIR / f"{name}.txt"
    out.write_text(text, encoding="utf-8")
    kb = len(text.encode("utf-8")) // 1024
    print(f"  -> {out.name} ({kb:,} KB)")
    return out


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Output dir: {OUTPUT_DIR}\n")

    results = {}

    # 1. ChatGPT conversation export
    if CONVERSATIONS_JSON.exists():
        print("=== ChatGPT user messages ===")
        text = extract_chatgpt_user_messages(CONVERSATIONS_JSON)
        results["chatgpt_user_messages"] = write_source("chatgpt_user_messages", text)
    else:
        print(f"[skip] conversations.json not found at {CONVERSATIONS_JSON}")

    # 2. OneDrive personal documents
    print("\n=== OneDrive personal docs ===")
    text = extract_onedrive_docs(ONEDRIVE_DOCS)
    results["onedrive_personal_docs"] = write_source("onedrive_personal_docs", text)

    # 3. Individual personal files
    print("\n=== Personal files ===")
    parts = []
    for p in PERSONAL_FILES:
        if not p.exists():
            print(f"  [skip] {p.name} not found")
            continue
        if is_warehouse_or_fiction(p):
            print(f"  [skip] {p.name} (excluded category)")
            continue
        text = p.read_text(encoding="utf-8", errors="replace").strip()
        if text:
            print(f"  + {p.name} ({len(text):,} chars)")
            parts.append(f"# {p.stem}\n\n{text}")
    results["personal_notes"] = write_source("personal_notes", "\n\n---\n\n".join(parts))

    # 4. mylessonlearned OneDrive root docs
    print("\n=== mylessonlearned OneDrive root docs ===")
    text = extract_mylessonlearned_docs(MYLESSONLEARNED_ROOT_DOCS)
    results["mylessonlearned_docs"] = write_source("mylessonlearned_docs", text)

    # 5. Recovered drive files
    print("\n=== Recovered drive (wiped) files ===")
    text = extract_recovered_drive(RECOVERED_DRIVE)
    results["recovered_drive"] = write_source("recovered_drive", text)

    # 6. User model package
    print("\n=== User model package ===")
    text = extract_user_model_package(USER_MODEL_PACKAGE)
    results["user_model_package"] = write_source("user_model_package", text)

    # 7. Facebook Messenger messages
    print("\n=== Facebook Messenger (user messages only) ===")
    text = extract_facebook_messages(FACEBOOK_ZIP, FACEBOOK_SENDER_NAME)
    results["facebook_messages"] = write_source("facebook_messages", text)

    # Summary
    print("\n=== Summary ===")
    total_bytes = 0
    for name, path in results.items():
        if path and path.exists():
            size = path.stat().st_size
            total_bytes += size
            print(f"  {name}: {size // 1024:,} KB")
    print(f"\nTotal: {total_bytes // (1024*1024):.1f} MB in {OUTPUT_DIR}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
