from __future__ import annotations


class ToolRegistry:
    """Мінімальний реєстр інструментів для multi-step планів."""

    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b
