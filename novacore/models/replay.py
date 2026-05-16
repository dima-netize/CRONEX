from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ReplayItem:
    task: str
    success: bool
    priority: float = 1.0
    tags: list[str] = field(default_factory=list)


class ExperienceReplayStore:
    def __init__(self, capacity: int = 500) -> None:
        self.capacity = capacity
        self.items: list[ReplayItem] = []

    def add(self, task: str, success: bool, priority: float = 1.0, tags: list[str] | None = None) -> None:
        self.items.append(ReplayItem(task=task, success=success, priority=priority, tags=tags or []))
        if len(self.items) > self.capacity:
            # drop lowest-priority oldest item
            min_idx = min(range(len(self.items)), key=lambda i: (self.items[i].priority, i))
            self.items.pop(min_idx)

    def success_rate(self) -> float:
        if not self.items:
            return 0.0
        return sum(int(x.success) for x in self.items) / len(self.items)

    def weighted_success_rate(self) -> float:
        if not self.items:
            return 0.0
        wsum = sum(x.priority for x in self.items)
        if wsum <= 0:
            return 0.0
        return sum((1.0 if x.success else 0.0) * x.priority for x in self.items) / wsum

    def top_hard_errors(self, limit: int = 10) -> list[ReplayItem]:
        failed = [x for x in self.items if not x.success]
        failed.sort(key=lambda x: x.priority, reverse=True)
        return failed[:limit]
