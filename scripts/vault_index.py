"""
vault_index.py — Step 2 of the craig-CODA Obsidian vault build.

Reads manifest.json and builds a semantic connection graph using pulse-cell
language — the repo describing its own structure in the same vocabulary the
project uses for donor behavioral extraction.

Connection detection sources:
  1. Python AST imports (already extracted in manifest metadata)
  2. Method-vault ancestry — parent folder has _method.md → extends edge
  3. YAML applies_to field in method notes → governs edge
  4. SCOPE_MAP.yaml read_order lists → mirrors edge
  5. Markdown file references (backtick paths) → mentions edge
  6. Test file imports → guards edge

Output:
  exports/obsidian_vault/_graph/connections.generated.yaml  (rebuilt each run)
  exports/obsidian_vault/_graph/connections.manual.yaml     (seeded once, user-maintained)
"""

import json
import re
from pathlib import Path

try:
    import yaml
    _YAML = True
except ImportError:
    _YAML = False

REPO_ROOT = Path(__file__).parent.parent.resolve()
GRAPH_DIR = REPO_ROOT / "exports" / "obsidian_vault" / "_graph"
MANIFEST_PATH = GRAPH_DIR / "manifest.json"
GENERATED_PATH = GRAPH_DIR / "connections.generated.yaml"
MANUAL_PATH = GRAPH_DIR / "connections.manual.yaml"

GENERATOR_VERSION = "1.0"

# Map edge_type → relation_type (story-role vocabulary)
EDGE_TO_RELATION = {
    "imports": "implements",         # code implements a contract it imports
    "imports_test": "guards",        # test importing something it watches
    "vault_ancestry": "extends",     # child note extends parent
    "applies_to": "governs",         # vault note governs named scope
    "scope_read_order": "mirrors",   # doc mirrors the component it describes
    "file_mention": "mentions",      # doc names this file
    "feeds": "feeds_into",           # explicit data-flow edges (hand-written)
}

# Narrative summary templates — the "original" part
NARRATIVE_TEMPLATES = {
    "implements": "{from_name} brings the contract to life — it is the code behind the word.",
    "extends": "{from_name} carries {to_name} forward — the child form of its elder.",
    "governs": "{from_name} sets the law. {to_name} must follow it.",
    "mirrors": "{from_name} is the map of the territory that is {to_name}.",
    "guards": "{from_name} stands at the gate — nothing passes without its approval.",
    "mentions": "{from_name} names {to_name} — a thread that binds them.",
    "feeds_into": "{from_name} ends where {to_name} begins.",
    "contradicts": "{from_name} and {to_name} are in tension. One will give way.",
}

BEHAVIORAL_MARKER_TEMPLATES = {
    "implements": "{from_name} realizes the abstract contract defined by {to_name}",
    "extends": "{from_name} is the child form of {to_name}",
    "governs": "{from_name} defines the rules that {to_name} must follow",
    "mirrors": "{from_name} documents the behavior of {to_name}",
    "guards": "{from_name} validates the invariants that {to_name} promises",
    "mentions": "{from_name} references {to_name} by path or name",
    "feeds_into": "output of {from_name} is consumed by {to_name}",
    "contradicts": "{from_name} and {to_name} represent competing approaches",
}


def load_manifest() -> dict:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return data


def build_path_lookup(nodes: list) -> dict:
    """Map repo-relative path → node dict."""
    lookup = {}
    for n in nodes:
        lookup[n["path"]] = n
    return lookup


def make_conn_id(from_id: str, edge_type: str, to_id: str) -> str:
    return f"conn--{from_id}--{edge_type}--{to_id}"


def render_pulse(relation_type: str, from_name: str, to_name: str) -> dict:
    tmpl_narr = NARRATIVE_TEMPLATES.get(relation_type, "{from_name} → {to_name}")
    tmpl_beh = BEHAVIORAL_MARKER_TEMPLATES.get(relation_type, "{from_name} connects to {to_name}")
    return {
        "behavioral_marker": tmpl_beh.format(from_name=from_name, to_name=to_name),
        "narrative_summary": tmpl_narr.format(from_name=from_name, to_name=to_name),
    }


