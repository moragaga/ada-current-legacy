from __future__ import annotations

from dash.development.base_component import Component
from ...components.linea_sag.mapper import build_lineas_sag_mapper


def build_molienda_content(kpis: dict) -> Component:
    return build_lineas_sag_mapper(kpis=kpis).to_component()