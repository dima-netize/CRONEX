from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RepairAction:
    repaired_program: str
    reason: str


class LearnedRepairPolicy:
    """Спрощена learned-like policy: підсилює дії, що раніше виправляли збої."""

    def __init__(self) -> None:
        self.weights = {
            "inject_store_color": 0.7,
            "inject_query": 0.4,
            "noop": 0.2,
        }

    def update(self, action: str, success: bool) -> None:
        delta = 0.1 if success else -0.05
        self.weights[action] = max(0.0, min(1.0, self.weights.get(action, 0.1) + delta))

    def repair(self, program: str, verifier_reason: str) -> RepairAction:
        steps = [chunk.strip() for chunk in program.split("|") if chunk.strip()]

        candidates = []
        if "base_color" in verifier_reason or "does not exist" in verifier_reason:
            candidates.append("inject_store_color")
        if not any(step.startswith("QUERY") for step in steps):
            candidates.append("inject_query")
        candidates.append("noop")

        best = max(candidates, key=lambda c: self.weights.get(c, 0.0))

        if best == "inject_store_color":
            repaired = ["STORE_COLOR C0", *steps]
            return RepairAction(" | ".join(repaired), "learned inject_store_color")
        if best == "inject_query":
            repaired = [*steps, "QUERY"]
            return RepairAction(" | ".join(repaired), "learned inject_query")
        return RepairAction(program, "learned noop")
