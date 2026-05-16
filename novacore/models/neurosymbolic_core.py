from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class NeuroSymbolicState:
    neural_score: float
    symbolic_score: float
    fusion_score: float


class NeuroSymbolicCore:
    """Єдине neural-symbolic ядро: узгоджує нейронний та символьний сигнали."""

    def fuse(self, tokens: List[str], symbolic_facts: Dict[str, str]) -> NeuroSymbolicState:
        token_diversity = len(set(tokens)) / max(1, len(tokens))
        neural_score = min(1.0, 0.4 + 0.6 * token_diversity)
        symbolic_score = min(1.0, 0.3 + 0.1 * len(symbolic_facts))
        fusion = round((0.55 * neural_score + 0.45 * symbolic_score), 4)
        return NeuroSymbolicState(
            neural_score=round(neural_score, 4),
            symbolic_score=round(symbolic_score, 4),
            fusion_score=fusion,
        )
