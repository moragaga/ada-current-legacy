from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias, Literal

from dash.development.base_component import Component
from .build import build_bomba_component, build_bomba_group_component

DisplayValue: TypeAlias = str | int | float | Component | None

PositionList = Literal['vertical', 'horizontal']

@dataclass(frozen=True, slots=True)
class BombasPosition:
    position: PositionList = 'vertical'

@dataclass(frozen=True, slots=True)
class BombaData:
    label: str
    bomba_state: DisplayValue = None

    def to_component(self) -> Component:
        return build_bomba_component(model=self)

@dataclass(frozen=True, slots=True)
class BombaGroupData:
    bombas_group: tuple[dict[BombasPosition, tuple[BombaData, ...]]]

    @classmethod
    def from_iterable(cls, bombas: Iterable[dict[BombasPosition, tuple[BombaData, ...]]]) -> BombaGroupData:
        return cls(bombas_group=tuple(bombas))

    def to_component(self) -> Component:
        return build_bomba_group_component(models=self)

    def __iter__(self):
        return iter(self.bombas_group)

    def __len__(self):
        return len(self.bombas_group)
