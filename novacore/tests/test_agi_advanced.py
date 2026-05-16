from novacore.models.novacore import NovaCoreMini
from novacore.models.formal_safety import FormalSafetyVerifier
from novacore.models.world_model import CounterfactualWorldModel


def test_counterfactual_blocks_destructive_action():
    wm = CounterfactualWorldModel()
    r = wm.simulate("DELETE_ALL", [])
    assert r.risk > 0.9


def test_formal_safety_proof_has_invariants():
    proof = FormalSafetyVerifier().verify("DELETE_ALL", "halt")
    assert "inv1=" in proof.proof


def test_novacore_outputs_advanced_fields():
    out = NovaCoreMini(max_retries=0).run("STORE_COLOR C1 | QUERY")
    assert isinstance(out.drift_score, float)
    assert isinstance(out.safety_proof, str)
    assert isinstance(out.critique_passed, bool)
