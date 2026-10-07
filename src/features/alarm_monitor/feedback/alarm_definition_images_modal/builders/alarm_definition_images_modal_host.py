from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from ..ids import AlarmDefinitionImagesModalIds


def build_alarm_definition_images_modal_host() -> dbc.Modal:
    return dbc.Modal(
        id=AlarmDefinitionImagesModalIds.MODAL,
        is_open=False,
        style={'--bs-modal-width': '70%'},
        # scrollable=True,
        backdrop='static',
        centered=True,
        keyboard=False,
        className='alarm-definition-images-modal',
        children=[
            dbc.ModalHeader(
                className='modal-background px-1 py-0',
                close_button=False,
                children=[
                    html.Div(
                        className='d-flex align-items-center w-100',
                        children=[
                            html.P(
                                id=AlarmDefinitionImagesModalIds.TITLE,
                                className='p-0 m-0 text-center w-100 fw-bold font-alarm-image-definition-header',
                                children=['Imágenes de alarma'],
                            ),
                            dbc.Button(
                                html.I(className='bi bi-x-lg text-white'),
                                id=AlarmDefinitionImagesModalIds.CLOSE_BUTTON,
                                color='link',
                                className='active-alarms-close-button',
                                n_clicks=0,
                            ),
                        ],
                    )
                ],
            ),
            dbc.ModalBody(
                id=AlarmDefinitionImagesModalIds.BODY,
                className='alarm-definition-images-modal-body p-0',
                children=_build_empty_body(),
            ),
        ],
    )


def _build_empty_body() -> html.Div:
    return html.Div(
        className='alarm-definition-images-modal-empty',
        children='Selecciona una alarma para ver sus imágenes asociadas.',
    )
