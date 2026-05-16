from pathlib import Path

from novacore.models.public_sota import PublicSOTAProtocolRunner


def test_public_sota_unavailable(tmp_path: Path):
    res = PublicSOTAProtocolRunner().run_jsonl("X", str(tmp_path / "missing.jsonl"))
    assert res.available is False


def test_public_sota_reads_jsonl(tmp_path: Path):
    f = tmp_path / "suite.jsonl"
    f.write_text('{"passed": true}\n{"passed": false}\n', encoding="utf-8")
    res = PublicSOTAProtocolRunner().run_jsonl("X", str(f))
    assert res.available is True
    assert res.total == 2
    assert res.passed == 1
