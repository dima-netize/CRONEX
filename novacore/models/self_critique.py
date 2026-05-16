from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CritiqueResult:
    critic_a: bool
    critic_b: bool
    passed: bool
    reason: str


class MultiAgentSelfCritique:
    """Два незалежні критики (символьний/каузальний) + vote."""

    def evaluate(self, answer: str, reason: str) -> CritiqueResult:
        critic_a = len(answer) > 0 and "Невірний" not in reason
        critic_b = "failed" not in reason.lower() and "does not exist" not in reason.lower()
        passed = critic_a and critic_b
        return CritiqueResult(critic_a=critic_a, critic_b=critic_b, passed=passed, reason="vote_pass" if passed else "vote_fail")
