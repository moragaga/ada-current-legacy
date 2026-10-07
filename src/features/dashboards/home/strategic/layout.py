from __future__ import annotations

from dash import html

from src.shared.ui.app_dashboard_shell.strategic.dashboard_layout import (
    build_dashboard_strategic_layout,
)

from ..definition import DASHBOARD_DEFINITION

_STRATEGIC_PAGE_ID = 'dashboard-home-strategic-page'


def build_strategic_home_layout():
    return html.Div(
        id=_STRATEGIC_PAGE_ID,
        children=build_dashboard_strategic_layout(
            dashboard_definition=DASHBOARD_DEFINITION,
            header_children=[_build_placeholder_header(title='Dashboard Estratégico')],
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
