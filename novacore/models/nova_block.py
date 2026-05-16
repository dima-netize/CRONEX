from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class NovaBlockOutput:
    mixed_signal: float
    attention_score: float
    state_score: float
    memory_score: float


class HybridNovaBlock:
    """Спрощений прототип гібридного блока: attention + state + memory router."""

    def __init__(self, attention_weight: float = 0.5, state_weight: float = 0.3, memory_weight: float = 0.2) -> None:
        total = attention_weight + state_weight + memory_weight
        if abs(total - 1.0) > 1e-6:
            raise ValueError("Сума ваг HybridNovaBlock має дорівнювати 1.0")
        self.attention_weight = attention_weight
        self.state_weight = state_weight
        self.memory_weight = memory_weight

    def forward(self, tokens: List[str], memory_density: float) -> NovaBlockOutput:
        token_count = max(1, len(tokens))
        attention_score = min(1.0, token_count / 10.0)
        state_score = min(1.0, len(set(tokens)) / token_count)
        memory_score = max(0.0, min(1.0, memory_density))

        mixed = (
            attention_score * self.attention_weight
            + state_score * self.state_weight
            + memory_score * self.memory_weight
        )

        return NovaBlockOutput(
            mixed_signal=round(mixed, 4),
            attention_score=round(attention_score, 4),
            state_score=round(state_score, 4),
            memory_score=round(memory_score, 4),
        )
