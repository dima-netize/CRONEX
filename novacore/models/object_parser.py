from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Operation:
    name: str
    args: List[str]


class ObjectParser:
    """Парсер DSL для NovaCore Mini."""

    def parse(self, program: str) -> List[Operation]:
        ops: List[Operation] = []
        for raw in [chunk.strip() for chunk in program.split("|") if chunk.strip()]:
            parts = raw.split()
            ops.append(Operation(name=parts[0].upper(), args=parts[1:]))
        return ops
