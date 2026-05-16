from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class ToolchainSafetyReport:
    valid: bool
    violated_rules: list[str]


class ToolchainSafetyVerifier:
    """Формальні safety-гарантії для всього toolchain."""

    required_rules = ("sandbox_enabled", "policy_checked", "audit_log")

    def verify(self, active_rules: Iterable[str]) -> ToolchainSafetyReport:
        active = set(active_rules)
        violated = [r for r in self.required_rules if r not in active]
        return ToolchainSafetyReport(valid=len(violated) == 0, violated_rules=violated)
