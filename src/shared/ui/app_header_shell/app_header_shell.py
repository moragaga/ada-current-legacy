from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.development.base_component import Component

from src.app.navigation.ids import AppNavigationIds
from src.app.navigation.offcanvas import build_app_navigation_offcanvas

from .primitives import build_button_action, build_logo


def build_app_header_shell(
    *,
    app_name: str,
    global_indicator_content=None,
    information_content=None,
    alarm_notifications_content=None,
    time_status_content=None,
) -> html.Div:
    global_indicator_content = global_indicator_content or []
    information_content = information_content or []
    alarm_notifications_content = alarm_notifications_content or []
    time_status_content = time_status_content or []

    return html.Div(
        className='app-header-shell position-relative',
        children=[
            dbc.Container(
                fluid=True,
                className='app-header-inner',
                children=[
                    dbc.Row(
                        className='g-0 align-items-stretch',
                        children=[
                            dbc.Col(
                                xs=12,
                                sm=1,
                                md=1,
                                lg=1,
                                xl=1,
                                xxl=1,
                                children=[_build_logo(app_name=app_name)],
                            ),
                            dbc.Col(
                                xs=12,
                                sm=9,
                                md=9,
                                lg=9,
                                xl=9,
                                xxl=9,
                                children=html.Div(
                                    className='',
                                    children=global_indicator_content,
                                ),
                            ),
                            dbc.Col(
                                xs=12,
                                sm=1,
                                md=1,
                                lg=1,
                                xl=1,
                                xxl=1,
                                children=[
                                    html.Div(
                                        className='d-flex align-items-center '
                                        'justify-content-center h-100 status-border-right',
                                        children=information_content,
                                    )
                                ],
                            ),
                            dbc.Col(
                                xs=12,
                                sm=1,
                                md=1,
                                lg=1,
                                xl=1,
                                xxl=1,
                                className='d-flex align-items-center justify-content-center background-secondary disabled',
                                children=[
                                    html.Div(
                                        className='d-flex align-items-center justify-content-center w-100 h-100',
                                        children=alarm_notifications_content,
                                    )
                                ],
                            ),
                            dbc.Col(
                                className='app-header-mobile-toggle',
                                xs=12,
                                sm=1,
                                md=1,
                                lg=1,
                                xl=1,
                                xxl=1,
                                children=[
                                    build_button_action(
                                        id_button=AppNavigationIds.HEADER_MOBILE_TOGGLE,
                                        icon_button='bi bi-list',
                                        class_name='dashboard-menu-btn-mobile',
                                    )
                                ],
                            ),
                        ],
                    ),
                    dbc.Row(
                        className='information-time-status-container',
                        children=time_status_content
                    )
                ],
            ),
            build_button_action(
                id_button=AppNavigationIds.HEADER_DESKTOP_TOGGLE,
                icon_button='bi bi-chevron-left',
                class_name='dashboard-menu-btn-desktop d-none d-md-flex',
            ),
            dcc.Location(
                id=AppNavigationIds.HEADER_LOCATION,
                refresh=False,
            ),
            build_app_navigation_offcanvas(),
        ],
    )

def _build_logo(app_name: str) -> Component:
    return html.Span(
        className='h-100 d-flex flex-column justify-content-center logo-wrapper',
        children=[
            build_logo(logo_src_name='app-web-home'),
            html.P(
                className='fs-io-hg-400 text-center pt-1',
                children='ASISTENTE DE DECISIONES ÁGILES'
            ),
            html.P(
                className='fs-io-hg-500 fw-bold app-name-with-lines',
                children=app_name.upper()
            )
        ]
    )