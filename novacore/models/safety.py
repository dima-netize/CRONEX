from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SafetyResult:
    allowed: bool
    reason: str


class SafetyGuard:
    """Системна безпека: блокує небезпечні/некоректні патерни програм."""

    blocked_tokens = {"DELETE_ALL", "FORMAT_DISK", "DROP_DB"}

    def check(self, program: str) -> SafetyResult:
        upper = program.upper()
        for token in self.blocked_tokens:
            if token in upper:
                return SafetyResult(False, f"Blocked token detected: {token}")
        # Піднято ліміт для long-horizon сценаріїв.
        if len(program) > 20000:
            return SafetyResult(False, "Program too long for safe execution")
        return SafetyResult(True, "ok")
