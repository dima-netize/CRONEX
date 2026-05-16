from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HorizonStatus:
    max_steps: int
    used_steps: int
    halted: bool
    reason: str


class LongHorizonController:
    """Контролює довгі автономні горизонти виконання."""

    def __init__(self, max_steps: int = 1000) -> None:
        self.max_steps = max_steps

    def assess(self, used_steps: int) -> HorizonStatus:
        if used_steps > self.max_steps:
            return HorizonStatus(self.max_steps, used_steps, True, "step_budget_exceeded")
        return HorizonStatus(self.max_steps, used_steps, False, "ok")
