from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .object_parser import Operation


@dataclass
class SubGoal:
    name: str
    steps: List[Operation]


@dataclass
class HierarchicalPlan:
    goal: str
    subgoals: List[SubGoal]


class HierarchicalPlanner:
    """Декомпозиція цілі на підцілі з контрольованими підпланами."""

    def build(self, ops: List[Operation]) -> HierarchicalPlan:
        setup = [op for op in ops if op.name in {"STORE_COLOR", "PAIR", "TOOL_ADD"}]
        transform = [op for op in ops if op.name in {"SHIFT", "IF_SHIFT_GT", "REPEAT"}]
        query = [op for op in ops if op.name == "QUERY"]
        subgoals = [
            SubGoal("setup_state", setup),
            SubGoal("transform_state", transform),
            SubGoal("emit_answer", query),
        ]
        return HierarchicalPlan(goal="solve_program", subgoals=subgoals)
