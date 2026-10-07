from __future__ import annotations

from dataclasses import dataclass
from typing import Any, TypeAlias

from dash.development.base_component import Component

DisplayValue: TypeAlias = str | int | float | Component | None


def _extract_display_value(kpi_data: Any) -> DisplayValue:
    if isinstance(kpi_data, dict):
        parsed = kpi_data.get('parsed_value')
        if parsed is not None and str(parsed).lower() != 'nan':
            return str(parsed)
        val = kpi_data.get('value')
        if val is not None and str(val).lower() != 'nan':
            return str(val)
        return '--'
    if kpi_data is not None and str(kpi_data).lower() != 'nan':
        return str(kpi_data)
    return '--'


def _get_mp10_alert(kpi_data: Any) -> tuple[str | None, str | None]:
    raw_val = None
    if isinstance(kpi_data, dict):
        raw_val = kpi_data.get('value')
        if raw_val is None or str(raw_val).lower() == 'nan':
            raw_val = kpi_data.get('parsed_value')
    else:
        raw_val = kpi_data

    if raw_val is None:
        return None, None

    try:
        val = float(str(raw_val).replace(',', '.'))
    except (ValueError, TypeError):
        return None, None

    if val >= 501:
        return 'Alerta 4', '#b02a37'  
    if val >= 351:
        return 'Alerta 3', '#b02a37'  # Rojo
    if val >= 251:
        return 'Alerta 2', '#eab308'  
    if val >= 150:
        return 'Alerta 1', '#eab308'  # Amarillo

    return None, None


@dataclass(frozen=True, slots=True)
class MP10Data:
    current_value: DisplayValue = None
    current_value_color: DisplayValue = None
    current_value_alert: DisplayValue = None
    current_value_alert_color: DisplayValue = None
    projection_value: DisplayValue = None
    projection_value_color: DisplayValue = None
    projection_value_alert: DisplayValue = None
    projection_value_alert_color: DisplayValue = None

    @classmethod
    def from_kpis(cls, kpis: dict[str, Any] | None = None, **kwargs: Any) -> MP10Data:
        data_dict = kpis if kpis is not None else kwargs.get('kpis', {})

        kpi_actual = data_dict.get('mp10_hotel_mina')
        kpi_proy = data_dict.get('mp10_hotel_mina_proy')

        alert_act, color_act = _get_mp10_alert(kpi_actual)
        alert_proy, color_proy = _get_mp10_alert(kpi_proy)

        return cls(
            current_value=_extract_display_value(kpi_actual),
            current_value_color=None,
            current_value_alert=alert_act,
            current_value_alert_color=color_act,
            projection_value=_extract_display_value(kpi_proy),
            projection_value_color=None,
            projection_value_alert=alert_proy,
            projection_value_alert_color=color_proy,
        )