from novacore.models.novacore import NovaCoreMini


def test_long_horizon_repeat_1000_passes():
    model = NovaCoreMini(max_retries=1)
    out = model.run("STORE_COLOR C1 | REPEAT 1000 SHIFT N1 | QUERY")
    assert out.verified is True
    assert out.governance_mode == "normal"
    assert out.answer == "C1001"
