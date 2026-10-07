from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.features.admin_framework.components import build_admin_page_header
from src.features.admin_framework.services import AdminGridService
from src.features.configuration.services import SchemaBuilderService

from .definition import ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION
from .ids import build_alarm_management_message_admin_ids
from .schema import ALARM_MANAGEMENT_MESSAGE_ROW_SCHEMA


def build_alarm_management_messages_admin_layout() -> html.Div:
    ids = build_alarm_management_message_admin_ids()
    column_defs = SchemaBuilderService.build_column_defs(ALARM_MANAGEMENT_MESSAGE_ROW_SCHEMA)

    configuration = AdminGridService.default_configuration()
    configuration.class_name += ' alarm-management-messages-configuration'

    return html.Div(
        id=ids['container'],
        className='p-0',
        children=[
            build_admin_page_header(ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION.title),
            html.Div(id=ids['toast_host']),
            html.Div(
                className='p-3',
                children=[
                    dcc.Store(id=ids['init'], data={'ready': True}),
                    dcc.Store(id=ids['snapshot']),
                    dbc.Card(
                        children=[
                            dbc.CardBody(
                                children=[
                                    _build_toolbar(ids=ids),
                                    dcc.Loading(
                                        id=ids['loading'],
                                        type='default',
                                        parent_className='loading-component-alarm-management-messages-admin',
                                        display='show',
                                        className='loading-component-spinner',
                                        children=AdminGridService.create_table(
                                            table_id=ids['grid'],
                                            row_data=[],
                                            column_defs=column_defs,
                                            configuration=configuration,
                                        ),
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
            ),
        ],
    )


def _build_toolbar(ids: dict[str, str]) -> html.Div:
    return html.Div(
        className='d-flex flex-wrap gap-2 align-items-end justify-content-between mb-3',
        children=[
            html.Div(
                className='flex-grow-1',
                children=[
                    html.Label(
                        className='fw-semibold mb-1 alarm-management-configuration-label',
                        children=['Grupo de mensajes'],
                    ),
                    dcc.Dropdown(
                        id=ids['bucket_selector'],
                        options=[],
                        value=None,
                        clearable=False,
                        placeholder='Seleccione Globales o un grupo de mensajes',
                    ),
                ],
            ),
            dbc.ButtonGroup(
                className='admin-toolbar-buttons-wrapper',
                children=[
                    dbc.Button(
                        id=ids['reload_button'],
                        color='secondary',
                        outline=True,
                        n_clicks=0,
                        children=['Recargar'],
                    ),
                    dbc.Button(
                        id=ids['add_row_button'],
                        color='success',
                        outline=True,
                        n_clicks=0,
                        children=['Agregar fila'],
                    ),
                    dbc.Button(
                        id=ids['delete_rows_button'],
                        color='danger',
                        outline=True,
                        n_clicks=0,
                        children=['Eliminar seleccionadas'],
                    ),
                    dbc.Button(
                        id=ids['save_button'],
                        color='dark',
                        outline=True,
                        n_clicks=0,
                        children=['Guardar'],
                    ),
                ],
            ),
        ],
    )