def make_connection(from_node: dict, to_node: dict, edge_type: str) -> dict:
    relation_type = EDGE_TO_RELATION.get(edge_type, "mentions")
    pulse = render_pulse(relation_type, from_node["display_name"], to_node["display_name"])
    conn_id = make_conn_id(from_node["id"], edge_type, to_node["id"])
    return {
        "id": conn_id,
        "from_id": from_node["id"],
        "from_path": from_node["path"],
        "to_id": to_node["id"],
        "to_path": to_node["path"],
        "edge_type": edge_type,
        "relation_type": relation_type,
        "pulse_signature": pulse,
    }


def detect_import_edges(node: dict, path_lookup: dict) -> list:
    """Python import statements → implements or guards edges."""
    if node["file_type"] not in ("python_module", "test_module"):
        return []

    imports = node.get("metadata", {}).get("imports", [])
    is_test = node["file_type"] == "test_module"
    edges = []
    node_dir = str(Path(node["path"]).parent).replace("\\", "/")

    for imp in imports:
        # Convert dotted import to possible repo-relative paths
        imp_path_candidate = imp.replace(".", "/") + ".py"
        candidates = [
            imp_path_candidate,
            "src/" + imp_path_candidate,
        ]
        for candidate in candidates:
            if candidate in path_lookup and candidate != node["path"]:
                target = path_lookup[candidate]
                etype = "imports_test" if is_test else "imports"
                edges.append(make_connection(node, target, etype))
                break

    return edges


def detect_vault_ancestry_edges(node: dict, path_lookup: dict) -> list:
    """
    Method vault _method.md notes: parent folder also has a _method.md → extends.
    Ancestry is derived from folder hierarchy, not from applies_to.
    """
    if node["file_type"] != "method_note" or not node["path"].endswith("_method.md"):
        return []

    edges = []
    p = Path(node["path"])
    parent = p.parent.parent  # grandparent dir

    while True:
        parent_note_path = str(parent / "_method.md").replace("\\", "/")
        if parent_note_path in path_lookup and parent_note_path != node["path"]:
            edges.append(make_connection(node, path_lookup[parent_note_path], "vault_ancestry"))
        if parent == parent.parent:
            break
        parent = parent.parent

    return edges


def detect_applies_to_edges(node: dict, path_lookup: dict, nodes: list) -> list:
    """
    applies_to in YAML front matter → governs edge toward any node whose
    path or display_name matches the tag.
    """
    fm = {}
    if node["file_type"] == "method_note":
        meta = node.get("metadata", {})
        fm = meta.get("front_matter", {}) if isinstance(meta, dict) else {}
        if not fm:
            # markdown method note: front_matter is nested
            fm = meta

    applies_to = fm.get("applies_to", [])
    if isinstance(applies_to, str):
        applies_to = [applies_to]
    if not applies_to:
        return []

    edges = []
    for tag in applies_to:
        tag_lower = tag.lower()
        for target in nodes:
            if target["id"] == node["id"]:
                continue
            if (tag_lower in target["path"].lower()
                    or tag_lower == target["display_name"].lower()):
                edges.append(make_connection(node, target, "applies_to"))
                break

    return edges


def detect_scope_map_edges(nodes: list, path_lookup: dict) -> list:
    """
    SCOPE_MAP.yaml read_order lists → mirrors edges from each listed file
    back to the SCOPE_MAP itself.
    """
    scope_map_path = "SCOPE_MAP.yaml"
    if scope_map_path not in path_lookup:
        return []

    scope_map_node = path_lookup[scope_map_path]

    try:
        import yaml as _yaml
        content = (REPO_ROOT / scope_map_path).read_text(encoding="utf-8")
        data = _yaml.safe_load(content) or {}
    except Exception:
        return []

    edges = []
    for scope_name, scope_data in data.get("scopes", {}).items():
        for listed_path in scope_data.get("read_order", []):
            listed_path_norm = listed_path.replace("\\", "/")
            if listed_path_norm in path_lookup and listed_path_norm != scope_map_path:
                target = path_lookup[listed_path_norm]
                edges.append(make_connection(target, scope_map_node, "scope_read_order"))

    return edges


