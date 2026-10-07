from __future__ import annotations

from dash import html

from src.shared.ui.app_dashboard_shell.process.dashboard_layout import (
    build_dashboard_process_layout,
)

from ..definition import DASHBOARD_DEFINITION

_PROCESS_PAGE_ID = 'dashboard-home-process-page'


def build_process_home_layout():
    return html.Div(
        id=_PROCESS_PAGE_ID,
        children=build_dashboard_process_layout(
            dashboard_definition=DASHBOARD_DEFINITION,
            header_children=[_build_placeholder_header(title='Dashboard Proceso')],
            information_children=[],
            body_children=[],
            modals_children=[],
        ),
    )


def _build_placeholder_header(*, title: str):
    return html.Div(
        className='dashboard-placeholder-header',
        children=[html.H4(title)],
    )
