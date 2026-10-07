from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component

from src.shared.ui.components.metrics import MetricRowsData

from .build import (
    build_correa_stmg_component,
    build_correa_stmg_group_component,
    build_correas_stmg_component,
)

DisplayValue: TypeAlias = str | int | float | Component | None


@dataclass(frozen=True, slots=True)
class CorreaStmgData:
    label: str
    correa_state: DisplayValue = None

    def to_component(self, position: int) -> Component:
        return build_correa_stmg_component(model=self, position=position)


@dataclass(frozen=True, slots=True)
class CorreaStmgGroupData:
    correas: tuple[CorreaStmgData, ...]
    metrics: MetricRowsData = None

    @classmethod
    def from_iterable(
        cls,
        correas: Iterable[CorreaStmgData],
        metrics: MetricRowsData = None,
    ) -> CorreaStmgGroupData:
        return cls(
            correas=tuple(correas),
            metrics=metrics,
        )

    def to_components(self) -> list[Component]:
        return [correa.to_component() for correa in self.correas]

    def to_component(self) -> Component:
        return build_correas_stmg_component(models=self.correas)

    def to_group_component(self) -> Component:
        return build_correa_stmg_group_component(models=self)

    def __iter__(self):
        return iter(self.correas)

    def __len__(self):
        return len(self.correas)
