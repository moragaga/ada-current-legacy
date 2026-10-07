from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from ...components.alarm_management_primitives import (
    build_buttons_action,
    build_information_block,
    build_personalized_message_section,
    build_predefined_message_section,
    build_silence_section,
)
from ..ids import build_distributed_alarm_management_operator_ids


def build_distributed_alarm_bulk_management_modal() -> dbc.Modal:
    ids = build_distributed_alarm_management_operator_ids()

    return dbc.Modal(
        id=ids['bulk_modal'],
        is_open=False,
        backdrop='static',
        centered=True,
        keyboard=False,
        style={
            '--bs-modal-width': 'var(--modal-alarm-management-width)',
        },
        children=[
            dbc.ModalHeader(
                close_button=False,
                className='p-2 modal-background',
                children=[
                    html.Div(
                        className='d-flex align-items-center w-100',
                        children=[
                            html.P(
                                id=ids['bulk_title'],
                                className='p-0 m-0 text-center w-100 fw-bold font-alarm-management-header',
                                children=['Gestión masiva'],
                            ),
                            html.I(
                                id=ids['bulk_modal_close_button'],
                                className='bi bi-x-lg active-cursor',
                                n_clicks=0,
                            ),
                        ],
                    ),
                ],
            ),
            dbc.ModalBody(
                className='pt-2 background-primary',
                children=[
                    html.P(
                        id=ids['bulk_summary'],
                        className='m-0 pb-2 text-center fw-semibold font-alarm-management-summary-name',
                        children='',
                    ),
                    html.P(
                        id=ids['bulk_alarm_list_button'],
                        className='font-alarm-management-section d-flex '
                        'justify-content-center align-items-center text-white fw-semibold '
                        'active-cursor mb-2',
                        style={
                            'background': 'var(--dark-color)',
                            'borderRadius': '10px',
                            'padding': '.3rem',
                        },
                        children=['Ver listado de alarmas a gestionar'],
                        n_clicks=0,
                    ),
                    dbc.Collapse(
                        id=ids['bulk_alarm_list_collapse'],
                        children=[
                            dbc.Card(
                                className='p-2',
                                children=[
                                    html.Div(
                                        id=ids['bulk_alarm_list'],
                                        className='d-flex flex-column gap-2 bulk-alarm-list-wrapper',
                                        children=[],
                                    ),
                                ],
                            )
                        ],
                    ),
                    build_predefined_message_section(
                        id_message_dropdown=ids['bulk_message_dropdown'],
                        id_message_validation=ids['bulk_message_validation'],
                    ),
                    build_personalized_message_section(
                        id_personalized_message=ids['bulk_personalized_message'],
                        id_personalized_message_validation=ids[
                            'bulk_personalized_message_validation'
                        ],
                    ),
                    build_silence_section(
                        id_silence_checkbox=ids['bulk_silence_checkbox'],
                        id_silence_information=ids['bulk_silence_information'],
                        id_silence_container=ids['bulk_silence_container'],
                        id_silence_dropdown=ids['bulk_silence_dropdown'],
                        id_silence_validation=ids['bulk_silence_validation'],
                        is_distributed=True,
                    ),
                    build_information_block(is_distributed=True),
                ],
            ),
            dbc.ModalFooter(
                className='d-flex flex-nowrap gap-2 background-primary',
                children=build_buttons_action(
                    id_save_button=ids['bulk_modal_save_button'],
                    id_cancel_button=ids['bulk_modal_cancel_button'],
                    is_distributed=True,
                ),
            ),
        ],
    )
