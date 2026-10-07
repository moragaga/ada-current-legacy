from __future__ import annotations

from dash.development.base_component import Component

from .latest_value_display import resolve_latest_value_display


def map_latest_values_for_display(
    *,
    data: dict[str, dict],
) -> dict[str, str | Component]:
    values: dict[str, str | Component] = {}

    for key, value in data.items():
        values[key] = resolve_latest_value_display(**value)

    return values
