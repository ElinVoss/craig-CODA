"""
vault_generate.py — Step 3 of the craig-CODA Obsidian vault build.

Reads manifest.json + connections files and generates Obsidian-compatible
vault pages with story-bible formatting. Pages are organized by story_role:

  universe/    → world_rule pages (DECISIONS.md, SCOPE_MAP.yaml, etc.)
  characters/  → Python module character sheets
  lore/        → _method.md notes + config YAMLs
  locations/   → directory pages
  timeline/    → LIVE_HANDOFF.md baton entries
  artifacts/   → generated outputs
  guardians/   → test files

Regeneration is content-hash-based: a state file tracks
(node_id → hash_of_inputs) so only changed nodes are rewritten.

All page filenames are stable IDs derived from repo-relative paths,
preventing collisions between identically named files (e.g. _method.md).
Obsidian aliases: front matter carries the human-readable display name.
"""

import hashlib
import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent.resolve()
VAULT_DIR = REPO_ROOT / "exports" / "obsidian_vault"
GRAPH_DIR = VAULT_DIR / "_graph"
MANIFEST_PATH = GRAPH_DIR / "manifest.json"
GENERATED_CONN_PATH = GRAPH_DIR / "connections.generated.yaml"
MANUAL_CONN_PATH = GRAPH_DIR / "connections.manual.yaml"
STATE_PATH = GRAPH_DIR / "generate_state.json"

GENERATOR_VERSION = "1.1"

ROLE_TO_DIR = {
    "world_rule": "universe",
    "character": "characters",
    "lore": "lore",
    "location": "locations",
    "timeline": "timeline",
    "artifact": "artifacts",
    "guardian": "guardians",
}


# ---------------------------------------------------------------------------
# Loading helpers
# ---------------------------------------------------------------------------

