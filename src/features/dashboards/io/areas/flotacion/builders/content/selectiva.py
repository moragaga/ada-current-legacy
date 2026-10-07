from __future__ import annotations

from dash import html
from dash.development.base_component import Component


def build_selectiva_content(kpis: dict):

    espesadores = []

    for tk_number in ('10', '12', '13', '55', '56'):
        espesadores.append(
            _espesador(
                estado=kpis.get(f'tk_{tk_number}_estado_inst'),
                label='TK-{0}'.format(tk_number),
                torque=kpis.get(f'tk_{tk_number}_torque_inst'),
                altura=kpis.get(f'tk_{tk_number}_altura_inst'),
                flujo=kpis.get(f'tk_{tk_number}_flujo_inst'),
                solido=kpis.get(f'tk_{tk_number}_solido_inst'),
                estado_alimentacion=kpis.get(f'tk_{tk_number}_estado_alimentacion_inst'),
            )
        )


    return html.Div(
        className='d-flex flex-column gap-1',
        children=[
            _title('Espesadores'),
            *espesadores
        ]
    )


def _espesador(estado: str, label: str, altura, torque, flujo, solido, estado_alimentacion: str):
    if estado_alimentacion == 'alimentando':
        _estado_alimentacion = 'operando'
    else:
        _estado_alimentacion = 'detenido'

    return html.Div(
        className='d-flex gap-1 fs-io-bc-400',
        style={
            'border': '1px solid var(--soft-border-color)',
            'border-radius': '5px',
            'padding': '.2rem .1rem'
        },
        children=[
            html.Div(
                className='d-flex w-100 align-items-start',
                children=[
                    html.Div(
                        style={
                            'border': '1px solid var(--soft-border-color)',
                            'border-radius': '5px',
                            'padding': '.1rem'
                        },
                        children=[
                            html.Img(
                                className='flotation-state__icon',
                                src=f'assets/img/industrial/circle_status/{_estado_alimentacion}.svg'
                            ),
                        ]
                    ),
                    html.Div(
                        className='d-flex flex-column align-items-center w-100 gap-1',
                        children=[
                            html.Img(
                                className='img-fluid espesador-v1-img',
                                src=f'assets/img/industrial/espesador/{estado}.svg'
                            ),
                            html.P(
                                className='fw-bold fs-io-bc-200',
                                children=[label]
                            )
                        ]
                    ),
                ]
            ),
            html.Div(
                className='d-flex flex-column w-100',
                children=[
                    html.Div(
                        className='d-flex w-100 gap-1',
                        children=[
                            html.Div(
                                className='d-flex flex-column align-items-center w-100',
                                children=[
                                    html.Span(
                                        className='d-flex justify-content-between w-100 app-border-bottom',
                                        children=[
                                            html.P(
                                                className='',
                                                children=[
                                                    'Altura (%)'
                                                ]
                                            ),
                                            html.P(
                                                className='fw-bold',
                                                children=[
                                                    altura
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Span(
                                        className='d-flex justify-content-between w-100',
                                        children=[
                                            html.P(
                                                className='',
                                                children=[
                                                    'Torque (%)'
                                                ]
                                            ),
                                            html.P(
                                                className='fw-bold',
                                                children=[
                                                    torque
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Span(
                                        className='d-flex justify-content-between w-100 app-border-bottom',
                                        children=[
                                            html.P(
                                                className='',
                                                children=[
                                                    'Flujo (t/h)'
                                                ]
                                            ),
                                            html.P(
                                                className='fw-bold',
                                                children=[
                                                    flujo
                                                ]
                                            ),
                                        ]
                                    ),
                                    html.Span(
                                        className='d-flex justify-content-between w-100',
                                        children=[
                                            html.P(
                                                className='',
                                                children=[
                                                    'Sólido (%)'
                                                ]
                                            ),
                                            html.P(
                                                className='fw-bold',
                                                children=[
                                                    solido
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    ),
                    # html.Div(
                    #     className='d-flex align-items-center w-100',
                    #     style={
                    #         'border': '1px solid var(--soft-border-color)',
                    #         'border-radius': '5px',
                    #     },
                    #     children=[
                    #         html.Span(
                    #             className='d-flex justify-content-center w-100 align-items-center',
                    #             children=[
                    #                 html.Img(
                    #                     className='flotation-state__icon',
                    #                     src=f'assets/img/industrial/circle_status/{_estado_alimentacion}.svg'
                    #                 ),
                    #                 html.P(
                    #                     className='fw-bold lh-1',
                    #                     children=[
                    #                         text
                    #                     ]
                    #                 ),
                    #             ]
                    #         ),
                    #
                    #     ]
                    # ),
                ]
            )
        ]
    )

def _title(title: str) -> Component:
    return html.Div(
        className='display-section-title fs-io-bc-100',
        children=[html.P(children=[title])],
    )