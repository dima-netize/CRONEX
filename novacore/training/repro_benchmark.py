from __future__ import annotations

import json
import random

from novacore.models.novacore import NovaCoreMini


DATA = [
    "STORE_COLOR C1 | SHIFT N2 | QUERY",
    "PAIR S1 C5 | QUERY S1",
    "TOOL_ADD 7 8 SUM | QUERY SUM",
]


if __name__ == "__main__":
    random.seed(42)
    model = NovaCoreMini(max_retries=1)
    outputs = []
    for item in DATA:
        out = model.run(item)
        outputs.append({"program": item, "verified": out.verified, "answer": out.answer})

    report = {
        "seed": 42,
        "num_cases": len(DATA),
        "verified": sum(int(o["verified"]) for o in outputs),
        "outputs": outputs,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
