from __future__ import annotations

from dataclasses import dataclass

from .models import (
    DisplayUnit,
    DisplayValue,
)


@dataclass(frozen=True, slots=True)
class StandardMetricDefinition:
    label: DisplayValue
    kpi_key: str

    unit: DisplayUnit = None
    unit_key: str | None = None
    unit_template: str = '{}'

    color_key: str | None = None
    field: str | None = None

    font_size_class_name: str | None = 'font-size-200'
    value_class_name: str | None = ''
    container_class_name: str | None = 'app-border-bottom'


@dataclass(frozen=True, slots=True)
class DualMetricDefinition:
    label: DisplayValue

    first_label: DisplayValue = None
    first_kpi_key: str | None = None
    first_unit: DisplayUnit = None
    first_color_key: str | None = ''

    second_label: DisplayValue = None
    second_kpi_key: str | None = None
    second_unit: DisplayUnit = None
    second_color_key: str | None = None

    divider_value: str = '/'

    font_size_class_name: str | None = 'font-size-100'
    first_value_class_name: str | None = ''
    second_value_class_name: str | None = ''
    container_class_name: str | None = 'app-border-bottom'
