from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component
from .build import build_molinos_bolas_component, build_molino_bolas_component

DisplayValue: TypeAlias = str | int | float | Component | None

@dataclass(frozen=True, slots=True)
class MolinoBolasData:
    label: str
    mb_state: DisplayValue = None
    mb_power: DisplayValue = None
    mb_power_color: DisplayValue = None

    def to_component(self) -> Component:
        return build_molino_bolas_component(model=self)

@dataclass(frozen=True, slots=True)
class MolinoBolasGroupData:
    molinos_bolas: tuple[MolinoBolasData, ...]

    @classmethod
    def from_iterable(cls, molinos_bolas: Iterable[MolinoBolasData]) -> MolinoBolasGroupData:
        return cls(molinos_bolas=tuple(molinos_bolas))

    def to_component(self) -> Component:
        return build_molinos_bolas_component(models=self)

    def to_components(self) -> list[Component]:
        return [molino_bolas.to_component() for molino_bolas in self.molinos_bolas]

    def __iter__(self):
        return iter(self.molinos_bolas)

    def __len__(self):
        return len(self.molinos_bolas)