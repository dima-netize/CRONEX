from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ErrorRecord:
    tag: str
    detail: str


class ErrorMemory:
    """Пам'ять типових помилок для подальшого аналізу та автопокращення."""

    def __init__(self) -> None:
        self._records: List[ErrorRecord] = []
        self._counter: Counter[str] = Counter()

    def add(self, tag: str, detail: str) -> None:
        self._records.append(ErrorRecord(tag=tag, detail=detail))
        self._counter[tag] += 1

    def top_tags(self, limit: int = 3) -> Dict[str, int]:
        return dict(self._counter.most_common(limit))

    def records(self) -> List[ErrorRecord]:
        return list(self._records)
