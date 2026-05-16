from novacore.models.multimodal import MultimodalGrounder
from novacore.models.long_horizon import LongHorizonController
from novacore.models.policy_formal import PolicyFormalGuarantee
from novacore.models.sota_bench import default_external_suites
from novacore.models.novacore import NovaCoreMini


def test_multimodal_grounding_counts_inputs():
    g = MultimodalGrounder().ground("a b c", {"regions": 2}, {"events": 1})
    assert g.text_tokens == 3 and g.image_regions == 2 and g.tool_signals == 1


def test_long_horizon_halts_if_budget_exceeded():
    h = LongHorizonController(max_steps=2)
    st = h.assess(3)
    assert st.halted is True


def test_policy_formal_blocks_tool_violation():
    p = PolicyFormalGuarantee().verify_tool_policy("halt", allow_tools=True)
    assert p.valid is False


def test_external_suite_present():
    suites = default_external_suites()
    assert len(suites) >= 3


def test_novacore_output_has_new_fields():
    out = NovaCoreMini(max_retries=0).run("STORE_COLOR C1 | QUERY")
    assert isinstance(out.multimodal_tokens, int)
