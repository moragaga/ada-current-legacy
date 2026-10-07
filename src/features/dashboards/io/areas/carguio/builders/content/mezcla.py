from __future__ import annotations

from typing import Any
from dash.development.base_component import Component

from ...mappers.mezcla import map_mezcla_table


def build_mezcla_content(kpis: dict[str, Any] | None = None, **kwargs) -> Component:
    actual_kpis = kpis if isinstance(kpis, dict) else kwargs.get('kpis', {})
    if not isinstance(actual_kpis, dict):
        actual_kpis = {}

    return map_mezcla_table(kpis=actual_kpis).to_component()