from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from .model import AppTimeStatusShellStructure
from .ids import AppTimeStatusShellIds

def build_app_time_status_shell() -> Component:
    return html.Div(
        className='information-time-status-wrapper',
        children=[
            html.Span(
                id=AppTimeStatusShellIds.TIME_STATUS_COMPONENT
            ),
            html.Span(
                children=[
                    AppTimeStatusShellStructure(
                        label='Hora Actual',
                        icon_class_name='bi bi-clock',
                        value_id=AppTimeStatusShellIds.HORA_ACTUAL,

                    ).to_component()
                ]
            )
        ]
    )
