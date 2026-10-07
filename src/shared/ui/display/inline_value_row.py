from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from ..theme import resolve_color_class


def build_inline_value_row(
    label: str | Component,
    value: str | html.Img | None,
    unit: str | Component | None = None,
    color: str | None = None,
    value_class_name: str | None = None,
    container_class_name: str = 'app-border-bottom pt-1',
    font_size_class_name: str = 'font-size-200',
) -> html.Div:
    return html.Div(
        className=f'd-flex justify-content-between {container_class_name} {font_size_class_name}',
        children=[
            html.P(children=[label]),
            html.Div(
                className='d-flex',
                children=[
                    html.P(
                        className=f'fw-bold '
                        f'{resolve_color_class(value=color)} '
                        f'{value_class_name or ""}',
                        children=[value],
                    ),
                    html.P(style={'paddingLeft': '.1rem'}, children=[unit])
                    if unit is not None
                    else None,
                ],
            ),
        ],
    )
