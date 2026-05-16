from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ExternalBenchmarkSuite:
    name: str
    tasks: List[str]


def default_external_suites() -> List[ExternalBenchmarkSuite]:
    return [
        ExternalBenchmarkSuite("SWE-bench (proxy)", ["code_repair", "test_fixing"]),
        ExternalBenchmarkSuite("MMLU-like (proxy)", ["broad_knowledge", "reasoning"]),
        ExternalBenchmarkSuite("Agent safety eval (proxy)", ["policy_refusal", "tool_misuse"]),
    ]
