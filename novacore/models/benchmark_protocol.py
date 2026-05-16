from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class ProtocolResult:
    reproducible: bool
    safety_coverage: float
    benchmark_coverage: float
    note: str


class ExternalBenchmarkProtocol:
    """Відтворюваний протокол оцінки (seed + safety + coverage)."""

    required_suites = {"SWE-bench (proxy)", "MMLU-like (proxy)", "Agent safety eval (proxy)"}

    def evaluate(self, suite_names: Iterable[str], seed: int, safety_cases: int, total_cases: int) -> ProtocolResult:
        suite_set = set(suite_names)
        coverage = len(self.required_suites.intersection(suite_set)) / len(self.required_suites)
        safety_cov = 0.0 if total_cases == 0 else min(1.0, safety_cases / total_cases)
        reproducible = seed == 42
        note = "ok" if reproducible and coverage >= 1.0 else "incomplete_protocol"
        return ProtocolResult(
            reproducible=reproducible,
            safety_coverage=round(safety_cov, 4),
            benchmark_coverage=round(coverage, 4),
            note=note,
        )
