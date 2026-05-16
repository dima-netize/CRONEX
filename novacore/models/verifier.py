from __future__ import annotations

from dataclasses import dataclass

from .causal_model import CausalWorldModel
from .memory import WorkingMemory


@dataclass
class VerificationResult:
    passed: bool
    reason: str
    score: float


class Verifier:
    def verify(self, answer: str, memory: WorkingMemory, causal_model: CausalWorldModel) -> VerificationResult:
        checks = [
            (self._causal_check(memory, causal_model), 0.35),
            (self._format_and_consistency_check(answer, memory), 0.45),
            (self._trace_grounding_check(answer, causal_model), 0.20),
        ]

        score = 0.0
        failed = []
        for res, w in checks:
            if res.passed:
                score += w
            else:
                failed.append(res.reason)

        if failed:
            return VerificationResult(False, " | ".join(failed), round(score, 4))
        return VerificationResult(True, "ok", round(score, 4))

    def _causal_check(self, memory: WorkingMemory, causal_model: CausalWorldModel) -> VerificationResult:
        issues = causal_model.validate_memory_state(memory)
        if issues:
            return VerificationResult(False, f"Causal check failed: {', '.join(issues)}", 0.0)
        return VerificationResult(True, "ok", 1.0)

    def _format_and_consistency_check(self, answer: str, memory: WorkingMemory) -> VerificationResult:
        if answer.startswith("C"):
            try:
                int(answer[1:])
            except ValueError:
                return VerificationResult(False, "Невалідний формат кольору", 0.0)

            if memory.exists("base_color") and memory.exists("total_shift"):
                base = int(memory.read("base_color").value[1:])
                shift = memory.read("total_shift").value
                expected = f"C{base + shift}"
                if answer != expected:
                    return VerificationResult(False, f"Очікувалось {expected}", 0.0)

        return VerificationResult(True, "ok", 1.0)

    def _trace_grounding_check(self, answer: str, causal_model: CausalWorldModel) -> VerificationResult:
        if answer.startswith("S") and not any(ev.effect.endswith(f"->{answer}") for ev in causal_model.events):
            return VerificationResult(False, "Відповідь S* не підтверджена причинним слідом", 0.0)
        if answer.startswith("C"):
            has_color_trace = any("color=" in ev.effect for ev in causal_model.events)
            has_binding_trace = any(ev.effect.endswith(f"->{answer}") for ev in causal_model.events)
            if not has_color_trace and not has_binding_trace:
                return VerificationResult(False, "Відповідь C* не підтверджена причинним слідом", 0.0)
        return VerificationResult(True, "ok", 1.0)
