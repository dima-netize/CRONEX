from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class CounterfactualResult:
    action: str
    predicted_effect: str
    risk: float


class CounterfactualWorldModel:
    """Контрфактуальний world-model для оцінки наслідків дій до виконання."""

    def simulate(self, action: str, context: List[str]) -> CounterfactualResult:
        upper = action.upper()
        if "DELETE" in upper or "DROP" in upper:
            return CounterfactualResult(action=action, predicted_effect="destructive_side_effect", risk=0.95)
        if "TOOL_ADD" in upper and "SUM" not in " ".join(context).upper():
            return CounterfactualResult(action=action, predicted_effect="new_memory_write", risk=0.2)
        if "SHIFT" in upper:
            return CounterfactualResult(action=action, predicted_effect="state_transform", risk=0.15)
        return CounterfactualResult(action=action, predicted_effect="unknown", risk=0.35)
