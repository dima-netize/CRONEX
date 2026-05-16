from __future__ import annotations

from dataclasses import dataclass


@dataclass
class GovernanceDecision:
    mode: str
    reason: str


class PolicyGovernor:
    """Керує режимом виконання: normal / cautious / halt."""

    def decide(self, fusion_score: float, retries_used: int, safety_ok: bool) -> GovernanceDecision:
        if not safety_ok:
            return GovernanceDecision("halt", "safety violation")
        if retries_used >= 2 or fusion_score < 0.45:
            return GovernanceDecision("cautious", "low confidence or many retries")
        return GovernanceDecision("normal", "stable execution")
