from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AGIMaturity:
    level: str
    score: float
    interpretation: str


def classify_maturity(score: float) -> AGIMaturity:
    s = max(0.0, min(1.0, score))
    if s < 0.35:
        return AGIMaturity("L1-Prototype", s, "Базовий прототип, вузькі задачі")
    if s < 0.55:
        return AGIMaturity("L2-Structured", s, "Структуроване мислення у вузькому домені")
    if s < 0.75:
        return AGIMaturity("L3-Agentic", s, "Агентні контури, але обмежене узагальнення")
    if s < 0.9:
        return AGIMaturity("L4-Pre-AGI", s, "Сильний pre-AGI каркас без універсального інтелекту")
    return AGIMaturity("L5-AGI-Ready", s, "Майже AGI-рівень, потребує зовнішньої валідації")
