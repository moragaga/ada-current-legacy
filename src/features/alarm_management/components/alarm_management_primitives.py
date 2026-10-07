from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html


def build_alarm_summary(
    *,
    ids: dict[str, str],
) -> html.Div:
    return html.Div(
        className='d-flex flex-column align-items-center text-center pb-3',
        children=[
            html.Div(
                className='d-flex justify-content-center align-items-center font-alarm-management-summary-name',
                children=[
                    html.P(
                        id=ids['alarm_title'],
                        className='p-0 m-0 fw-semibold',
                        children=[''],
                    ),
                ],
            ),
            html.P(
                id=ids['alarm_cause'],
                className='p-0 m-0 pt-1 fst-italic font-alarm-management-summary-cause',
                children=[''],
            ),
        ],
    )


def build_warning(*, id_warning: str) -> html.Div:
    return html.Div(
        id=id_warning,
        className='d-none',
        children=[''],
    )


def build_predefined_message_section(
    *,
    id_message_dropdown: str,
    id_message_validation: str,
) -> html.Div:
    return html.Div(
        className='pt-2',
        children=[
            _build_section_title(text='Mensaje predefinido'),
            dcc.Dropdown(
                id=id_message_dropdown,
                className='pt-2',
                placeholder='Seleccione una opción',
                clearable=True,
                disabled=True,
                options=[],
                value=None,
            ),
            html.Span(
                id=id_message_validation,
                className='d-none',
                style=_error_style(),
                children=[''],
            ),
        ],
    )


def build_personalized_message_section(
    *,
    id_personalized_message: str,
    id_personalized_message_validation: str,
) -> html.Div:
    return html.Div(
        className='pt-3',
        children=[
            _build_section_title(text='Descripción'),
            dcc.Textarea(
                id=id_personalized_message,
                className='w-100 mt-2 p-2',
                placeholder='Ingrese un mensaje personalizado',
                value='',
                style={
                    'height': '15vh',
                    'maxHeight': '20vh',
                    'outlineColor': '#313131',
                    'resize': 'vertical',
                },
            ),
            html.Span(
                id=id_personalized_message_validation,
                className='d-none',
                style=_error_style(),
                children=[''],
            ),
        ],
    )


def build_silence_section(
    *,
    id_silence_checkbox: str,
    id_silence_information: str,
    id_silence_container: str,
    id_silence_dropdown: str,
    id_silence_validation: str,
    is_distributed: bool = False,
) -> html.Div:
    section_title = 'Desactivar alarmas' if is_distributed else 'Desactivar alarma'
    return html.Div(
        className='pt-3',
        children=[
            html.Div(
                className='d-flex align-items-center gap-3',
                children=[
                    _build_section_title(text=section_title),
                    dbc.Checkbox(
                        id=id_silence_checkbox,
                        value=False,
                        disabled=True,
                    ),
                ],
            ),
            html.P(
                id=id_silence_information,
                className='m-0 pt-2 fst-italic font-alarm-management-silence-information',
                children=[''],
            ),
            html.Div(
                id=id_silence_container,
                className='d-none',
                children=[
                    dcc.Dropdown(
                        id=id_silence_dropdown,
                        className='pt-2',
                        placeholder='Seleccione una opción',
                        clearable=True,
                        disabled=True,
                        options=[],
                        value=None,
                    ),
                    html.Span(
                        id=id_silence_validation,
                        className='d-none',
                        style=_error_style(),
                        children=[''],
                    ),
                ],
            ),
        ],
    )


def build_information_block(is_distributed: bool = False) -> html.Div:
    information = []
    if is_distributed:
        information = [
            _build_info_text(text='* Se registrará una gestión por cada alarma listada.'),
            _build_info_text(
                text='* Internamente validará si alguna ya fue gestionada o dejó de estar activa.'
            ),
        ]

    return html.Div(
        className='d-flex flex-column pt-3',
        children=[
            _build_info_text(
                text='* Se puede ingresar una descripción o seleccionar un mensaje predefinido.'
            ),
            _build_info_text(text='* No es obligatorio desactivar una alarma.'),
            _build_info_text(text='* La gestión se verá reflejada en los próximos minutos.'),
            *information,
        ],
    )


def build_buttons_action(
    id_save_button: str,
    id_cancel_button: str,
    is_distributed: bool = False,
):
    save_message = 'Gestionar grupo' if is_distributed else 'Gestionar'
    return [
        dbc.Button(
            id=id_cancel_button,
            color='danger',
            outline=True,
            className='w-50 app-close-button-host',
            n_clicks=0,
            children=['Cancelar'],
        ),
        dbc.Button(
            id=id_save_button,
            color='dark',
            className='w-50 app-running-button-host',
            n_clicks=0,
            children=[save_message],
        ),
    ]


def _build_section_title(
    *,
    text: str,
) -> html.P:
    return html.P(
        className='m-0 fw-bold font-alarm-management-section',
        children=[text],
    )


def _build_info_text(
    *,
    text: str,
) -> html.P:
    return html.P(
        className='m-0 fst-italic',
        style={
            'fontSize': 'var(--font-size-alarm-management-info-text)',
            'color': '#000000',
        },
        children=[text],
    )


def _error_style() -> dict[str, str]:
    return {
        'color': '#DC3545',
        'fontStyle': 'italic',
        'fontSize': 'var(--font-size-alarm-management-validation-error)',
    }
