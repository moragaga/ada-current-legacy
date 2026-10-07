from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

DisplayKey: TypeAlias = str | None


@dataclass(frozen=True, slots=True)
class ChancadorDefinition:
    label: str
    chancado_state_key: DisplayKey = None
    chancado_value_key: DisplayKey = None
    chancado_color_key: DisplayKey = None
    chancado_unit: DisplayKey = None
    atollo_state_key: DisplayKey = None
    mirror: bool = False
