"""
Message Extraction Pipeline

Parses E:\\Messages\\sms-20260426024848.xml and produces:

  data/raw/messages/corpus.txt             — all personal conversation text (named contacts only)
  data/raw/messages/craig_sent.txt         — Craig's sent messages only (voice corpus)
  data/raw/messages/conversations/         — one JSONL per contact (conversation threads)
  data/raw/messages/sft_pairs.jsonl        — (received → Craig reply) SFT training pairs
  data/raw/messages/vault_nodes.jsonl      — episodic VaultNode records per conversation session

Usage:
    python scripts/extract_messages.py
    python scripts/extract_messages.py --xml "E:\\Messages\\sms-20260426024848.xml"
    python scripts/extract_messages.py --dry-run
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).parents[1]))

from src.memory.node_schema import VaultNode

DEFAULT_XML = Path(r"E:\Messages\sms-20260426024848.xml")
OUT_DIR = Path("data/raw/messages")

# Gap that splits a continuous exchange into a new conversation "session"
SESSION_GAP_SECONDS = 4 * 3600   # 4 hours
# Max gap between received message and Craig's reply to form an SFT pair
SFT_REPLY_WINDOW_SECONDS = 30 * 60  # 30 minutes
# Contact name used when no name is known
AUTOMATED_CONTACT = "(Unknown)"
# Contacts to skip entirely (automated, bots, service accounts)
SKIP_CONTACTS = {AUTOMATED_CONTACT, "", "Gemini", "AT&T Service Contacts"}


# ── Parsing ──────────────────────────────────────────────────────────────────

def _mms_text(mms_elem: ET.Element) -> str:
    """Extract text body from an MMS element."""
    for part in mms_elem.iter("part"):
        ct = part.get("ct", "")
        if "text" in ct and "smil" not in ct:
            text = part.get("text", "")
            if text and text.lower() != "null":
                return text.strip()
    return ""


def parse_messages(xml_path: Path) -> list[dict]:
    """Return all personal messages as a list of dicts, sorted by timestamp."""
    tree = ET.parse(str(xml_path))
    root = tree.getroot()
    messages: list[dict] = []

    for sms in root.findall("sms"):
        contact = sms.get("contact_name", AUTOMATED_CONTACT)
        if contact in SKIP_CONTACTS:
            continue
        body = sms.get("body", "").strip()
        if not body or body.lower() == "null":
            continue
        messages.append({
            "ts": int(sms.get("date", 0)) // 1000,
            "contact": contact,
            "address": sms.get("address", ""),
            "sent_by_craig": sms.get("type", "1") == "2",
            "body": body,
            "kind": "sms",
        })

    for mms in root.findall("mms"):
        contact = mms.get("contact_name", AUTOMATED_CONTACT)
        if contact in SKIP_CONTACTS:
            continue
        text = _mms_text(mms)
        if not text:
            continue
        messages.append({
            "ts": int(mms.get("date", 0)) // 1000,
            "contact": contact,
            "address": mms.get("address", ""),
            "sent_by_craig": mms.get("msg_box", "1") == "2",
            "body": text,
            "kind": "mms",
        })

    return sorted(messages, key=lambda m: m["ts"])


# ── Session splitting ─────────────────────────────────────────────────────────

def split_sessions(messages: list[dict]) -> list[list[dict]]:
    """Group messages into conversation sessions based on time gap."""
    if not messages:
        return []
    sessions: list[list[dict]] = [[messages[0]]]
    for msg in messages[1:]:
        if msg["ts"] - sessions[-1][-1]["ts"] > SESSION_GAP_SECONDS:
            sessions.append([])
        sessions[-1].append(msg)
    return sessions


# ── SFT pair extraction ───────────────────────────────────────────────────────

def extract_sft_pairs(messages: list[dict]) -> list[dict]:
    """
    For each of Craig's sent messages that immediately follows a received message
    within the SFT_REPLY_WINDOW, emit an input→output pair.
    """
    pairs: list[dict] = []
    for i, msg in enumerate(messages):
        if not msg["sent_by_craig"]:
            continue
        # Look back for the most recent received message within the window
        for j in range(i - 1, max(i - 5, -1), -1):
            prev = messages[j]
            if prev["sent_by_craig"]:
                continue
            if msg["ts"] - prev["ts"] > SFT_REPLY_WINDOW_SECONDS:
                break
            if prev["contact"] != msg["contact"]:
                continue
            pairs.append({
                "input": prev["body"],
                "output": msg["body"],
                "contact": msg["contact"],
                "ts": msg["ts"],
                "readable_date": datetime.fromtimestamp(msg["ts"], tz=timezone.utc).strftime("%Y-%m-%d"),
                "source": "sms_backup",
            })
            break
    return pairs


# ── Vault node creation ───────────────────────────────────────────────────────

def _node_id(contact: str, session_ts: int) -> str:
    raw = f"sms::{contact}::{session_ts}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def _session_summary(session: list[dict]) -> str:
    date_str = datetime.fromtimestamp(session[0]["ts"], tz=timezone.utc).strftime("%Y-%m-%d")
    sent = sum(1 for m in session if m["sent_by_craig"])
    received = sum(1 for m in session if not m["sent_by_craig"])
    return f"SMS conversation with {session[0]['contact']} on {date_str} ({sent} sent, {received} received)"


def _session_content(session: list[dict], max_chars: int = 2000) -> str:
    lines = []
    total = 0
    for msg in session:
        who = "Craig" if msg["sent_by_craig"] else msg["contact"]
        ts = datetime.fromtimestamp(msg["ts"], tz=timezone.utc).strftime("%H:%M")
        line = f"[{ts}] {who}: {msg['body']}"
        total += len(line)
        if total > max_chars:
            lines.append(f"... ({len(session) - len(lines)} more messages)")
            break
        lines.append(line)
    return "\n".join(lines)


def make_vault_nodes(messages: list[dict]) -> list[VaultNode]:
    by_contact = defaultdict(list)
    for msg in messages:
        by_contact[msg["contact"]].append(msg)

    nodes: list[VaultNode] = []
    timestamp = datetime.now(timezone.utc).isoformat()

    for contact, msgs in by_contact.items():
        sessions = split_sessions(msgs)
        for session in sessions:
            if len(session) < 2:
                continue
            date_str = datetime.fromtimestamp(session[0]["ts"], tz=timezone.utc).strftime("%Y-%m-%d")
            node = VaultNode(
                id=_node_id(contact, session[0]["ts"]),
                node_type="event_note",
                trust_layer="episodic_events",
                content=_session_content(session),
                summary=_session_summary(session),
                source_path="E:/Messages/sms-20260426024848.xml",
                source_kind="sms_backup",
                created_at=timestamp,
                time_start=date_str,
                time_end=datetime.fromtimestamp(session[-1]["ts"], tz=timezone.utc).strftime("%Y-%m-%d"),
                life_phase="current",
                people=[contact],
                projects=[],
                tags=["#sms", "#conversation", f"#contact_{re.sub(r'[^a-z0-9]', '_', contact.lower())}"],
                confidence=0.90,
                privacy_level="restricted",
                voice_score=0.70,
                reasoning_score=0.40,
                prose_score=0.65,
                project_relevance=0.30,
            )
            nodes.append(node)

    return nodes


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="Extract message data from SMS Backup & Restore XML.")
    p.add_argument("--xml", default=str(DEFAULT_XML))
    p.add_argument("--out-dir", default=str(OUT_DIR))
    p.add_argument("--dry-run", action="store_true", help="Print stats only, write nothing")
    args = p.parse_args()

    xml_path = Path(args.xml)
    out_dir = Path(args.out_dir)

    print(f"Parsing: {xml_path}")
    messages = parse_messages(xml_path)
    print(f"Personal messages: {len(messages)}")

    craig_sent = [m for m in messages if m["sent_by_craig"]]
    received = [m for m in messages if not m["sent_by_craig"]]
    sft_pairs = extract_sft_pairs(messages)
    vault_nodes = make_vault_nodes(messages)

    by_contact = defaultdict(list)
    for m in messages:
        by_contact[m["contact"]].append(m)

    print(f"  Craig sent:    {len(craig_sent)}")
    print(f"  Received:      {len(received)}")
    print(f"  SFT pairs:     {len(sft_pairs)}")
    print(f"  Vault nodes:   {len(vault_nodes)}")
    print(f"  Contacts:      {sorted(by_contact.keys())}")

    if args.dry_run:
        print("\n--- Sample SFT pair ---")
        if sft_pairs:
            print(json.dumps(sft_pairs[0], indent=2))
        print("\n--- Sample vault node ---")
        if vault_nodes:
            print(vault_nodes[0].summary)
            print(vault_nodes[0].content[:300])
        return

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "conversations").mkdir(exist_ok=True)

    # corpus.txt — all personal messages
    corpus_path = out_dir / "corpus.txt"
    with corpus_path.open("w", encoding="utf-8") as f:
        for m in messages:
            f.write(m["body"] + "\n")
    print(f"\nWritten: {corpus_path} ({corpus_path.stat().st_size // 1024} KB)")

    # craig_sent.txt — voice corpus
    voice_path = out_dir / "craig_sent.txt"
    with voice_path.open("w", encoding="utf-8") as f:
        for m in craig_sent:
            f.write(m["body"] + "\n")
    print(f"Written: {voice_path} ({voice_path.stat().st_size // 1024} KB)")

    # conversations/ — one JSONL per contact
    for contact, msgs in by_contact.items():
        safe_name = re.sub(r"[^a-zA-Z0-9_-]", "_", contact) + ".jsonl"
        cpath = out_dir / "conversations" / safe_name
        with cpath.open("w", encoding="utf-8") as f:
            for m in msgs:
                row = dict(m)
                row["readable_date"] = datetime.fromtimestamp(m["ts"], tz=timezone.utc).strftime("%Y-%m-%d %H:%M")
                f.write(json.dumps(row) + "\n")
    print(f"Written: {out_dir / 'conversations'}/ ({len(by_contact)} files)")

    # sft_pairs.jsonl
    sft_path = out_dir / "sft_pairs.jsonl"
    with sft_path.open("w", encoding="utf-8") as f:
        for pair in sft_pairs:
            f.write(json.dumps(pair) + "\n")
    print(f"Written: {sft_path} ({len(sft_pairs)} pairs)")

    # vault_nodes.jsonl
    vault_path = out_dir / "vault_nodes.jsonl"
    with vault_path.open("w", encoding="utf-8") as f:
        for node in vault_nodes:
            f.write(json.dumps(node.to_dict()) + "\n")
    print(f"Written: {vault_path} ({len(vault_nodes)} nodes)")


if __name__ == "__main__":
    main()
