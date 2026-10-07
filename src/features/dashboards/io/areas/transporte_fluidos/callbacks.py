from __future__ import annotations

from dash import (
    Input,
    Output,
    ctx,
)
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.shared.runtime.logging.debug import debug_log
from src.shared.ui.app_dashboard_shell.io.ids import DashboardShellIOIds
from src.shared.ui.app_dashboard_shell.runtime.ids import DashboardRuntimeShellIds
from src.shared.ui.rendering import build_content
from src.shared.ui.status.value_mapping import map_latest_values_for_display

from .builders import CONTENT_BUILDER_DEFINITION
from .ids import TransporteFluidosIds

import time

def register_transporte_fluidos_callback():
    app = get_dash_app()

    @app.callback(
        Output(component_id=TransporteFluidosIds.STR, component_property='children'),
        Output(component_id=TransporteFluidosIds.STC, component_property='children'),
        Output(component_id=TransporteFluidosIds.TRANQUE, component_property='children'),
        Output(component_id=TransporteFluidosIds.STA, component_property='children'),
        Output(component_id=TransporteFluidosIds.READY_FLAG, component_property='data-ready'),
        Input(
            component_id=DashboardShellIOIds.STORE_TRANSPORTE_FLUIDOS,
            component_property='data',
        ),
    )
    def render_transporte_fluidos(
            context,
    ):
        if ctx.triggered_id is None or context is None:
            raise PreventUpdate

        # REMOVE TO NOT GET EXTERNAL DATA
        if context.get('runtime_error'):
            raise ValueError('[ERROR] Dashboard information runtime error')

        if not context.get('changed', False):
            debug_log('[INFO] transporte fluidos has not changed. Skipping render.')
            raise PreventUpdate

        _start = time.perf_counter()

        kpis = map_latest_values_for_display(data=context.get('data'))
        content = build_content(definition=CONTENT_BUILDER_DEFINITION, kpis=kpis)

        debug_log(f'[INFO] render transporte fluidos took {time.perf_counter() - _start:.2f} seconds.')

        return *content, 'true'
