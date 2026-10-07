from __future__ import annotations

from dash import html
import dash_bootstrap_components as dbc
from dash.development.base_component import Component
from src.shared.ui.theme import resolve_color_class

DISPLAY_CARD_STATUS_BACKDROP_TYPE = 'display-card-status-backdrop'



def build_information_content(kpis: dict):
    return html.Div(
        className='position-relative d-flex justify-content-evenly align-items-center h-100 w-100',
        children=[
            # _build_group_content(group_number='3', operation='Mina', gestion_progress=76),
            # _build_group_content(group_number='1', operation='Planta', gestion_progress=45),
            build_status_backdrop(uuid='header-information-alarm-uuid')
        ]
    )


def _build_group_content(
    *,
    group_number: str,
    operation: str,
    gestion_progress: float| int | Component ,
):
    return html.Div(
        className='d-flex flex-column align-items-start',
        children=[
            _build_isolated_content(
                label=f'Grupo {operation.title()}',
                value=f'G{group_number}',
            ),
            _build_isolated_content(
                label=f'Gestión {operation.title()}',
                value=gestion_progress,
                is_progres=True,
            ),
        ]
    )

def _build_isolated_content(
    *,
    label: str,
    value: str | float| int | Component,
    is_progres:bool = False,
):

    if is_progres:
        if value > 75:
            color = resolve_color_class(value=None, default='background-gray')
            text = resolve_color_class(value=None, default='text-gray')
        elif value > 50:
            color = resolve_color_class(value='2', color_type='background')
            text = resolve_color_class(value='2', color_type='text')
        else:
            color = resolve_color_class(value='1', color_type='background')
            text = resolve_color_class(value='1', color_type='text')

        color = color.split('-')[1]

        component = html.Div(
            className='d-flex flex-column',
            children=[
                html.P(className=f'{text} fs-io-hg-200 fw-bold', children=[f'{value}%']),
                dbc.Progress(value=value, class_name=f'header-information-alarm-gestion {color}')
            ]
        )
    else:
        component = html.P(
            className='fw-bold fs-io-hg-200',
            children=[value],
        )

    return html.Div(
        className='d-flex flex-column',
        children=[
            html.P(
                className='fs-io-hg-300',
                children=[label],
            ),
            component
        ]
    )

def build_status_backdrop(
    *,
    uuid: str,
    message: str = 'Datos desactualizados',
) -> Component:
    return html.Div(
        # id={
        #     'type': DISPLAY_CARD_STATUS_BACKDROP_TYPE,
        #     'index': uuid,
        # },
        className='display-card-backdrop display-card-backdrop--visible',
        children=[
            html.Div(
                className='display-card-backdrop__content',
                children=[
                    html.I(
                        className=(
                            'bi bi-hammer '
                            'display-card-backdrop__icon'
                        ),
                    ),
                    html.P(
                        className='display-card-backdrop__message',
                        children=['En construcción'],
                    ),
                ],
            ),
        ],
    )