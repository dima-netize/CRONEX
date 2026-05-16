from novacore.models.novacore import NovaCoreMini


def test_repair_policy_injects_store_color_when_missing():
    model = NovaCoreMini(max_retries=1)
    out = model.run("QUERY")
    assert out.verified is True
    assert out.answer == "C0"
    assert out.retries_used == 1
    assert out.final_program.startswith("STORE_COLOR C0")
