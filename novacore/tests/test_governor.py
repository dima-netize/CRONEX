from novacore.models.novacore import NovaCoreMini


def test_governance_mode_present():
    model = NovaCoreMini(max_retries=0)
    out = model.run("STORE_COLOR C1 | QUERY")
    assert out.governance_mode in {"normal", "cautious", "halt"}


def test_safety_sets_halt_mode():
    model = NovaCoreMini(max_retries=0)
    out = model.run("DELETE_ALL")
    assert out.governance_mode == "halt"
