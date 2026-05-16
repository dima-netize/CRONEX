from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Capability:
    name: str
    description: str
    use_case: str


def default_capabilities() -> List[Capability]:
    return [
        Capability(
            name="Object Parsing",
            description="Розбирає DSL-програми на структуровані операції.",
            use_case="Перетворення текстової задачі у виконуваний план.",
        ),
        Capability(
            name="Working Memory",
            description="Зберігає факти та проміжні стани в явних комірках.",
            use_case="Стабільне compositional-обчислення без втрати контексту.",
        ),
        Capability(
            name="Causal Trace",
            description="Записує причинно-наслідковий слід кожної операції.",
            use_case="Дебаг рішень і перевірка пояснюваності відповіді.",
        ),
        Capability(
            name="Verification",
            description="Перевіряє формат, узгодженість і groundedness відповіді.",
            use_case="Зменшення впевнених помилок перед фінальним output.",
        ),
        Capability(
            name="Hybrid Signal",
            description="Обчислює сигнал гібридного блока attention/state/memory.",
            use_case="Базова метрика для майбутнього neural routing.",
        ),
    ]
