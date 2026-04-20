from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CorpusSource:
    path: Path
    source_file: str
    source_type: str

