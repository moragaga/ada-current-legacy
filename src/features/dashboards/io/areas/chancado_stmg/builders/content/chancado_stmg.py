from __future__ import annotations

from dash.development.base_component import Component

from ...components.chancado_stmg.mappers import build_chancado_stmg_mapper


def build_chancado_stmg_content(kpis: dict) -> Component:
    return build_chancado_stmg_mapper(kpis=kpis).to_component()
