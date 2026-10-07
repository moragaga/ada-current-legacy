from __future__ import annotations

from typing import Any

from src.utils.colors import get_status_color

from .definitions import DualMetricDefinition, StandardMetricDefinition
from .models import DualMetricDetailData, MetricRowsData, StandardMetricDetailData


def map_standard_metric_rows(
    *,
    definitions: tuple[StandardMetricDefinition, ...],
    kpis: dict[str, Any],
) -> MetricRowsData:
    return MetricRowsData.from_iterable(
        items=(
            map_standard_metric(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions
        ),
    )


def map_standard_metric(
    *,
    definition: StandardMetricDefinition,
    kpis: dict[str, Any],
) -> StandardMetricDetailData:
    raw_color = kpis.get(definition.color_key) if definition.color_key else None

    return StandardMetricDetailData(
        label=definition.label,
        value=kpis.get(definition.kpi_key),
        field=definition.field,
        unit=definition.unit,
        color=get_status_color(raw_color),  # <-- Convierte el payload a '#d93829', '#eab308' o None
        font_size_class_name=definition.font_size_class_name,
        value_class_name=definition.value_class_name,
        container_class_name=definition.container_class_name,
    )


def map_dual_metric_rows(
    *,
    definitions: tuple[DualMetricDefinition, ...],
    kpis: dict[str, Any],
) -> MetricRowsData:
    return MetricRowsData.from_iterable(
        items=(
            map_dual_metric(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions
        )
    )


def map_dual_metric(
    *,
    definition: DualMetricDefinition,
    kpis: dict[str, Any],
) -> DualMetricDetailData:
    raw_first_color = kpis.get(definition.first_color_key) if definition.first_color_key else None
    raw_second_color = kpis.get(definition.second_color_key) if definition.second_color_key else None

    # DIAGNÓSTICO EN TERMINAL
    if definition.first_color_key:
        print(f"[DEBUG COLOR] KPI: {definition.first_color_key} | Raw: {raw_first_color} | Resuelto: {get_status_color(raw_first_color)}")

    return DualMetricDetailData(
        label=definition.label,
        first_label=definition.first_label,
        first_value=kpis.get(definition.first_kpi_key),
        first_unit=definition.first_unit,
        first_color=get_status_color(raw_first_color),  
        second_label=definition.second_label,
        second_value=kpis.get(definition.second_kpi_key),
        second_unit=definition.second_unit,
        second_color=get_status_color(raw_second_color), 
        divider_value=definition.divider_value,
        font_size_class_name=definition.font_size_class_name,
        first_value_class_name=definition.first_value_class_name,
        second_value_class_name=definition.second_value_class_name,
        container_class_name=definition.container_class_name,
    )