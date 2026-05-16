from novacore.models.novacore import NovaCoreMini


def test_no_catastrophic_forgetting_on_small_shift():
    model = NovaCoreMini(max_retries=1)
    base = ["STORE_COLOR C1 | SHIFT N2 | QUERY", "PAIR S1 C5 | QUERY S1"]
    before = sum(int(model.run(x).verified) for x in base) / len(base)
    model.run("STORE_COLOR C2 | REPEAT 15 SHIFT N1 | QUERY")
    after = sum(int(model.run(x).verified) for x in base) / len(base)
    assert (before - after) <= 0.02
