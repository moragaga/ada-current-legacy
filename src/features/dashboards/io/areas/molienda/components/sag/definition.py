from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

DisplayKey: TypeAlias = str | None

@dataclass(frozen=True, slots=True)
class SagDefinition:
    label: str
    sag_state_key: DisplayKey = None
    sag_power_key: DisplayKey = None
    sag_power_color_key: DisplayKey = None