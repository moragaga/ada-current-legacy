from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component

from .build import (
    build_global_indicator_component,
    build_global_indicator_group_component,
)

DisplayValue: TypeAlias = str | int | float | Component | None


@dataclass(frozen=True, slots=True)
class GlobalIndicatorDetailData:
    uuid: str
    indicator: DisplayValue
    unit: DisplayValue
    real_dia: DisplayValue
    plan_dia: DisplayValue
    real_semana: DisplayValue
    plan_semana: DisplayValue
    color_dia: DisplayValue = None
    color_semana: DisplayValue = None
    border_left: bool = False
    border_right: bool = False

    def to_component(self) -> Component:
        return build_global_indicator_component(
            uuid=self.uuid,
            indicator=self.indicator,
            unit=self.unit,
            real_dia=self.real_dia,
            plan_dia=self.plan_dia,
            real_semana=self.real_semana,
            plan_semana=self.plan_semana,
            color_dia=self.color_dia,
            color_semana=self.color_semana,
            border_left=self.border_left,
            border_right=self.border_right,
        )


@dataclass(frozen=True, slots=True)
class GlobalIndicatorGroupData:
    indicators: tuple[GlobalIndicatorDetailData, ...]

    @classmethod
    def from_iterable(
        cls,
        indicators: Iterable[GlobalIndicatorDetailData],
    ) -> GlobalIndicatorGroupData:
        return cls(
            indicators=tuple(indicators),
        )

    def to_component(self) -> Component:
        return build_global_indicator_group_component(
            indicators=self.indicators,
        )

    def to_components(self) -> list[Component]:
        return [indicator.to_component() for indicator in self.indicators]

    def __iter__(self):
        return iter(self.indicators)

    def __len__(self) -> int:
        return len(self.indicators)
