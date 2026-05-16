from novacore.models.novacore import NovaCoreMini


def test_weighted_verifier_returns_score():
    out = NovaCoreMini(max_retries=0).run("STORE_COLOR C1 | SHIFT N1 | QUERY")
    assert out.verified is True
