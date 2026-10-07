from __future__ import annotations

from dash import html
from dash.development.base_component import Component


def build_alarm_notification_content(kpis: dict):
    return html.Div(
        className='h-100 w-100 position-relative',
        children=[
            build_status_backdrop(uuid='header-alarm-notifications-uuid-1')
        ]
    )

DISPLAY_CARD_STATUS_BACKDROP_TYPE = 'display-card-status-backdrop'

def build_status_backdrop(
    *,
    uuid: str,
    message: str = 'En construcción',
) -> Component:
    return html.Div(
        # id={
        #     'type': DISPLAY_CARD_STATUS_BACKDROP_TYPE,
        #     'index': uuid,
        # },
        className='display-card-backdrop display-card-backdrop--visible',
        children=[
            html.Div(
                className='display-card-backdrop__content',
                children=[
                    html.I(
                        className=(
                            'bi bi-hammer '
                            'display-card-backdrop__icon'
                        ),
                    ),
                    html.P(
                        className='display-card-backdrop__message',
                        children=[message],
                    ),
                ],
            ),
        ],
    )