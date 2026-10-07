from __future__ import annotations

from dash import html

from src.shared.ui.app_dashboard_shell.io.dashboard_layout import build_dashboard_io_layout

from .composition.dashboard_io_content_layout import build_dashboard_io_content_layout
from .definition import DASHBOARD_IO_DEFINITION

_INTEGRATED_OPERATIONS_PAGE_ID = 'dashboard-home-integrated-operations-page'


def build_integrated_operations_home_layout():
    return html.Div(
        id=_INTEGRATED_OPERATIONS_PAGE_ID,
        children=build_dashboard_io_layout(
            dashboard_definition=DASHBOARD_IO_DEFINITION,
            **build_dashboard_io_content_layout(),
        ),
    )
