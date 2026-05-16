from novacore.models.novacore import NovaCoreMini


def test_core_regression_guard_suite():
    model = NovaCoreMini(max_retries=1)
    cases = [
        ("STORE_COLOR C1 | SHIFT N2 | QUERY", "C3", True),
        ("PAIR S3 C7 | QUERY S3", "C7", True),
        ("DELETE_ALL | QUERY", "", False),
    ]
    for program, answer, verified in cases:
        out = model.run(program)
        assert out.answer == answer
        assert out.verified is verified
