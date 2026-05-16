from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PolicyProof:
    valid: bool
    detail: str


class PolicyFormalGuarantee:
    """Формальна перевірка інструментальних політик."""

    def verify_tool_policy(self, governance_mode: str, allow_tools: bool) -> PolicyProof:
        if governance_mode in {"halt", "cautious"} and allow_tools:
            return PolicyProof(False, "tool_policy_violation")
        return PolicyProof(True, "tool_policy_ok")
