from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

DisplayKey: TypeAlias = str | None

@dataclass(frozen=True, slots=True)
class MolinoBolasDefinition:
    label: str
    mb_state_key: DisplayKey = None
    mb_power_key: DisplayKey = None
    mb_power_color_key: DisplayKey = None