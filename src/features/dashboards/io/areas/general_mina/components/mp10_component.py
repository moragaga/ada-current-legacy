from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from src.shared.ui.theme import resolve_color_class

from ..models.mp10 import MP10Data


def build_mp10_component(*, model: MP10Data) -> Component:
    return html.Div(
        className='d-flex flex-column gap-1',
        children=[
            _build_row(
                text_prefix='Hotel Mina (μg/m³)',
                value=model.current_value,
                value_color=model.current_value_color,
                alert=model.current_value_alert,
                alert_color=model.current_value_alert_color,
            ),
            _build_row(
                text_prefix='HM proy prom diario (μg/m³)',
                value=model.projection_value,
                value_color=model.projection_value_color,
                alert=model.projection_value_alert,
                alert_color=model.projection_value_alert_color,
            ),
        ],
    )


def _build_row(
    *,
    text_prefix: str,
    value: str | Component | None,
    value_color: str | Component | None,
    alert: str | Component | None,
    alert_color: str | Component | None,
) -> Component:
    return html.Div(
        className='d-flex justify-content-between align-items-center app-border-bottom py-1',
        children=[
            _build_information(
                text_prefix=text_prefix,
                value=value,
                color=value_color,
            ),
            _build_alert(value=alert, color=alert_color),
        ],
    )


def _build_information(
    *,
    text_prefix: str,
    value: str | Component | None,
    color: str | Component | None,
) -> Component:
    color_class = resolve_color_class(value=color) if color else ''
    value_style = {} if color_class else {'color': '#495057'}

    return html.Div(
        className='d-flex gap-2 align-items-baseline',
        children=[
            html.P(className='fs-io-200 text-secondary mb-0', children=[text_prefix]),
            html.P(
                className=f'{color_class} fs-io-200 fw-bold mb-0',
                style=value_style,
                children=[value],
            ),
        ],
    )


def _build_alert(*, value: str | None, color: str | Component | None) -> Component | None:
    if not value:
        return None

    style = {
        'backgroundColor': str(color),
        'minWidth': '44px',
        'height': '16px',
        'borderRadius': '3px',
    }

    text_style = {
        'fontSize': '0.45rem',
        'lineHeight': '1',
        'letterSpacing': '0.2px',
        'color': '#ffffff',
    }

    return html.Div(
        className='px-1 d-flex align-items-center justify-content-center',
        style=style,
        children=[
            html.Span(
                className='text-white fw-bold mb-0',
                style=text_style,
                children=[value],
            )
        ],
    )