from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SafetyProof:
    valid: bool
    proof: str


class FormalSafetyVerifier:
    """Формалізована safety-перевірка інваріантів виконання."""

    def verify(self, program: str, governance_mode: str) -> SafetyProof:
        p = program.upper()
        inv1 = not ("DELETE_ALL" in p and governance_mode != "halt")
        inv2 = not ("DROP_DB" in p and governance_mode != "halt")
        inv3 = len(program) <= 20000
        # tool preconditions
        inv4 = ("TOOL_ADD" not in p) or ("QUERY" in p)
        # postconditions: if query exists, program should define some state
        inv5 = ("QUERY" not in p) or any(tok in p for tok in ["STORE_COLOR", "PAIR", "TOOL_ADD", "SHIFT", "REPEAT"])
        # forbidden transitions
        inv6 = not ("DELETE_ALL" in p and "TOOL_ADD" in p)
        valid = all([inv1, inv2, inv3, inv4, inv5, inv6])
        proof = f"inv1={inv1};inv2={inv2};inv3={inv3};inv4={inv4};inv5={inv5};inv6={inv6}"
        return SafetyProof(valid=valid, proof=proof)
