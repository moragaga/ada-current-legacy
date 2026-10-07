from __future__ import annotations

import time

from dash import Input, Output
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.shared.runtime.logging.callback_logger import log_component_callback
from src.shared.runtime.logging.debug import debug_log
from src.shared.ui.app_alarm_shell.ids import AlarmShellIds

from .builders.alarm_panel_content import build_alarm_panel_content
from .ids import AlarmPanelIds


def register_alarm_panel_callback() -> None:
    app = get_dash_app()

    @app.callback(
        Output(
            component_id=AlarmPanelIds.ALARM_PANEL,
            component_property='children',
        ),
        Output(
            component_id=AlarmPanelIds.READY_FLAG,
            component_property='data-ready',
        ),
        Input(
            component_id=AlarmShellIds.STORE_ALARM_RUNTIME_STORE,
            component_property='data',
        ),
        prevent_initial_call=True,
    )
    @log_component_callback(
        callback_name='alarm_monitor.panel.render_alarm_panel',
        components=1,
        flags=1,
        ui_size='large',
    )
    def render_alarm_panel(context: dict):
        if context is None:
            raise PreventUpdate

        start = time.perf_counter()

        alarm_panel_content = build_alarm_panel_content(
            alarm_context=context,
        )

        debug_log(
            '[INFO] Render generic alarm panel took {0:.2f} seconds.'.format(
                time.perf_counter() - start,
            )
        )

        return (
            alarm_panel_content,
            'true',
        )
