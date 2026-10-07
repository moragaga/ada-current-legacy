from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component

from .build import (
    build_level_gauge_component,
    build_level_gauge_group_component,
)
from .config import (
    GaugeVariant,
)

DisplayValue: TypeAlias = str | Component | None
DisplayNumeric: TypeAlias = float | int | str | Component | None


@dataclass(frozen=True, slots=True)
class LevelGaugeDetailData:
    variant: GaugeVariant
    image_name: str
    percentage: DisplayNumeric
    unit: str = '%'
    name: str = ''
    color: DisplayValue = None
    state: DisplayValue = None

    def to_component(self) -> Component:
        return build_level_gauge_component(
            variant=self.variant,
            image_name=self.image_name,
            percentage=self.percentage,
            unit=self.unit,
            name=self.name,
            color=self.color,
            state=self.state,
        )


@dataclass(frozen=True, slots=True)
class LevelGaugeGroupData:
    level_gauges: tuple[LevelGaugeDetailData, ...]

    @classmethod
    def from_iterable(
        cls,
        level_gauges: Iterable[LevelGaugeDetailData],
    ) -> LevelGaugeGroupData:
        return cls(
            level_gauges=tuple(level_gauges),
        )

    def to_component(self) -> Component:
        return build_level_gauge_group_component(
            level_gauges=self.level_gauges,
        )

    def to_components(self) -> list[Component]:
        return [level_gauge.to_component() for level_gauge in self.level_gauges]

    def __iter__(self):
        return iter(self.level_gauges)

    def __len__(self) -> int:
        return len(self.level_gauges)
