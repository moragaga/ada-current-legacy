from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias, Literal

DisplayKey: TypeAlias = str | None

PositionList = Literal['vertical', 'horizontal']

@dataclass(frozen=True, slots=True)
class BombasPosition:
    position: PositionList = 'vertical'

@dataclass(frozen=True, slots=True)
class BombaDefinition:
    label: str
    bomba_state_key: DisplayKey = None

@dataclass(frozen=True, slots=True)
class BombasGroupDefinition:
    bombas_group: tuple[dict[BombasPosition, tuple[BombaDefinition, ...]]]