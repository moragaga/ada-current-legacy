from __future__ import annotations

from typing import Any
from dash import html
from dash.development.base_component import Component
from ...mappers.equipos_servicio import map_equipos_servicio_table


def build_equipos_servicio_content(kpis: dict[str, Any]) -> Component:
    return map_equipos_servicio_table(kpis=kpis).to_component()


def build_equipos_servicio_total(kpis: dict[str, Any]) -> Component:
    return html.Div()