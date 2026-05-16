from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from novacore.models.public_sota import PublicSOTAProtocolRunner


if __name__ == "__main__":
    sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True).strip()
    runner = PublicSOTAProtocolRunner()
    suites = [
        ("SWE-bench", "external/swe_bench.jsonl"),
        ("MMLU", "external/mmlu.jsonl"),
        ("AgentSafety", "external/agent_safety.jsonl"),
    ]

    results = []
    total = passed = 0
    for name, path in suites:
        r = runner.run_jsonl(name, path)
        rate = 0.0 if r.total == 0 else round(r.passed / r.total, 4)
        total += r.total
        passed += r.passed
        results.append({"suite": name, "path": path, "total": r.total, "passed": r.passed, "rate": rate, "available": r.available})

    bundle = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "commit": sha,
        "seed": 42,
        "config": {"max_retries": 1},
        "aggregate_rate": 0.0 if total == 0 else round(passed / total, 4),
        "results": results,
    }

    outdir = Path("artifacts")
    outdir.mkdir(exist_ok=True)
    out = outdir / "protocol_bundle.json"
    out.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    print(out)
    print(json.dumps(bundle, ensure_ascii=False, indent=2))
