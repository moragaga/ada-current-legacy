from __future__ import annotations

from dash import html
from dash.development.base_component import Component
from src.shared.ui.charts.level_gauge import LevelGaugeDefinition, map_level_gauge


def build_stc_content(kpis: dict):

    estado_tk_711 = kpis.get('estado_tk_711_inst')
    altura_tk_711 = kpis.get('altura_tk_711_inst')
    torque_tk_711 = kpis.get('torque_tk_711_inst')
    flujo_tk_711 = kpis.get('flujo_tk_711_inst')
    solido_tk_711 = kpis.get('solido_tk_711_inst')
    estado_alimentacion_tk_711 = kpis.get('estado_alimentacion_tk_711_inst')

    return html.Div(
        className='d-flex flex-column gap-1',
        children=[
            html.Div(
                className='d-flex flex-column gap-1',
                children=[
                    _title('Espesadores'),
                    _espesador(estado=estado_tk_711, label='TK-711', altura=altura_tk_711, torque=torque_tk_711, flujo=flujo_tk_711, solido=solido_tk_711, estado_alimentacion=estado_alimentacion_tk_711),
                ]
            ),
            html.Div(
                className='d-flex flex-column gap-1',
                children=[
                    _title('--'),
                    html.Div(
                        className='d-flex justify-content-center w-100',
                        children=[
                            _level_gauge(tk_number='20', kpis=kpis),
                            _level_gauge(tk_number='21', kpis=kpis),
                        ]
                    ),
                ]
            )
        ]
    )

def _level_gauge(tk_number: str, kpis: dict):
    definition = LevelGaugeDefinition(
        number=tk_number,
        variant='tk',
        image_name='tk',
        name_prefix='TK',
        tag_prefix='tk',
    )

    data = map_level_gauge(
        definition=definition,
        kpis=kpis,
    )

    return data.to_component()


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
