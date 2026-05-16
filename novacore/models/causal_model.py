from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .memory import WorkingMemory


@dataclass
class CausalEvent:
    cause: str
    effect: str
    confidence: float = 1.0


class CausalWorldModel:
    """Мінімальна причинна модель для трасування наслідків дій."""

    def __init__(self) -> None:
        self.events: List[CausalEvent] = []

    def clear(self) -> None:
        self.events.clear()

    def record(self, cause: str, effect: str, confidence: float = 1.0) -> None:
        self.events.append(CausalEvent(cause=cause, effect=effect, confidence=confidence))

    def validate_memory_state(self, memory: WorkingMemory) -> List[str]:
        issues: List[str] = []
        if memory.exists("base_color") and not memory.read("base_color").value.startswith("C"):
            issues.append("base_color має невалідний формат")
        if memory.exists("total_shift") and not isinstance(memory.read("total_shift").value, int):
            issues.append("total_shift має бути int")
        return issues
