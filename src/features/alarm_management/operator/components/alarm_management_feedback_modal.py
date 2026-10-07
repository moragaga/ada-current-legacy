from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from ..ids import build_alarm_management_operator_ids


def build_alarm_management_feedback_modal() -> dbc.Modal:
    ids = build_alarm_management_operator_ids()

    return dbc.Modal(
        id=ids['feedback_modal'],
        is_open=False,
        backdrop='static',
        centered=True,
        keyboard=False,
        style={
            '--bs-modal-width': '30%',
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
                                id=ids['feedback_title'],
                                className='p-0 m-0 text-center w-100 fw-bold font-alarm-management-header',
                                children=['Información'],
                            ),
                            html.I(
                                id=ids['feedback_modal_close_button'],
                                className='bi bi-x-lg active-cursor',
                                n_clicks=0,
                            ),
                        ],
                    ),
                ],
            ),
            dbc.ModalBody(
                children=[
                    html.P(
                        id=ids['feedback_message'],
                        className='text-center m-0 font-alarm-management-summary-name',
                        children=[''],
                    ),
                ],
            ),
            dbc.ModalFooter(
                className='d-flex justify-content-center',
                children=[
                    dbc.Button(
                        id=ids['feedback_modal_footer_close_button'],
                        color='secondary',
                        className='w-50 app-close-button-host',
                        n_clicks=0,
                        children=['Cerrar'],
                    ),
                ],
            ),
        ],
    )
