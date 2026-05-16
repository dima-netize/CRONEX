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
        runner.run_jsonl("SWE-bench", "external/swe_bench.jsonl"),
        runner.run_jsonl("MMLU", "external/mmlu.jsonl"),
        runner.run_jsonl("AgentSafety", "external/agent_safety.jsonl"),
    ]
    total = sum(x.total for x in suites)
    passed = sum(x.passed for x in suites)
    row = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "commit": sha,
        "aggregate_rate": 0.0 if total == 0 else round(passed/total, 4),
        "suites": [{"name": x.name, "passed": x.passed, "total": x.total} for x in suites],
    }
    p = Path("leaderboard.json")
    data = []
    if p.exists():
        data = json.loads(p.read_text(encoding="utf-8"))
    data.append(row)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(row, ensure_ascii=False, indent=2))
