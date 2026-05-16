from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class MultimodalContext:
    text_tokens: int
    image_regions: int
    tool_signals: int


class MultimodalGrounder:
    """Прототип grounding-ядра: зводить текст/візуальні/інструментальні сигнали в єдиний контекст."""

    def ground(self, text: str, image_stub: Dict[str, int] | None = None, tool_stub: Dict[str, int] | None = None) -> MultimodalContext:
        image_stub = image_stub or {}
        tool_stub = tool_stub or {}
        return MultimodalContext(
            text_tokens=len(text.split()),
            image_regions=int(image_stub.get("regions", 0)),
            tool_signals=int(tool_stub.get("events", 0)),
        )
