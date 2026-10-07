from __future__ import annotations

from dash import html

from src.shared.ui.app_dashboard_shell.ids import DashboardShellIds
from src.shared.ui.app_dashboard_shell.models import DashboardShellDefinition
from src.shared.ui.app_dashboard_shell.runtime.stores import (
    build_dashboard_process_runtime_store_components,
)


def build_dashboard_process_layout(
    *,
    dashboard_definition: DashboardShellDefinition,
    header_children=None,
    information_children=None,
    body_children=None,
    modals_children=None,
):
    header_children = header_children or []
    information_children = information_children or []
    body_children = body_children or []
    modals_children = modals_children or []

    dashboard = html.Div(
        id=DashboardShellIds.ROOT,
        className='dashboard-process-root',
        children=[
            html.Header(
                id=DashboardShellIds.HEADER,
                children=header_children,
            ),
            html.Main(
                children=[
                    html.Div(
                        id=DashboardShellIds.INFORMATION,
                        children=information_children,
                    ),
                    html.Div(
                        id=DashboardShellIds.BODY,
                        className='dashboard-process-body',
                        children=body_children,
                    ),
                ],
            ),
            html.Span(children=modals_children),
        ],
    )

    return [
        *build_dashboard_process_runtime_store_components(
            interval_ms=dashboard_definition.dashboard_interval_ms,
        ),
        html.Div(
            id='main-page-loader-scope',
            **{
                'data-page-loader': 'true',
                'data-loader-key': 'main-dashboard',
            },
            children=[
                html.Div(
                    className='page-loader-content',
                    children=[dashboard],
                ),
                html.Div(className='page-loader-overlay', children=[]),
            ],
        ),
    ]