def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def load_connections() -> dict:
    """Load generated + manual connections; manual entries override generated."""
    conn_map = {}

    def parse_yaml_connections(path: Path) -> list:
        if not path.exists():
            return []
        # Simple line-by-line parser for our known format
        entries = []
        current = {}
        pulse = {}
        in_pulse = False
        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if stripped.startswith("- id:"):
                if current:
                    current["pulse_signature"] = pulse
                    entries.append(current)
                current = {"id": stripped.split(":", 1)[1].strip().strip('"')}
                pulse = {}
                in_pulse = False
            elif stripped.startswith("from_id:"):
                current["from_id"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("from_path:"):
                current["from_path"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("to_id:"):
                current["to_id"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("to_path:"):
                current["to_path"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("edge_type:"):
                current["edge_type"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("relation_type:"):
                current["relation_type"] = stripped.split(":", 1)[1].strip().strip('"')
            elif stripped.startswith("pulse_signature:"):
                in_pulse = True
            elif in_pulse and stripped.startswith("behavioral_marker:"):
                pulse["behavioral_marker"] = stripped.split(":", 1)[1].strip().strip('"')
            elif in_pulse and stripped.startswith("narrative_summary:"):
                pulse["narrative_summary"] = stripped.split(":", 1)[1].strip().strip('"')

        if current:
            current["pulse_signature"] = pulse
            entries.append(current)
        return entries

    for c in parse_yaml_connections(GENERATED_CONN_PATH):
        conn_map[c["id"]] = c
    for c in parse_yaml_connections(MANUAL_CONN_PATH):
        conn_map[c["id"]] = c  # override

    return conn_map


def build_edge_index(connections: dict, nodes: list) -> dict:
    """Build per-node edge index: node_id → {outbound: [...], inbound: [...]}"""
    node_ids = {n["id"] for n in nodes}
    index: dict = {nid: {"out": [], "in": []} for nid in node_ids}
    for c in connections.values():
        if c["from_id"] in index:
            index[c["from_id"]]["out"].append(c)
        if c["to_id"] in index:
            index[c["to_id"]]["in"].append(c)
    return index


def build_node_lookup(nodes: list) -> dict:
    return {n["id"]: n for n in nodes}


# ---------------------------------------------------------------------------
# Content-hash helpers
# ---------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_state(state: dict):
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def input_hash_for_node(node: dict, edges: dict) -> str:
    out_ids = sorted(e["id"] for e in edges.get(node["id"], {}).get("out", []))
    in_ids = sorted(e["id"] for e in edges.get(node["id"], {}).get("in", []))
    payload = json.dumps({
        "content_hash": node.get("content_hash"),
        "display_name": node.get("display_name"),
        "story_role": node.get("story_role"),
        "out": out_ids,
        "in": in_ids,
        "generator_version": GENERATOR_VERSION,
    }, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Wikilink helpers
# ---------------------------------------------------------------------------

def wikilink(node: dict) -> str:
    """[[node_id|display_name]]"""
    return f"[[{node['id']}|{node['display_name']}]]"


def edge_section(label: str, edges: list, node_lookup: dict, direction: str = "out") -> str:
    """
    Render a section of wikilinks for a set of edges.
    direction="out" uses to_id (we are the source, linking to targets)
    direction="in"  uses from_id (we are the target, linking back to sources)
    """
    if not edges:
        return ""
    lines = [f"\n## {label}\n"]
    seen = set()
    for e in edges:
        other_id = e["to_id"] if direction == "out" else e["from_id"]
        if other_id in seen:
            continue
        seen.add(other_id)
        other = node_lookup.get(other_id)
        if not other:
            continue
        narr = e.get("pulse_signature", {}).get("narrative_summary", "")
        link = wikilink(other)
        lines.append(f"- {link}  \n  *{narr}*")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Page renderers per story_role
# ---------------------------------------------------------------------------

def render_world_rule(node: dict, edges: dict, node_lookup: dict) -> str:
    out_edges = edges.get(node["id"], {}).get("out", [])
    in_edges = edges.get(node["id"], {}).get("in", [])
    meta = node.get("metadata", {})
    summary = meta.get("summary", "")[:600]

    sections = [
        f"---",
        f"id: {node['id']}",
        f"title: \"{node['display_name']}\"",
        f"story_role: world_rule",
        f"aliases:",
        f"  - \"{node['display_name']}\"",
        f"source: \"{node['path']}\"",
        f"---",
        f"",
        f"# {node['display_name']} — World Rule",
        f"",
        f"> *The laws this universe runs on.*",
        f"",
        f"## Content",
        f"",
        summary,
        f"",
    ]

    if out_edges:
        sections.append(edge_section("Governs / Mentions", out_edges, node_lookup, "out"))

    if in_edges:
        sections.append(edge_section("Referenced By", in_edges, node_lookup, "in"))

    sections.append(f"\n---\n*Source: `{node['path']}`*")
    return "\n".join(sections)


def render_character(node: dict, edges: dict, node_lookup: dict) -> str:
    out_edges = edges.get(node["id"], {}).get("out", [])
    in_edges = edges.get(node["id"], {}).get("in", [])
    meta = node.get("metadata", {})
    docstring = meta.get("docstring", "").strip()
    functions = meta.get("functions", [])
    classes = meta.get("classes", [])

    implements_edges = [e for e in out_edges if e["relation_type"] == "implements"]
    guarded_by = [e for e in in_edges if e["relation_type"] == "guards"]
    used_by = [e for e in in_edges if e["relation_type"] in ("implements", "feeds_into")]
    mentions_edges = [e for e in out_edges if e["relation_type"] == "mentions"]

    abilities = []
    for cls in classes:
        abilities.append(f"- **class** `{cls}`")
    for fn in functions:
        abilities.append(f"- `{fn}()`")

    sections = [
        f"---",
        f"id: {node['id']}",
        f"title: \"{node['display_name']}\"",
        f"story_role: character",
        f"aliases:",
        f"  - \"{node['display_name']}\"",
        f"source: \"{node['path']}\"",
        f"---",
        f"",
        f"# {node['display_name']} — Character",
        f"",
        f"> *{docstring[:200] if docstring else 'A working part of this universe.'}*",
        f"",
    ]

    if abilities:
        sections += ["## Abilities", ""] + abilities + [""]

    if implements_edges:
        sections.append(edge_section("Implements", implements_edges, node_lookup, "out"))

    if used_by:
        sections.append(edge_section("Known To", used_by, node_lookup, "in"))

    if guarded_by:
        sections.append(edge_section("Protected By", guarded_by, node_lookup, "in"))

    if mentions_edges:
        sections.append(edge_section("Mentions", mentions_edges, node_lookup, "out"))

    sections.append(f"\n---\n*Source: `{node['path']}`*")
    return "\n".join(sections)


def render_lore(node: dict, edges: dict, node_lookup: dict) -> str:
    out_edges = edges.get(node["id"], {}).get("out", [])
    in_edges = edges.get(node["id"], {}).get("in", [])
    meta = node.get("metadata", {})
    fm = meta.get("front_matter", {}) or {}
    summary = meta.get("summary", "").strip()[:800]
    title = node["display_name"]
    applies_to = fm.get("applies_to", [])
    if isinstance(applies_to, str):
        applies_to = [applies_to]

    extends_edges = [e for e in out_edges if e["relation_type"] == "extends"]
    governs_edges = [e for e in out_edges if e["relation_type"] == "governs"]
    implemented_by = [e for e in in_edges if e["relation_type"] == "implements"]
    extended_by = [e for e in in_edges if e["relation_type"] == "extends"]

    sections = [
        f"---",
        f"id: {node['id']}",
        f"title: \"{title}\"",
        f"story_role: lore",
        f"aliases:",
        f"  - \"{title}\"",
        f"source: \"{node['path']}\"",
        f"---",
        f"",
        f"# {title} — The Lore",
        f"",
    ]

    if applies_to:
        sections.append(f"> *Applies to: {', '.join(applies_to)}*\n")

    sections += ["## The Lore", "", summary, ""]

    if extends_edges:
        sections.append(edge_section("Extends", extends_edges, node_lookup, "out"))

    if extended_by:
        sections.append(edge_section("Extended By", extended_by, node_lookup, "in"))

    if governs_edges:
        sections.append(edge_section("Governs", governs_edges, node_lookup, "out"))

    if implemented_by:
        sections.append(edge_section("Implemented By", implemented_by, node_lookup, "in"))

    sections.append(f"\n---\n*Source: `{node['path']}`*")
    return "\n".join(sections)


def render_location(node: dict, edges: dict, node_lookup: dict, all_nodes: list) -> str:
    # Find direct children (nodes whose path starts with this dir's path + /)
    dir_prefix = node["path"] + "/"
    children = [
        n for n in all_nodes
        if n["path"].startswith(dir_prefix)
        and "/" not in n["path"][len(dir_prefix):]
    ]

    in_edges = edges.get(node["id"], {}).get("in", [])

    sections = [
        f"---",
        f"id: {node['id']}",
        f"title: \"{node['display_name']}\"",
        f"story_role: location",
        f"aliases:",
        f"  - \"{node['display_name']}\"",
        f"source: \"{node['path']}/\"",
        f"---",
        f"",
        f"# {node['display_name']} — Location",
        f"",
        f"> *A place in this universe.*",
        f"",
        f"## What Lives Here",
        f"",
    ]

    for child in sorted(children, key=lambda n: n["path"]):
        sections.append(f"- {wikilink(child)}  ({child['story_role']})")

    if in_edges:
        sections.append(edge_section("\n## Referenced By", in_edges, node_lookup, "in"))

    sections.append(f"\n---\n*Source: `{node['path']}/`*")
    return "\n".join(sections)


_BATON_ENTRY_RE = re.compile(
    r"^###\s+(.+?)\s*\|\s*(.+?)\s*\|\s*scope=`(.+?)`$",
    re.MULTILINE,
)


def render_timeline(node: dict, edges: dict, node_lookup: dict) -> str:
    try:
        raw = (REPO_ROOT / node["path"]).read_text(encoding="utf-8", errors="replace")
    except Exception:
        raw = ""

    # Split on ### headings
    entries = re.split(r"\n(?=###\s)", raw)
    entry_blocks = []
    for block in entries:
        m = _BATON_ENTRY_RE.match(block.strip())
        if not m:
            continue
        ts, agent, scope = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        body = block[m.end():].strip()
        entry_blocks.append(f"### {ts} — {agent} `{scope}`\n\n{body}")

    sections = [
        f"---",
        f"id: {node['id']}",
        f"title: \"Timeline of Events\"",
        f"story_role: timeline",
        f"aliases:",
        f"  - \"Timeline\"",
        f"  - \"LIVE_HANDOFF\"",
        f"source: \"{node['path']}\"",
        f"---",
        f"",
        f"# Timeline of Events",
        f"",
        f"> *Every meaningful action taken in this universe, in the order it happened.*",
        f"",
    ]

    if entry_blocks:
        sections += entry_blocks
    else:
        sections.append("*No baton entries detected.*")

    sections.append(f"\n---\n*Source: `{node['path']}`*")
    return "\n".join(sections)


def render_guardian(node: dict, edges: dict, node_lookup: dict) -> str:
    meta = node.get("metadata", {})
    functions = meta.get("functions", [])
    imports = meta.get("imports", [])
    out_edges = edges.get(node["id"], {}).get("out", [])
    guards_edges = [e for e in out_edges if e["relation_type"] == "guards"]

    sections = [
        f"---",
        f"id: {node['id']}",
        f"title: \"{node['display_name']}\"",
        f"story_role: guardian",
        f"aliases:",
        f"  - \"{node['display_name']}\"",
        f"source: \"{node['path']}\"",
        f"---",
        f"",
        f"# {node['display_name']} — Guardian",
        f"",
        f"> *Standing watch over the contracts of this universe.*",
        f"",
    ]

    if guards_edges:
        sections.append(edge_section("Guards", guards_edges, node_lookup, "out"))

    if functions:
        sections += ["\n## Protected Contracts", ""]
        for fn in functions:
            sections.append(f"- `{fn}()`")

    sections.append(f"\n---\n*Source: `{node['path']}`*")
    return "\n".join(sections)


def render_artifact(node: dict, edges: dict, node_lookup: dict) -> str:
    in_edges = edges.get(node["id"], {}).get("in", [])
    sections = [
        f"---",
        f"id: {node['id']}",
        f"title: \"{node['display_name']}\"",
        f"story_role: artifact",
        f"aliases:",
        f"  - \"{node['display_name']}\"",
        f"source: \"{node['path']}\"",
        f"---",
        f"",
        f"# {node['display_name']} — Artifact",
        f"",
        f"> *A relic produced by this universe.*",
        f"",
    ]

    if in_edges:
        sections.append(edge_section("Referenced By", in_edges, node_lookup, "in"))

    sections.append(f"\n---\n*Source: `{node['path']}`*")
    return "\n".join(sections)


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

def render_index(nodes: list) -> str:
    by_role: dict = {}
    for n in nodes:
        by_role.setdefault(n["story_role"], []).append(n)

    lines = [
        "---",
        "id: _index",
        "title: \"craig-CODA Story Bible\"",
        "tags: [index]",
        "---",
        "",
        "# craig-CODA Story Bible",
        "",
        "> *A complete record of the universe of `D:\\craig-CODA`.*",
        "> *Auto-generated by `scripts/run_vault_build.py`. Do not edit directly.*",
        "",
    ]

    role_order = ["world_rule", "character", "lore", "location",
                  "timeline", "artifact", "guardian"]
    role_labels = {
        "world_rule": "The World Rules",
        "character": "Characters",
        "lore": "The Lore",
        "location": "Locations",
        "timeline": "Timeline",
        "artifact": "Artifacts",
        "guardian": "Guardians",
    }

    for role in role_order:
        role_nodes = sorted(by_role.get(role, []), key=lambda n: n["display_name"])
        if not role_nodes:
            continue
        lines.append(f"## {role_labels.get(role, role)}")
        lines.append("")
        for n in role_nodes:
            lines.append(f"- {wikilink(n)}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not MANIFEST_PATH.exists():
        print("vault_generate: manifest.json not found — run vault_flatten.py first")
        return

    manifest = load_manifest()
    nodes = manifest["nodes"]
    connections = load_connections()
    edge_index = build_edge_index(connections, nodes)
    node_lookup = build_node_lookup(nodes)
    state = load_state()
    new_state = {}

    # Ensure output subdirs exist
    for subdir in ROLE_TO_DIR.values():
        (VAULT_DIR / subdir).mkdir(parents=True, exist_ok=True)

    written = skipped = 0

    for node in nodes:
        role = node["story_role"]
        subdir = ROLE_TO_DIR.get(role, "artifacts")
        page_path = VAULT_DIR / subdir / f"{node['id']}.md"

        # Content-hash check
        ih = input_hash_for_node(node, edge_index)
        if state.get(node["id"]) == ih and page_path.exists():
            new_state[node["id"]] = ih
            skipped += 1
            continue

        # Generate page
        try:
            if role == "world_rule":
                content = render_world_rule(node, edge_index, node_lookup)
            elif role == "character":
                content = render_character(node, edge_index, node_lookup)
            elif role == "lore":
                content = render_lore(node, edge_index, node_lookup)
            elif role == "location":
                content = render_location(node, edge_index, node_lookup, nodes)
            elif role == "timeline":
                content = render_timeline(node, edge_index, node_lookup)
            elif role == "guardian":
                content = render_guardian(node, edge_index, node_lookup)
            elif role == "artifact":
                content = render_artifact(node, edge_index, node_lookup)
            else:
                content = render_artifact(node, edge_index, node_lookup)

            page_path.write_text(content, encoding="utf-8")
            new_state[node["id"]] = ih
            written += 1
        except Exception as exc:
            print(f"  WARN: failed to render {node['path']}: {exc}")

    # Write index
    index_content = render_index(nodes)
    (VAULT_DIR / "_index.md").write_text(index_content, encoding="utf-8")

    save_state(new_state)
    print(f"vault_generate: {written} pages written, {skipped} skipped (unchanged)")
    print(f"  vault: {VAULT_DIR}")


if __name__ == "__main__":
    main()
