from __future__ import annotations

import time

from dash import (
    Input,
    Output,
    ctx,
)
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.shared.runtime.logging.debug import debug_log
from src.shared.ui.app_dashboard_shell.io.ids import DashboardShellIOIds
from src.shared.ui.rendering import build_content
from src.shared.ui.status.value_mapping import map_latest_values_for_display

from .builders import CONTENT_BUILDER_DEFINITION
from .ids import MoliendaIds


def register_molienda_callback():
    app = get_dash_app()

    @app.callback(
        Output(component_id=MoliendaIds.MOLIENDA, component_property='children'),
        Output(component_id=MoliendaIds.READY_FLAG, component_property='data-ready'),
        Input(
            component_id=DashboardShellIOIds.STORE_MOLIENDA,
            component_property='data',
        ),
    )
    def render_molienda(
        context,
    ):
        if ctx.triggered_id is None or context is None:
            raise PreventUpdate

        # REMOVE TO NOT GET EXTERNAL DATA
        if context.get('runtime_error'):
            raise ValueError('[ERROR] Dashboard information runtime error')

        if not context.get('changed', False):
            debug_log('[INFO] molienda has not changed. Skipping render.')
            raise PreventUpdate

        _start = time.perf_counter()

        kpis = map_latest_values_for_display(data=context.get('data'))
        content = build_content(definition=CONTENT_BUILDER_DEFINITION, kpis=kpis)

        debug_log(f'[INFO] render molienda took {time.perf_counter() - _start:.2f} seconds.')

        return *content, 'true'
