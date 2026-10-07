from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from ...components.alarm_management_primitives import (
    build_alarm_summary,
    build_buttons_action,
    build_information_block,
    build_personalized_message_section,
    build_predefined_message_section,
    build_silence_section,
    build_warning,
)
from ..ids import (
    build_distributed_alarm_management_operator_ids,
)


def build_distributed_alarm_management_modal() -> dbc.Modal:
    ids = build_distributed_alarm_management_operator_ids()

    return dbc.Modal(
        id=ids['modal'],
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
                                id=ids['modal_title'],
                                className='p-0 m-0 text-center w-100 fw-bold font-alarm-management-header',
                                children=['Gestión de alarma'],
                            ),
                            html.I(
                                id=ids['modal_close_button'],
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
                    build_alarm_summary(ids=ids),
                    build_warning(id_warning=ids['alarm_warning']),
                    build_predefined_message_section(
                        id_message_dropdown=ids['message_dropdown'],
                        id_message_validation=ids['message_validation'],
                    ),
                    build_personalized_message_section(
                        id_personalized_message=ids['personalized_message'],
                        id_personalized_message_validation=ids['personalized_message_validation'],
                    ),
                    build_silence_section(
                        id_silence_checkbox=ids['silence_checkbox'],
                        id_silence_information=ids['silence_information'],
                        id_silence_container=ids['silence_container'],
                        id_silence_dropdown=ids['silence_dropdown'],
                        id_silence_validation=ids['silence_validation'],
                    ),
                    build_information_block(),
                ],
            ),
            dbc.ModalFooter(
                className='d-flex flex-nowrap gap-2 background-primary',
                children=build_buttons_action(
                    id_save_button=ids['modal_save_button'],
                    id_cancel_button=ids['modal_cancel_button'],
                ),
            ),
        ],
    )
