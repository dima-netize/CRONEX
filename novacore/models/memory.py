from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class MemoryCell:
    key: str
    type: str
    value: Any
    provenance: str = "parser"
    confidence: float = 1.0
    ttl: int = 10
    links: Dict[str, List[str]] = field(default_factory=dict)


class WorkingMemory:
    def __init__(self) -> None:
        self._cells: Dict[str, MemoryCell] = {}

    def write(self, cell: MemoryCell) -> None:
        self._cells[cell.key] = cell

    def update(self, key: str, value: Any, confidence: Optional[float] = None) -> None:
        if key not in self._cells:
            raise KeyError(f"Cell '{key}' does not exist")
        self._cells[key].value = value
        if confidence is not None:
            self._cells[key].confidence = confidence

    def read(self, key: str) -> MemoryCell:
        if key not in self._cells:
            raise KeyError(f"Cell '{key}' does not exist")
        return self._cells[key]

    def exists(self, key: str) -> bool:
        return key in self._cells

    def link(self, key_a: str, relation: str, key_b: str) -> None:
        a = self.read(key_a)
        self.read(key_b)
        a.links.setdefault(relation, []).append(key_b)

    def evict(self) -> None:
        dead: List[str] = []
        for key, cell in self._cells.items():
            cell.ttl -= 1
            if cell.ttl <= 0:
                dead.append(key)
        for key in dead:
            del self._cells[key]

    def keys(self) -> Iterable[str]:
        return self._cells.keys()


    def prune(self, min_confidence: float = 0.2) -> int:
        to_remove = [k for k, c in self._cells.items() if c.confidence < min_confidence]
        for k in to_remove:
            del self._cells[k]
        return len(to_remove)
