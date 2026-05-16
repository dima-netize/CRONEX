from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AGIReadiness:
    memory_score: float
    planning_score: float
    verification_score: float
    tool_use_score: float
    adaptation_score: float

    @property
    def overall(self) -> float:
        return round(
            (self.memory_score + self.planning_score + self.verification_score + self.tool_use_score + self.adaptation_score)
            / 5.0,
            4,
        )


def estimate_agi_readiness(
    has_working_memory: bool,
    has_branching: bool,
    has_verifier: bool,
    has_tool_use: bool,
    has_learned_repair: bool,
) -> AGIReadiness:
    return AGIReadiness(
        memory_score=1.0 if has_working_memory else 0.2,
        planning_score=0.8 if has_branching else 0.4,
        verification_score=0.9 if has_verifier else 0.3,
        tool_use_score=0.8 if has_tool_use else 0.2,
        adaptation_score=0.8 if has_learned_repair else 0.2,
    )
