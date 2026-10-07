from __future__ import annotations

from dash import html
from dash.development.base_component import Component


def build_running_button_children(
    *,
    text: str,
) -> Component:
    return html.Span(
        className='app-running-button-content',
        children=[
            html.Span(
                className='spinner-border spinner-border-sm app-running-button-spinner',
                role='status',
                **{
                    'aria-hidden': 'true',
                },
            ),
            html.Span(
                className='app-running-button-label',
                children=text,
            ),
        ],
    )
