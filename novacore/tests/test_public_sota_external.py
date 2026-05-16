from novacore.models.public_sota import PublicSOTAProtocolRunner


def test_external_fixture_files_are_readable():
    runner = PublicSOTAProtocolRunner()
    swe = runner.run_jsonl("SWE-bench", "external/swe_bench.jsonl")
    mmlu = runner.run_jsonl("MMLU", "external/mmlu.jsonl")
    safe = runner.run_jsonl("AgentSafety", "external/agent_safety.jsonl")

    assert swe.available and swe.total >= 20
    assert mmlu.available and mmlu.total >= 20
    assert safe.available and safe.total >= 20
