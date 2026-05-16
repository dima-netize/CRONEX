from novacore.models.novacore import NovaCoreMini


def test_repeat_expansion_long_plan():
    model = NovaCoreMini(max_retries=0)
    out = model.run("STORE_COLOR C1 | REPEAT 3 SHIFT N1 | QUERY")
    assert out.answer == "C4"
    assert out.verified is True


def test_meta_adapter_learns_new_rule_alias():
    model = NovaCoreMini(max_retries=0)
    model.learn_runtime_rule("MOVE", "SHIFT N2")
    out = model.run("STORE_COLOR C1 | MOVE | QUERY")
    assert out.answer == "C3"


def test_safety_blocks_dangerous_program():
    model = NovaCoreMini(max_retries=0)
    out = model.run("STORE_COLOR C1 | DELETE_ALL | QUERY")
    assert out.verified is False
    assert "Blocked token" in out.verifier_reason
