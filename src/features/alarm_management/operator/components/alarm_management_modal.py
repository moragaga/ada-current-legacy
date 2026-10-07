from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from ..ids import build_alarm_management_operator_ids


def build_alarm_management_modal() -> dbc.Modal:
    ids = build_alarm_management_operator_ids()

    return dbc.Modal(
        id=ids['modal'],
        is_open=False,
        backdrop='static',
        centered=True,
        keyboard=False,
        style={
            '--bs-modal-width': '35%',
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
                className='pt-2',
                children=[
                    _build_alarm_summary(ids=ids),
                    _build_warning(ids=ids),
                    _build_predefined_message_section(ids=ids),
                    _build_personalized_message_section(ids=ids),
                    _build_silence_section(ids=ids),
                    _build_information_block(),
                ],
            ),
            dbc.ModalFooter(
                className='d-flex flex-nowrap gap-2',
                children=[
                    dbc.Button(
                        id=ids['modal_cancel_button'],
                        color='secondary',
                        outline=True,
                        className='w-50',
                        n_clicks=0,
                        children=['Cancelar'],
                    ),
                    dbc.Button(
                        id=ids['modal_save_button'],
                        color='primary',
                        className='w-50 app-running-button-host',
                        n_clicks=0,
                        children=['Gestionar'],
                    ),
                ],
            ),
        ],
    )


def _build_alarm_summary(
    *,
    ids: dict[str, str],
) -> html.Div:
    return html.Div(
        className='d-flex flex-column align-items-center text-center pb-3',
        children=[
            html.Div(
                className='d-flex justify-content-center align-items-center gap-2',
                children=[
                    html.I(
                        className='bi bi-exclamation-triangle',
                    ),
                    html.P(
                        id=ids['alarm_title'],
                        className='p-0 m-0 fw-semibold',
                        children=[''],
                    ),
                ],
            ),
            html.P(
                id=ids['alarm_cause'],
                className='p-0 m-0 pt-1 fst-italic',
                children=[''],
            ),
        ],
    )


def _build_warning(
    *,
    ids: dict[str, str],
) -> html.Div:
    return html.Div(
        id=ids['alarm_warning'],
        className='d-none',
        children=[''],
    )


def _build_predefined_message_section(
    *,
    ids: dict[str, str],
) -> html.Div:
    return html.Div(
        className='pt-2',
        children=[
            _build_section_title(text='Mensaje predefinido'),
            dcc.Dropdown(
                id=ids['message_dropdown'],
                className='pt-2',
                placeholder='Seleccione una opción',
                clearable=True,
                disabled=True,
                options=[],
                value=None,
            ),
            html.Span(
                id=ids['message_validation'],
                className='d-none',
                style=_error_style(),
                children=[''],
            ),
        ],
    )


def _build_personalized_message_section(
    *,
    ids: dict[str, str],
) -> html.Div:
    return html.Div(
        className='pt-3',
        children=[
            _build_section_title(text='Descripción'),
            dcc.Textarea(
                id=ids['personalized_message'],
                className='w-100 mt-2 p-2',
                placeholder='Ingrese un mensaje personalizado',
                value='',
                style={
                    'height': '10vh',
                    'maxHeight': '15vh',
                    'outlineColor': '#313131',
                    'resize': 'vertical',
                },
            ),
            html.Span(
                id=ids['personalized_message_validation'],
                className='d-none',
                style=_error_style(),
                children=[''],
            ),
        ],
    )


def _build_silence_section(
    *,
    ids: dict[str, str],
) -> html.Div:
    return html.Div(
        className='pt-3',
        children=[
            html.Div(
                className='d-flex align-items-center gap-3',
                children=[
                    _build_section_title(text='Desactivar alarma'),
                    dbc.Checkbox(
                        id=ids['silence_checkbox'],
                        value=False,
                        disabled=True,
                    ),
                ],
            ),
            html.P(
                id=ids['silence_information'],
                className='m-0 pt-2 fst-italic',
                style={
                    'fontSize': '0.9rem',
                },
                children=[''],
            ),
            html.Div(
                id=ids['silence_container'],
                className='d-none',
                children=[
                    dcc.Dropdown(
                        id=ids['silence_dropdown'],
                        className='pt-2',
                        placeholder='Seleccione una opción',
                        clearable=True,
                        disabled=True,
                        options=[],
                        value=None,
                    ),
                    html.Span(
                        id=ids['silence_validation'],
                        className='d-none',
                        style=_error_style(),
                        children=[''],
                    ),
                ],
            ),
        ],
    )


def _build_information_block() -> html.Div:
    return html.Div(
        className='d-flex flex-column pt-3',
        children=[
            _build_info_text(
                text='* Se puede ingresar una descripción o seleccionar un mensaje predefinido.'
            ),
            _build_info_text(text='* No es obligatorio desactivar una alarma.'),
            _build_info_text(text='* La gestión se verá reflejada en los próximos minutos.'),
        ],
    )


def _build_section_title(
    *,
    text: str,
) -> html.P:
    return html.P(
        className='m-0 fw-bold',
        children=[text],
    )


def _build_info_text(
    *,
    text: str,
) -> html.P:
    return html.P(
        className='m-0 fst-italic',
        style={
            'fontSize': '0.9rem',
            'color': '#000000',
        },
        children=[text],
    )


def _error_style() -> dict[str, str]:
    return {
        'color': '#DC3545',
        'fontStyle': 'italic',
        'fontSize': '0.9rem',
    }
