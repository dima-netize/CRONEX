from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class DriftReport:
    drift_score: float
    exceeds_threshold: bool


class LifelongAdapter:
    """Lifelong adaptation + drift monitor."""

    def __init__(self, drift_threshold: float = 0.35) -> None:
        self.rule_success: Dict[str, int] = {}
        self.rule_fail: Dict[str, int] = {}
        self.drift_threshold = drift_threshold

    def update_rule_outcome(self, rule: str, success: bool) -> None:
        key = rule.upper()
        if success:
            self.rule_success[key] = self.rule_success.get(key, 0) + 1
        else:
            self.rule_fail[key] = self.rule_fail.get(key, 0) + 1

    def drift_report(self) -> DriftReport:
        total_success = sum(self.rule_success.values())
        total_fail = sum(self.rule_fail.values())
        total = total_success + total_fail
        if total == 0:
            return DriftReport(0.0, False)
        drift = total_fail / total
        return DriftReport(drift_score=round(drift, 4), exceeds_threshold=drift > self.drift_threshold)
