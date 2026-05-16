from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass
class ConfidenceInterval:
    mean: float
    lower: float
    upper: float


class UncertaintyCalibrator:
    """Калібрує довіру через інтервал, а не тільки raw threshold."""

    def calibrate(self, fusion_score: float, retries_used: int, trace_len: int) -> ConfidenceInterval:
        mean = max(0.0, min(1.0, fusion_score - 0.05 * retries_used + 0.01 * min(trace_len, 10)))
        variance = max(0.01, 0.15 - 0.02 * min(trace_len, 5) + 0.03 * retries_used)
        std = math.sqrt(variance)
        lower = max(0.0, mean - 1.96 * std)
        upper = min(1.0, mean + 1.96 * std)
        return ConfidenceInterval(round(mean, 4), round(lower, 4), round(upper, 4))
