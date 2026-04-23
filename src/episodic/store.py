from __future__ import annotations
import sqlite3
import json
import uuid
import numpy as np
from pathlib import Path
from datetime import datetime
from .node import MemoryNode

# Resonance bond logic lives here intentionally (update_resonance, resonance table).
# No separate resonance.py module.

SCHEMA = """
CREATE TABLE IF NOT EXISTS nodes (
    id                  TEXT PRIMARY KEY,
    content             TEXT NOT NULL,
    keywords            TEXT,
    emotional           REAL,
    circumstantial      REAL,
    developmental_phase REAL,
    mood_tag            TEXT,
    context_tag         TEXT,
    domain              TEXT,
    timestamp           TEXT,
    reinforce_count     INTEGER DEFAULT 0,
    crystallized        INTEGER DEFAULT 0,
    vector              BLOB
);

CREATE TABLE IF NOT EXISTS resonance (
    node_a          TEXT,
    node_b          TEXT,
    bond_strength   REAL DEFAULT 1.0,
    PRIMARY KEY (node_a, node_b)
);

CREATE TABLE IF NOT EXISTS retrieval_log (
    session_id      TEXT,
    node_id         TEXT,
    retrieved_at    TEXT
);
"""


class EpisodicStore:
    def __init__(self, db_path: Path):
        db_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.executescript(SCHEMA)
        self.conn.commit()

    def add(self, node: MemoryNode, vector: np.ndarray) -> str:
        node.id = node.id or str(uuid.uuid4())
        self.conn.execute(
            "INSERT OR REPLACE INTO nodes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                node.id, node.content,
                json.dumps(node.keywords),
                node.emotional, node.circumstantial, node.developmental_phase,
                node.mood_tag, node.context_tag, node.domain,
                node.timestamp.isoformat(),
                node.reinforce_count, int(node.crystallized),
                vector.astype(np.float32).tobytes(),
            ),
        )
        self.conn.commit()
        return node.id

    def all_vectors(self) -> tuple[list[str], np.ndarray]:
        rows = self.conn.execute(
            "SELECT id, vector FROM nodes WHERE vector IS NOT NULL"
        ).fetchall()
        if not rows:
            return [], np.empty((0, 388), dtype=np.float32)
        ids = [r[0] for r in rows]
        vecs = np.stack([np.frombuffer(r[1], dtype=np.float32) for r in rows])
        return ids, vecs

    def all_timestamps(self) -> dict[str, datetime]:
        rows = self.conn.execute("SELECT id, timestamp FROM nodes").fetchall()
        return {r[0]: datetime.fromisoformat(r[1]) for r in rows}

    def get(self, node_id: str) -> MemoryNode | None:
        row = self.conn.execute(
            "SELECT * FROM nodes WHERE id=?", (node_id,)
        ).fetchone()
        if not row:
            return None
        return self._row_to_node(row)

    def reinforce(self, node_id: str) -> None:
        self.conn.execute(
            "UPDATE nodes SET reinforce_count = reinforce_count + 1 WHERE id=?",
            (node_id,),
        )
        self.conn.commit()

    def apply_decay(self, rate: float, crystallize_threshold: int) -> None:
        rows = self.conn.execute(
            "SELECT id, reinforce_count FROM nodes"
        ).fetchall()
        for nid, rc in rows:
            if rc >= crystallize_threshold:
                self.conn.execute(
                    "UPDATE nodes SET crystallized=1 WHERE id=?", (nid,)
                )
            else:
                self.conn.execute(
                    """UPDATE nodes SET
                        emotional = emotional * ?,
                        circumstantial = circumstantial * ?
                    WHERE id=? AND crystallized=0""",
                    (rate, rate, nid),
                )
        self.conn.commit()

    def log_retrieval(self, session_id: str, node_ids: list[str]) -> None:
        now = datetime.utcnow().isoformat()
        self.conn.executemany(
            "INSERT INTO retrieval_log VALUES (?,?,?)",
            [(session_id, nid, now) for nid in node_ids],
        )
        self.conn.commit()

    def update_resonance(self, node_ids: list[str]) -> None:
        for i, a in enumerate(node_ids):
            for b in node_ids[i + 1:]:
                key = (min(a, b), max(a, b))
                self.conn.execute(
                    """INSERT INTO resonance (node_a, node_b, bond_strength)
                    VALUES (?,?,1)
                    ON CONFLICT(node_a,node_b)
                    DO UPDATE SET bond_strength = bond_strength + 0.5""",
                    key,
                )
        self.conn.commit()

    def _row_to_node(self, row) -> MemoryNode:
        return MemoryNode(
            id=row[0], content=row[1],
            keywords=json.loads(row[2] or "[]"),
            emotional=row[3], circumstantial=row[4],
            developmental_phase=row[5],
            mood_tag=row[6], context_tag=row[7], domain=row[8],
            timestamp=datetime.fromisoformat(row[9]),
            reinforce_count=row[10],
            crystallized=bool(row[11]),
        )