def detect_file_mention_edges(node: dict, path_lookup: dict) -> list:
    """
    Markdown file references (backtick paths) in docs → mentions edges.
    Only for markdown docs and world_rule pages.
    """
    if node["file_type"] not in ("markdown_doc", "method_note"):
        return []
    if node["story_role"] not in ("world_rule", "timeline", "lore"):
        return []

    file_refs = node.get("metadata", {}).get("file_refs", [])
    edges = []

    for ref in file_refs:
        ref_norm = ref.replace("\\", "/").lstrip("/")
        if ref_norm in path_lookup and ref_norm != node["path"]:
            edges.append(make_connection(node, path_lookup[ref_norm], "file_mention"))

    return edges


def dump_yaml_connections(connections: list, extra_header: str = "") -> str:
    """Serialize connection list to YAML-like text without requiring pyyaml."""
    lines = ["schema_version: \"1.0\""]
    if extra_header:
        lines.append(extra_header)
    lines.append("connections:")

    for c in connections:
        lines.append(f"  - id: \"{c['id']}\"")
        lines.append(f"    from_id: \"{c['from_id']}\"")
        lines.append(f"    from_path: \"{c['from_path']}\"")
        lines.append(f"    to_id: \"{c['to_id']}\"")
        lines.append(f"    to_path: \"{c['to_path']}\"")
        lines.append(f"    edge_type: \"{c['edge_type']}\"")
        lines.append(f"    relation_type: \"{c['relation_type']}\"")
        ps = c.get("pulse_signature", {})
        lines.append("    pulse_signature:")
        lines.append(f"      behavioral_marker: \"{ps.get('behavioral_marker', '')}\"")
        lines.append(f"      narrative_summary: \"{ps.get('narrative_summary', '')}\"")

    return "\n".join(lines) + "\n"


def main():
    if not MANIFEST_PATH.exists():
        print("vault_index: manifest.json not found — run vault_flatten.py first")
        return

    manifest = load_manifest()
    nodes = manifest["nodes"]
    path_lookup = build_path_lookup(nodes)

    all_connections = {}

    def add(edges: list):
        for e in edges:
            all_connections[e["id"]] = e

    # 1. Python import edges
    for node in nodes:
        add(detect_import_edges(node, path_lookup))

    # 2. Vault ancestry edges
    for node in nodes:
        add(detect_vault_ancestry_edges(node, path_lookup))

    # 3. applies_to edges
    for node in nodes:
        add(detect_applies_to_edges(node, path_lookup, nodes))

    # 4. SCOPE_MAP read_order edges
    add(detect_scope_map_edges(nodes, path_lookup))

    # 5. Markdown file mention edges
    for node in nodes:
        add(detect_file_mention_edges(node, path_lookup))

    connections = sorted(all_connections.values(), key=lambda c: c["id"])

    # Write generated connections
    header = ("description: >\n"
              "  The repo's own living substrate — every meaningful connection between\n"
              "  entities in this universe, expressed as pulse cells. The story of how\n"
              "  the pieces know each other. Auto-generated. Edit connections.manual.yaml\n"
              "  to add or override entries.")
    GENERATED_PATH.write_text(
        dump_yaml_connections(connections, header),
        encoding="utf-8",
    )

    # Seed manual connections file if it doesn't exist
    if not MANUAL_PATH.exists():
        MANUAL_PATH.write_text(
            "# Hand-editable connection overrides and additions.\n"
            "# Entries here are merged with connections.generated.yaml at render time.\n"
            "# Use matching 'id' fields to override a generated entry.\n"
            "# Add new entries with any id not in the generated file.\n"
            "schema_version: \"1.0\"\n"
            "connections: []\n",
            encoding="utf-8",
        )

    # Stats
    by_relation: dict = {}
    for c in connections:
        r = c["relation_type"]
        by_relation[r] = by_relation.get(r, 0) + 1

    print(f"vault_index: {len(connections)} connections written to {GENERATED_PATH}")
    for rel, count in sorted(by_relation.items()):
        print(f"  {rel:20s} {count}")


if __name__ == "__main__":
    main()
