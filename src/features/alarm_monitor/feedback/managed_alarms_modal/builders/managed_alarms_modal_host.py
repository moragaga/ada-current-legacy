from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from ..components import (
    build_initial_summary_state,
    build_managed_alarm_panel_shell,
    build_managed_alarms_modal_footer,
    build_managed_alarms_modal_toolbar,
)
from ..constants import (
    ITEMS_CONTENT_SIDE_SHOW_CLASSNAME,
)
from ..graphs.recurrence_figure import (
    build_empty_recurrence_figure,
)
from ..ids import (
    ManagedAlarmsModalIds,
)


def build_managed_alarms_modal_host() -> html.Div:
    return html.Div(
        children=[
            dcc.Store(
                id=ManagedAlarmsModalIds.FROZEN_SNAPSHOT_STORE,
                storage_type='memory',
            ),
            dcc.Store(
                id=ManagedAlarmsModalIds.ITEMS_PAGE_STORE,
                data=1,
                storage_type='memory',
            ),
            dbc.Modal(
                id=ManagedAlarmsModalIds.MODAL,
                is_open=False,
                style={'--bs-modal-width': '98%'},
                scrollable=True,
                backdrop='static',
                centered=True,
                keyboard=False,
                class_name='managed-alarms-modal',
                children=[
                    dbc.ModalHeader(
                        close_button=False,
                        className='d-flex justify-content-end align-items-center py-0 px-3 modal-background',
                        children=[
                            dbc.Button(
                                html.I(className='bi bi-x-lg text-white'),
                                id=ManagedAlarmsModalIds.CLOSE_BUTTON,
                                color='link',
                                className='managed-alarms-close-button',
                                n_clicks=0,
                            ),
                        ],
                    ),
                    dbc.ModalBody(
                        className='managed-alarms-modal-body',
                        children=[
                            _build_information(),
                            build_managed_alarms_modal_toolbar(),
                            _build_managed_alarms_modal_content_shell(),
                            build_managed_alarms_modal_footer(),
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_information() -> html.Div:
    return html.Div(
        className='managed-alarms-modal-header',
        children=[
            html.Div(
                children=[
                    html.P(
                        className='managed-alarms-modal-title',
                        children=['Detalle de alarmas gestionadas'],
                    ),
                    html.Div(
                        className='managed-alarms-modal-subtitle',
                        children=[
                            'Gestiones efectivas, tendencia de activaciones y seguimiento operacional.'
                        ],
                    ),
                    html.Div(
                        className='managed-alarms-modal-updated-wrapper',
                        children=[
                            html.I(className='bi bi-clock'),
                            html.Span(
                                id=ManagedAlarmsModalIds.LAST_UPDATED_TEXT,
                                children='Sin actualización',
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className='managed-alarms-modal-header-actions',
                children=[
                    dbc.Button(
                        children=[
                            html.I(className='bi bi-arrow-clockwise me-2'),
                            html.Span('Actualizar'),
                        ],
                        id=ManagedAlarmsModalIds.REFRESH_BUTTON,
                        color='light',
                        className='managed-alarms-refresh-button',
                        n_clicks=0,
                    ),
                ],
            ),
        ],
    )


def _build_managed_alarms_modal_content_shell() -> dbc.Row:
    return html.Div(
        className='managed-alarms-content-shell',
        children=[
            html.Div(
                className='managed-alarms-main-column d-flex flex-fill',
                children=[
                    build_managed_alarm_panel_shell(),
                ],
            ),
            html.Div(
                id=ManagedAlarmsModalIds.ITEMS_SIDE_CONTENT,
                className=ITEMS_CONTENT_SIDE_SHOW_CLASSNAME,
                children=[
                    _build_summary_card(),
                    _build_chart_card(),
                ],
            ),
        ],
    )


def _build_summary_card() -> dbc.Card:
    return dbc.Card(
        className='managed-alarms-context-card flex-fill',
        children=[
            dbc.CardHeader(
                className='managed-alarms-panel-header',
                children=[
                    html.Div(
                        className='managed-alarms-panel-title-wrapper',
                        children=[
                            html.I(
                                className=('bi bi-clipboard-data managed-alarms-panel-icon'),
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        className='managed-alarms-panel-title',
                                        children=['Contexto analítico'],
                                    ),
                                    html.Div(
                                        className='managed-alarms-panel-subtitle',
                                        children=['Resumen de gestiones y tendencia operacional.'],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                id=ManagedAlarmsModalIds.SUMMARY_CONTAINER,
                className='managed-alarms-summary-grid h-100',
                children=[build_initial_summary_state()],
            ),
        ],
    )


def _build_chart_card() -> dbc.Card:
    return dbc.Card(
        className='managed-alarms-chart-card flex-fill justify-content-between',
        children=[
            dbc.CardHeader(
                className='managed-alarms-panel-header',
                children=[
                    html.Div(
                        className='managed-alarms-panel-title-wrapper',
                        children=[
                            html.I(
                                className=('bi bi-graph-up-arrow managed-alarms-panel-icon'),
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        className='managed-alarms-panel-title',
                                        children=['Tendencia de recurrencia'],
                                    ),
                                    html.Div(
                                        className='managed-alarms-panel-subtitle',
                                        children=[
                                            'Activaciones representativas según turno seleccionado.'
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className='managed-alarms-chart-wrapper my-auto',
                children=[
                    dcc.Graph(
                        id=ManagedAlarmsModalIds.RECURRENCE_CHART,
                        className='managed-alarms-recurrence-chart',
                        config={
                            'displayModeBar': False,
                            'responsive': True,
                        },
                        figure=build_empty_recurrence_figure(
                            message='Esperando datos de tendencia.',
                        ),
                    ),
                ],
            ),
        ],
    )
