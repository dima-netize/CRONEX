from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class PublicSuiteResult:
    name: str
    available: bool
    total: int
    passed: int


class PublicSOTAProtocolRunner:
    """Інтеграція з зовнішніми протоколами через JSONL-файли кейсів."""

    def run_jsonl(self, suite_name: str, path: str) -> PublicSuiteResult:
        p = Path(path)
        if not p.exists():
            return PublicSuiteResult(suite_name, False, 0, 0)

        total = passed = 0
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            item = json.loads(line)
            total += 1
            passed += int(bool(item.get("passed", False)))
        return PublicSuiteResult(suite_name, True, total, passed)
