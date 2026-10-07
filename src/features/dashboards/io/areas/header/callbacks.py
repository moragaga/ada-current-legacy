from __future__ import annotations

from dash import (
    Input,
    Output,
    ctx,
)
from dash.exceptions import PreventUpdate

import time

from src.app.dash import get_dash_app
from src.shared.time.timestamps import parse_utc_datetime
from src.shared.ui.app_dashboard_shell.io.ids import DashboardShellIOIds
from src.shared.ui.app_dashboard_shell.runtime.ids import DashboardRuntimeShellIds
from src.shared.ui.app_time_status_shell.ids import AppTimeStatusShellIds
from src.shared.ui.rendering import build_content
from src.shared.ui.status.value_mapping import map_latest_values_for_display

from .builders import CONTENT_BUILDER_DEFINITION, CONTENT_BUILDER_ALARM_NOTIFICATION
from .builders.content.time_status import build_time_status_content
from .ids import HeaderIds
from src.shared.runtime.logging.debug import debug_log

def register_global_indicator_callback():
    app = get_dash_app()

    @app.callback(
        Output(component_id=HeaderIds.GLOBAL_INDICATOR, component_property='children'),
        # Output(component_id=HeaderIds.STATUS, component_property='children'),
        # Output(component_id=HeaderIds.NOTIFICATIONS, component_property='children'),
        Output(component_id=HeaderIds.READY_FLAG_HEADER, component_property='data-ready'),
        Input(
            component_id=DashboardShellIOIds.STORE_GLOBAL_INDICATOR,
            component_property='data',
        ),
    )
    def render_global_indicator(
        context,
    ):
        if ctx.triggered_id is None or context is None:
            raise PreventUpdate

        # REMOVE TO NOT GET EXTERNAL DATA
        if context.get('runtime_error'):
            raise ValueError('[ERROR] Dashboard information runtime error')

        if not context.get('changed', False):
            debug_log('[INFO] global indicator has not changed. Skipping render.')
            raise PreventUpdate

        _start = time.perf_counter()

        kpis = map_latest_values_for_display(data=context.get('data'))
        content = build_content(definition=CONTENT_BUILDER_DEFINITION, kpis=kpis)

        debug_log(f'[INFO] render global indicator took {time.perf_counter() - _start:.2f} seconds.')

        return *content, 'true'

    @app.callback(
        Output(component_id=AppTimeStatusShellIds.TIME_STATUS_COMPONENT, component_property='children'),
        Output(component_id=HeaderIds.READY_FLAG_TIME_STATUS, component_property='data-ready'),
        Input(
            component_id=DashboardRuntimeShellIds.STORE_INFORMATION_STATUS,
            component_property='data',
        ),
    )
    def render_global_indicator(
        context,
    ):
        if ctx.triggered_id is None or context is None:
            raise PreventUpdate

        _start = time.perf_counter()

        last_update_pi = parse_utc_datetime(context.get('last_update_pi_utc'))
        last_update_dispatch = parse_utc_datetime(context.get('last_update_dispatch_utc'))
        content = build_time_status_content(
            last_update_pi=last_update_pi,
            last_update_dispatch=last_update_dispatch
        )
        debug_log(f'[INFO] render information time took {time.perf_counter() - _start:.2f} seconds.')

        return content, 'true'

    @app.callback(
        Output(component_id=HeaderIds.INFORMATION, component_property='children'),
        Output(component_id=HeaderIds.ALARM_NOTIFICATIONS, component_property='children'),
        Output(component_id=HeaderIds.READY_FLAG_ALARM_NOTIFICATIONS, component_property='data-ready'),
        Input(
            component_id=DashboardRuntimeShellIds.STORE_INFORMATION_STATUS,
            component_property='data',
        ),
    )
    def render_information_alarm(
            context,
    ):
        if ctx.triggered_id is None or context is None:
            raise PreventUpdate

        _start = time.perf_counter()

        content = build_content(definition=CONTENT_BUILDER_ALARM_NOTIFICATION, kpis={})

        debug_log(f'[INFO] render information alarm took {time.perf_counter() - _start:.2f} seconds.')

        return *content, 'true'