from novacore.models.benchmark_protocol import ExternalBenchmarkProtocol
from novacore.training.l5_upgrade_report import assess_l5_candidate


def test_protocol_full_coverage_ok():
    p = ExternalBenchmarkProtocol().evaluate(
        ["SWE-bench (proxy)", "MMLU-like (proxy)", "Agent safety eval (proxy)"],
        seed=42,
        safety_cases=2,
        total_cases=5,
    )
    assert p.reproducible is True
    assert p.benchmark_coverage == 1.0


def test_l5_candidate_gate():
    m = assess_l5_candidate(0.96, True, True, True)
    assert m.level == "L5-Candidate-Experimental"
