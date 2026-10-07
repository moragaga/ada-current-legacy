from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component
from .build import build_vertimil_component, build_vertimil_group_component

DisplayValue: TypeAlias = str | int | float | Component | None


@dataclass(frozen=True, slots=True)
class VertimilData:
    label: str
    vertimil_state: DisplayValue = None
    vertimil_value: DisplayValue = None
    vertimil_color: DisplayValue = None
    vertimil_unit: str | None = None

    def to_component(self) -> Component:
        return build_vertimil_component(model=self)

@dataclass(frozen=True, slots=True)
class VertimilGroupData:
    vertimils: tuple[VertimilData, ...]

    @classmethod
    def from_iterable(cls, vertimils: Iterable[VertimilData]) -> VertimilGroupData:
        return cls(vertimils=tuple(vertimils))

    def to_component(self) -> Component:
        return build_vertimil_group_component(models=self)

    def to_components(self) -> list[Component]:
        return [vertimil.to_component() for vertimil in self.vertimils]

    def __iter__(self):
        return iter(self.vertimils)

    def __len__(self):
        return len(self.vertimils)
