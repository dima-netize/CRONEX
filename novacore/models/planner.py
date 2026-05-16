from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .object_parser import Operation


@dataclass
class Plan:
    steps: List[Operation]


class Planner:
    """Long-horizon planner: нормалізація + розгортка складних кроків."""

    def create_plan(self, ops: List[Operation]) -> Plan:
        expanded: List[Operation] = []
        for op in ops:
            if op.name == "REPEAT" and len(op.args) >= 2:
                n = int(op.args[0])
                nested_name = op.args[1].upper()
                nested_args = op.args[2:]
                for _ in range(max(0, n)):
                    expanded.append(Operation(name=nested_name, args=nested_args))
            else:
                expanded.append(op)

        no_query = [op for op in expanded if op.name != "QUERY"]
        queries = [op for op in expanded if op.name == "QUERY"]
        return Plan(steps=[*no_query, *queries])
