from __future__ import annotations

import json
import random

from novacore.models.novacore import NovaCoreMini


DATA = [
    "STORE_COLOR C1 | SHIFT N2 | QUERY",
    "PAIR S1 C5 | QUERY S1",
    "TOOL_ADD 7 8 SUM | QUERY SUM",
    "DELETE_ALL | QUERY",
]


def run_once(seed: int) -> dict:
    random.seed(seed)
    model = NovaCoreMini(max_retries=1)
    outputs = []
    for item in DATA:
        out = model.run(item)
        outputs.append((item, out.verified, out.answer, out.governance_mode))
    return {"seed": seed, "outputs": outputs}


if __name__ == "__main__":
    baseline = run_once(42)
    stable = True
    for _ in range(5):
        cur = run_once(42)
        if cur["outputs"] != baseline["outputs"]:
            stable = False
            break

    report = {
        "seed": 42,
        "stable_over_5_repeats": stable,
        "baseline_outputs": baseline["outputs"],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
