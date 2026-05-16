from __future__ import annotations

from collections import Counter

from novacore.models.novacore import NovaCoreMini
from novacore.training.open_world_hard_eval import SUITE


if __name__ == "__main__":
    model = NovaCoreMini(max_retries=1)
    errors = Counter()

    for bucket, programs in SUITE.items():
        for p in programs:
            out = model.run(p)
            if bucket == "safety_external":
                if out.governance_mode != "halt":
                    errors["safety_miss"] += 1
            elif not out.verified:
                key = out.verifier_reason.split("|")[0].strip()
                errors[key] += 1

    print("Top hard-error types:")
    for k, v in errors.most_common(10):
        print(f"- {k}: {v}")
