from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvalMetrics:
    total: int
    verified: int
    accuracy: float
    avg_retries: float


def compute_metrics(total: int, verified: int, retries_sum: int) -> EvalMetrics:
    if total <= 0:
        return EvalMetrics(total=0, verified=0, accuracy=0.0, avg_retries=0.0)
    return EvalMetrics(
        total=total,
        verified=verified,
        accuracy=round(verified / total, 4),
        avg_retries=round(retries_sum / total, 4),
    )
