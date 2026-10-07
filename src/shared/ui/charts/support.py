from __future__ import annotations

from dash.development.base_component import Component

from src.shared.ui.theme import resolve_color_class


def resolve_value(value: str | Component | None, default: int = 0) -> tuple[bool, int]:
    try:
        return True, int(float(value))
    except Exception as e:
        del e
        return False, default


def resolve_color(color: str | None, opacity_value: bool = False) -> str:
    if opacity_value:
        return '#BBBBBB'
    return resolve_color_class(value=color, color_type='hex', default='#5B5C64')
