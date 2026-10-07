from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

DisplayKey: TypeAlias = str | None


@dataclass(frozen=True, slots=True)
class VertimilDefinition:
    label: str
    vertimil_state_key: DisplayKey = None
    vertimil_value_key: DisplayKey = None
    vertimil_color_key: DisplayKey = None
    vertimil_unit: DisplayKey = None
