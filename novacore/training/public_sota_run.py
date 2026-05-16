from __future__ import annotations

import json
import os

from novacore.models.public_sota import PublicSOTAProtocolRunner


if __name__ == "__main__":
    runner = PublicSOTAProtocolRunner()
    suites = [
        ("SWE-bench", os.getenv("SWE_BENCH_JSONL", "external/swe_bench.jsonl")),
        ("MMLU", os.getenv("MMLU_JSONL", "external/mmlu.jsonl")),
        ("AgentSafety", os.getenv("AGENT_SAFETY_JSONL", "external/agent_safety.jsonl")),
    ]

    print("Public SOTA protocol run:")
    total = passed = available = 0
    details: list[dict] = []

    for name, path in suites:
        res = runner.run_jsonl(name, path)
        if not res.available:
            print(f"- {name}: UNAVAILABLE ({path})")
            details.append({"suite": name, "available": False, "path": path})
            continue

        rate = 0.0 if res.total == 0 else round(res.passed / res.total, 4)
        print(f"- {name}: passed={res.passed}/{res.total} rate={rate}")
        total += res.total
        passed += res.passed
        available += 1
        details.append({"suite": name, "available": True, "path": path, "passed": res.passed, "total": res.total, "rate": rate})

    aggregate_rate = 0.0 if total == 0 else round(passed / total, 4)
    summary = {
        "available_suites": available,
        "total_suites": len(suites),
        "passed": passed,
        "total": total,
        "aggregate_rate": aggregate_rate,
        "details": details,
    }
    print("\nJSON_SUMMARY=")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
