from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from ..components.active_alarm_list import build_active_alarm_panel_shell
from ..components.footer import build_active_alarms_modal_footer
from ..components.toolbar import build_active_alarms_modal_toolbar
from ..ids import ActiveAlarmsModalIds


def build_active_alarms_modal_host() -> html.Div:
    return html.Div(
        children=[
            dcc.Store(
                id=ActiveAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
                storage_type='memory',
            ),
            dcc.Store(
                id=ActiveAlarmsModalIds.OPERATOR_PAGE_STORE,
                data=1,
                storage_type='memory',
            ),
            dcc.Store(
                id=ActiveAlarmsModalIds.TRACKING_PAGE_STORE,
                data=1,
                storage_type='memory',
            ),
            dbc.Modal(
                id=ActiveAlarmsModalIds.MODAL,
                is_open=False,
                style={'--bs-modal-width': '98%'},
                scrollable=True,
                backdrop='static',
                centered=True,
                keyboard=False,
                class_name='active-alarms-modal modal-background',
                children=[
                    dbc.ModalHeader(
                        close_button=False,
                        className='d-flex justify-content-end align-items-center py-0 px-3 modal-background',
                        children=[
                            dbc.Button(
                                html.I(className='bi bi-x-lg text-white'),
                                id=ActiveAlarmsModalIds.CLOSE_BUTTON,
                                color='link',
                                className='active-alarms-close-button',
                                n_clicks=0,
                            ),
                        ],
                    ),
                    dbc.ModalBody(
                        className='active-alarms-modal-body',
                        children=[
                            _build_information(),
                            build_active_alarms_modal_toolbar(),
                            build_active_alarm_panel_shell(),
                            build_active_alarms_modal_footer(),
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_information() -> html.Div:
    return html.Div(
        className='active-alarms-modal-header',
        children=[
            html.Div(
                children=[
                    html.P(
                        className='active-alarms-modal-title',
                        children=['Detalle de alarmas'],
                    ),
                    html.Div(
                        className='active-alarms-modal-subtitle',
                        children=['Alarmas activas / Alarmas aún activas después de la gestión'],
                    ),
                    html.Div(
                        className='active-alarms-modal-updated-wrapper',
                        children=[
                            html.I(className='bi bi-clock'),
                            html.Span(
                                id=ActiveAlarmsModalIds.LAST_UPDATED_TEXT,
                                children='Sin actualización',
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className='active-alarms-modal-header-actions',
                children=[
                    dbc.Button(
                        children=[
                            html.I(className='bi bi-arrow-clockwise me-2'),
                            html.Span('Actualizar'),
                        ],
                        id=ActiveAlarmsModalIds.REFRESH_BUTTON,
                        color='light',
                        className='active-alarms-refresh-button',
                        n_clicks=0,
                    ),
                ],
            ),
        ],
    )
