from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from src.features.dashboards.io.areas.header.mappers.global_indicator_mapper import build_global_indicator_mapper


def build_global_indicator_content(kpis: dict) -> list[Component]:
    return build_global_indicator_mapper(kpis=kpis).to_component()
