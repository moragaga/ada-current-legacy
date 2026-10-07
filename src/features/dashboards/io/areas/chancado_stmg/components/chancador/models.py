from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component

from .build import build_chancado_stmg_component, build_chancado_stmg_group_component

DisplayValue: TypeAlias = str | int | float | Component | None


@dataclass(frozen=True, slots=True)
class ChancadorData:
    label: str

    chancado_state: DisplayValue = None
    chancado_value: DisplayValue = None
    chancado_color: DisplayValue = None
    chancado_unit: str | None = None
    atollo_state: DisplayValue = None
    mirror: bool = False

    def to_component(self) -> Component:
        return build_chancado_stmg_component(model=self)


@dataclass(frozen=True, slots=True)
class ChancadorGroupData:
    chancadores: tuple[ChancadorData, ...]

    @classmethod
    def from_iterable(cls, chancadores: Iterable[ChancadorData]) -> ChancadorGroupData:
        return cls(chancadores=tuple(chancadores))

    def to_component(self) -> Component:
        return build_chancado_stmg_group_component(models=self.chancadores)

    def to_components(self) -> list[Component]:
        return [chancador.to_component() for chancador in self.chancadores]

    def __iter__(self):
        return iter(self.chancadores)

    def __len__(self):
        return len(self.chancadores)
