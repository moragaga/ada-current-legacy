from __future__ import annotations

from typing import Iterable
from dash.development.base_component import Component

from dataclasses import dataclass

from src.shared.ui.components.metrics import MetricRowsData
from ..molino_bolas.model import MolinoBolasGroupData
from ..sag.model import SagData
from .build import build_linea_sag_component, build_lineas_sag_component

@dataclass(frozen=True, slots=True)
class LineaSagData:
    linea_number: str
    sag: SagData
    molinos_bolas: MolinoBolasGroupData
    metrics: MetricRowsData

    def to_component(self) -> Component:
        return build_linea_sag_component(model=self)


@dataclass(frozen=True, slots=True)
class LineaSagGroupData:
    lineas_sag: tuple[LineaSagData, ...]

    @classmethod
    def from_iterable(cls, lineas_sag: Iterable[LineaSagData]) -> LineaSagGroupData:
        return cls(lineas_sag=tuple(lineas_sag))

    def to_component(self) -> Component:
        return build_lineas_sag_component(models=self)

    def to_components(self) -> list[Component]:
        return [linea_sag.to_component() for linea_sag in self.lineas_sag]

    def __iter__(self):
        return iter(self.lineas_sag)

    def __len__(self):
        return len(self.lineas_sag)