from __future__ import annotations

from dash import (
    Input,
    Output,
    ctx,
)
from dash.exceptions import PreventUpdate

import time

from src.app.dash import get_dash_app
from src.shared.runtime.logging.debug import debug_log
from src.shared.ui.app_dashboard_shell.io.ids import DashboardShellIOIds
from src.shared.ui.rendering import build_content
from src.shared.ui.status.value_mapping import map_latest_values_for_display

from .builders import CONTENT_BUILDER_DEFINITION
from .ids import CarguioTransporteIds


def register_carguio_transporte_callback():
    app = get_dash_app()

    @app.callback(
        Output(component_id=CarguioTransporteIds.GESTION_CARGUIO, component_property='children'),
        # Output(
        #     component_id=CarguioTransporteIds.GESTION_CARGUIO_FOOTER_EXTRA_CONTENT,
        #     component_property='children',
        # ),
        Output(component_id=CarguioTransporteIds.READY_FLAG, component_property='data-ready'),
        Input(
            component_id=DashboardShellIOIds.STORE_CARGUIO_TRANSPORTE,
            component_property='data',
        ),
    )
    def render_transporte(
            context,
    ):
        if ctx.triggered_id is None or context is None:
            raise PreventUpdate

        # REMOVE TO NOT GET EXTERNAL DATA
        if context.get('runtime_error'):
            raise ValueError('[ERROR] Dashboard information runtime error')

        if not context.get('changed', False):
            debug_log('[INFO] carguío - transporte has not changed. Skipping render.')
            raise PreventUpdate

        _start = time.perf_counter()

        kpis = map_latest_values_for_display(data=context.get('data'))
        content = build_content(definition=CONTENT_BUILDER_DEFINITION, kpis=kpis)

        debug_log(f'[INFO] render carguío - transporte took {time.perf_counter() - _start:.2f} seconds.')

        return *content, 'true'