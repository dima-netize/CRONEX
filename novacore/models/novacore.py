from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .causal_model import CausalWorldModel
from .capabilities import default_capabilities
from .error_memory import ErrorMemory
from .memory import WorkingMemory
from .nova_block import HybridNovaBlock
from .neurosymbolic_core import NeuroSymbolicCore
from .meta_adapter import MetaRuleAdapter
from .safety import SafetyGuard
from .governor import PolicyGovernor
from .hierarchical_planner import HierarchicalPlanner
from .tool_sandbox import ToolSandbox
from .uncertainty import UncertaintyCalibrator
from .formal_safety import FormalSafetyVerifier
from .self_critique import MultiAgentSelfCritique
from .lifelong import LifelongAdapter
from .world_model import CounterfactualWorldModel
from .multimodal import MultimodalGrounder
from .long_horizon import LongHorizonController
from .policy_formal import PolicyFormalGuarantee
from .object_parser import ObjectParser
from .operation_engine import OperationEngine
from .planner import Planner
from .repair_policy import LearnedRepairPolicy
from .verifier import Verifier


@dataclass
class NovaCoreOutput:
    answer: str
    verified: bool
    verifier_reason: str
    trace: List[str]
    block_signal: float
    retries_used: int
    final_program: str
    fusion_score: float
    governance_mode: str
    confidence_lower: float
    confidence_upper: float
    drift_score: float
    safety_proof: str
    critique_passed: bool
    horizon_reason: str
    multimodal_tokens: int
    tool_policy_proof: str


class NovaCoreMini:
    def __init__(self, max_retries: int = 1) -> None:
        self.parser = ObjectParser()
        self.planner = Planner()
        self.engine = OperationEngine()
        self.verifier = Verifier()
        self.error_memory = ErrorMemory()
        self.nova_block = HybridNovaBlock()
        self.max_retries = max_retries
        self.repair_policy = LearnedRepairPolicy()
        self.safety_guard = SafetyGuard()
        self.meta_adapter = MetaRuleAdapter()
        self.ns_core = NeuroSymbolicCore()
        self.governor = PolicyGovernor()
        self.h_planner = HierarchicalPlanner()
        self.tool_sandbox = ToolSandbox()
        self.calibrator = UncertaintyCalibrator()
        self.world_model = CounterfactualWorldModel()
        self.lifelong = LifelongAdapter()
        self.critique = MultiAgentSelfCritique()
        self.formal_safety = FormalSafetyVerifier()
        self.multimodal = MultimodalGrounder()
        self.horizon = LongHorizonController(max_steps=2000)
        self.policy_formal = PolicyFormalGuarantee()

    def describe_capabilities(self) -> list[str]:
        return [f"{c.name}: {c.description} (Для чого: {c.use_case})" for c in default_capabilities()]

    def _run_once(self, program: str) -> tuple[str, List[str], bool, str, float, float, bool, str, int, str]:
        memory = WorkingMemory()
        causal_model = CausalWorldModel()

        guard = self.safety_guard.check(program)
        if not guard.allowed:
            return "", [f"SAFETY: {guard.reason}"], False, guard.reason, 0.0, 0.0, False, guard.reason, 0, "tool_policy_ok"

        mm = self.multimodal.ground(program, image_stub={"regions": 0}, tool_stub={"events": 0})
        normalized_program = " | ".join(self.meta_adapter.map_token(x.strip()) for x in program.split("|") if x.strip())
        ops = self.parser.parse(normalized_program)
        hierarchical = self.h_planner.build(ops)
        flat_ops = [op for sg in hierarchical.subgoals for op in sg.steps]
        plan = self.planner.create_plan(flat_ops)

        horizon_state = self.horizon.assess(used_steps=len(plan.steps))
        if horizon_state.halted:
            return "", [], False, horizon_state.reason, 0.0, 0.0, True, horizon_state.reason, mm.text_tokens, "tool_policy_ok"

        answer = ""
        trace: List[str] = []
        tool_policy_detail = "tool_policy_ok"
        try:
            for op in plan.steps:
                cf = self.world_model.simulate(op.name + " " + " ".join(op.args), context=trace)
                if cf.risk > 0.9:
                    raise PermissionError(f"Counterfactual risk too high: {cf.predicted_effect}")
                policy = self.tool_sandbox.policy_for_mode("normal")
                policy_proof = self.policy_formal.verify_tool_policy("normal", policy.allow_tool_add)
                tool_policy_detail = policy_proof.detail
                if not policy_proof.valid:
                    raise PermissionError(policy_proof.detail)
                result = self.engine.run(op, memory, causal_model, allow_tools=policy.allow_tool_add)
                trace.append(f"{op.name}: {result.message}")
                if op.name == "QUERY":
                    answer = result.message

            result = self.verifier.verify(answer, memory, causal_model)
            passed, reason = result.passed, result.reason
        except Exception as exc:  # noqa: BLE001
            passed, reason = False, str(exc)

        memory_density = min(1.0, len(list(memory.keys())) / 10.0)
        block_metrics = self.nova_block.forward(tokens=normalized_program.split(), memory_density=memory_density)
        symbolic_facts = {k: str(memory.read(k).value) for k in memory.keys()}
        fused = self.ns_core.fuse(tokens=normalized_program.split(), symbolic_facts=symbolic_facts)
        return answer, trace, passed, reason, block_metrics.mixed_signal, fused.fusion_score, True, horizon_state.reason, mm.text_tokens, tool_policy_detail

    def learn_runtime_rule(self, alias: str, canonical: str) -> str:
        result = self.meta_adapter.learn_rule(alias, canonical)
        return result.reason

    def run(self, program: str) -> NovaCoreOutput:
        retries = 0
        current_program = program
        answer, trace, passed, reason, signal, fusion, safety_ok, horizon_reason, mm_tokens, tool_policy = self._run_once(current_program)
        while not passed and retries < self.max_retries:
            retries += 1
            self.error_memory.add(tag="verification_failed", detail=reason)
            repair = self.repair_policy.repair(current_program, reason)
            self.error_memory.add(tag="repair_applied", detail=repair.reason)
            current_program = repair.repaired_program
            answer, trace, passed, reason, signal, fusion, safety_ok, horizon_reason, mm_tokens, tool_policy = self._run_once(current_program)
            self.repair_policy.update("inject_store_color", passed)
            self.lifelong.update_rule_outcome("inject_store_color", passed)

        if not passed:
            self.error_memory.add(tag="final_failure", detail=reason)

        ci = self.calibrator.calibrate(fusion_score=fusion, retries_used=retries, trace_len=len(trace))
        decision = self.governor.decide(fusion_score=ci.mean, retries_used=retries, safety_ok=safety_ok)
        safety_proof = self.formal_safety.verify(current_program, decision.mode)
        critique = self.critique.evaluate(answer=answer, reason=reason)
        drift = self.lifelong.drift_report()

        return NovaCoreOutput(
            answer=answer,
            verified=passed,
            verifier_reason=reason,
            trace=trace,
            block_signal=signal,
            retries_used=retries,
            final_program=current_program,
            fusion_score=fusion,
            governance_mode=decision.mode,
            confidence_lower=ci.lower,
            confidence_upper=ci.upper,
            drift_score=drift.drift_score,
            safety_proof=safety_proof.proof,
            critique_passed=critique.passed,
            horizon_reason=horizon_reason,
            multimodal_tokens=mm_tokens,
            tool_policy_proof=tool_policy,
        )
