from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class AdaptationResult:
    changed: bool
    reason: str


class MetaRuleAdapter:
    """Швидка адаптація до нових правил через lightweight runtime-override."""

    def __init__(self) -> None:
        self.shift_aliases: Dict[str, str] = {}

    def learn_rule(self, alias: str, canonical: str) -> AdaptationResult:
        self.shift_aliases[alias.upper()] = canonical.upper()
        return AdaptationResult(True, f"learned {alias}->{canonical}")

    def map_token(self, token: str) -> str:
        return self.shift_aliases.get(token.upper(), token)
