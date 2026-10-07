from __future__ import annotations

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class AppTimeStatusShellDefinition:
    label: str
    icon_class_name: str
    value_id: str
    icons_id: str | None = None
    right_divisor: bool = False
    value: Any | None = None

