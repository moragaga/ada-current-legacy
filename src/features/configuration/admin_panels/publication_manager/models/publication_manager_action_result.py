from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PublicationManagerActionResult:
    rows: list[dict[str, Any]]
    errors: tuple[str, ...] = ()
    success_message: str | None = None

    @property
    def has_errors(self) -> bool:
        return bool(self.errors)
