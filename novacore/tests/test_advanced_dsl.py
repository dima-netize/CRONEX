from novacore.models.novacore import NovaCoreMini


def test_if_branch_applies_store_color():
    model = NovaCoreMini(max_retries=0)
    out = model.run("STORE_COLOR C1 | SHIFT N3 | IF_SHIFT_GT 2 STORE_COLOR C9 | QUERY")
    assert out.answer == "C12"
    assert out.verified is True


def test_tool_add_and_query_memory_key():
    model = NovaCoreMini(max_retries=0)
    out = model.run("TOOL_ADD 2 3 SUM | QUERY SUM")
    assert out.answer == "5"
    assert out.verified is True
