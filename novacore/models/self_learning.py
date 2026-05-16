from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class LearningState:
    strengths: Dict[str, float]


class SelfLearningController:
    """Self-learning з контрольованим forgetting (bounded decay)."""

    def __init__(self, decay: float = 0.02) -> None:
        self.decay = decay
        self.strengths: Dict[str, float] = {}

    def reinforce(self, skill: str, reward: float) -> None:
        cur = self.strengths.get(skill, 0.5)
        self.strengths[skill] = max(0.0, min(1.0, cur + reward))

    def controlled_forgetting(self) -> None:
        for k, v in list(self.strengths.items()):
            self.strengths[k] = max(0.1, v - self.decay)

    def state(self) -> LearningState:
        return LearningState(strengths=dict(self.strengths))
