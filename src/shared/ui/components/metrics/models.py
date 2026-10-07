from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, TypeAlias

from dash.development.base_component import Component

from src.shared.ui.display.inline_two_value_row import build_inline_two_values_row
from src.shared.ui.display.inline_value_row import build_inline_value_row

DisplayValue: TypeAlias = str | int | float | Component | None
DisplayUnit: TypeAlias = str | Component | None


@dataclass(frozen=True, slots=True)
class StandardMetricDetailData:
    label: DisplayValue
    value: DisplayValue = None
    field: str | None = None
    unit: DisplayUnit = None
    color: str | None = None
    font_size_class_name: str | None = 'font-size-100'
    value_class_name: str | None = ''
    container_class_name: str | None = 'app-border-bottom'

    def to_component(self) -> Component:
        return build_inline_value_row(
            label=self.label,
            value=self.value,
            unit=self.unit,
            font_size_class_name=self.font_size_class_name,
            value_class_name=self.value_class_name,
            container_class_name=self.container_class_name,
            color=self.color,
        )


@dataclass(frozen=True, slots=True)
class DualMetricDetailData:
    label: DisplayValue

    first_label: DisplayValue
    first_value: DisplayValue
    first_unit: DisplayUnit = None
    first_color: str | None = None

    second_label: DisplayValue = None
    second_value: DisplayValue = None
    second_unit: DisplayUnit = None
    second_color: str | None = None

    divider_value: str = '/'

    font_size_class_name: str | None = 'font-size-100'
    first_value_class_name: str | None = ''
    second_value_class_name: str | None = ''
    container_class_name: str | None = 'app-border-bottom'

    def to_component(self) -> Component:
        return build_inline_two_values_row(
            label=self.label,
            first_label=self.first_label,
            first_value=self.first_value,
            first_unit=self.first_unit,
            first_color=self.first_color,
            first_value_class_name=self.first_value_class_name,
            second_label=self.second_label,
            second_value=self.second_value,
            second_unit=self.second_unit,
            second_color=self.second_color,
            second_value_class_name=self.second_value_class_name,
            font_size_class_name=self.font_size_class_name,
            container_class_name=self.container_class_name,
            divider_value=self.divider_value,
        )


MetricDetailData: TypeAlias = StandardMetricDetailData | DualMetricDetailData


@dataclass(frozen=True, slots=True)
class MetricRowsData:
    items: tuple[MetricDetailData, ...]

    @classmethod
    def from_iterable(cls, items: Iterable[MetricDetailData]) -> MetricRowsData:
        return cls(items=tuple(items))

    def to_components(self) -> list[Component]:
        return [item.to_component() for item in self.items]

    def __iter__(self):
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
