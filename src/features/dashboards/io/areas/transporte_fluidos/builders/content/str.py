from __future__ import annotations

from dash import html
from dash.development.base_component import Component


def build_str_content(kpis: dict):
    estado_bomba_003 = kpis.get('estado_bomba_003_inst')
    estado_bomba_004 = kpis.get('estado_bomba_004_inst')
    estado_bomba_1005 = kpis.get('estado_bomba_1005_inst')
    estado_bomba_1010 = kpis.get('estado_bomba_1010_inst')
    estado_bomba_1011 = kpis.get('estado_bomba_1011_inst')
    estado_str_36 = kpis.get('estado_str_36_inst')
    solido_entrada_str_36 = kpis.get('solido_entrada_str_36_inst')
    solido_salida_str_36 = kpis.get('solido_salida_str_36_inst')
    estado_str_28 = kpis.get('estado_str_28_inst')
    solido_entrada_str_28 = kpis.get('solido_entrada_str_28_inst')
    solido_salida_str_28 = kpis.get('solido_salida_str_28_inst')

    estado_tk_050 = kpis.get('estado_tk_050_inst')
    altura_tk_050 = kpis.get('altura_tk_050_inst')
    torque_tk_050 = kpis.get('torque_tk_050_inst')
    pendiente_tk_050 = kpis.get('pendiente_tk_050_inst')
    interfaz_tk_050 = kpis.get('interfaz_tk_050_inst')
    estado_alimentacion_tk_050 = kpis.get('estado_alimentacion_tk_050_inst')

    estado_tk_051 = kpis.get('estado_tk_051_inst')
    altura_tk_051 = kpis.get('altura_tk_051_inst')
    torque_tk_051 = kpis.get('torque_tk_051_inst')
    pendiente_tk_051 = kpis.get('pendiente_tk_051_inst')
    interfaz_tk_051 = kpis.get('interfaz_tk_051_inst')
    estado_alimentacion_tk_051 = kpis.get('estado_alimentacion_tk_051_inst')

    estado_tk_712 = kpis.get('estado_tk_712_inst')
    altura_tk_712 = kpis.get('altura_tk_712_inst')
    torque_tk_712 = kpis.get('torque_tk_712_inst')
    pendiente_tk_712 = kpis.get('pendiente_tk_712_inst')
    interfaz_tk_712 = kpis.get('interfaz_tk_712_inst')
    estado_alimentacion_tk_712 = kpis.get('estado_alimentacion_tk_712_inst')

    return html.Div(
        className='d-flex flex-column gap-1',
        children=[
            html.Div(
                className='d-flex flex-column gap-1',
                children=[
                    _title('Espesadores'),
                    _espesador(estado=estado_tk_050, label='TK-50', altura=altura_tk_050, torque=torque_tk_050, pendiente=pendiente_tk_050, interfaz=interfaz_tk_050, estado_alimentacion=estado_alimentacion_tk_050),
                    _espesador(estado=estado_tk_051, label='TK-51', altura=altura_tk_051, torque=torque_tk_051, pendiente=pendiente_tk_051, interfaz=interfaz_tk_051, estado_alimentacion=estado_alimentacion_tk_051),
                    _espesador(estado=estado_tk_712, label='TK-712', altura=altura_tk_712, torque=torque_tk_712, pendiente=pendiente_tk_712, interfaz=interfaz_tk_712, estado_alimentacion=estado_alimentacion_tk_712),
                ]
            ),
            html.Div(
                className='d-flex flex-column gap-1',
                children=[
                    _title('Ductos STR'),
                    html.Div(
                        className='d-flex justify-content-evenly',
                        children=[
                            _build_ductos(
                                label='36', estado=estado_str_36, solido_1=solido_entrada_str_36, solido_2=solido_salida_str_36,
                                bombas_list=[{'label': 'PP003', 'estado': estado_bomba_003}, {'label': 'PP004', 'estado': estado_bomba_004}, {'label': 'PP1005', 'estado': estado_bomba_1005}]
                            ),
                            _build_ductos(
                                label='28', estado=estado_str_28, solido_1=solido_entrada_str_28, solido_2=solido_salida_str_28,
                                bombas_list=[{'label': 'PP1010', 'estado': estado_bomba_1010}, {'label': 'PP1011', 'estado': estado_bomba_1011}]
                            ),
                        ]
                    )
                ]
            )
        ]
    )



def _espesador(
        estado: str,
        label: str,
        torque: str,
        altura: str,
        pendiente: str,
        interfaz: str,
        estado_alimentacion,
):
    if estado_alimentacion == 'alimentando':
        estado_alim = 'operando'
    else:
        estado_alim = 'detenido'
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
                                src=f'assets/img/industrial/circle_status/{estado_alim}.svg'
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
                                                    'Pendiente'
                                                ]
                                            ),
                                            html.P(
                                                className='fw-bold',
                                                children=[
                                                    pendiente
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
                                                    'Interfaz (cms)'
                                                ]
                                            ),
                                            html.P(
                                                className='fw-bold',
                                                children=[
                                                    interfaz
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
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
                    #                     src=f'assets/img/industrial/circle_status/{estado_alim}.svg'
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


def _build_ductos(
    *,
    label: str,
    estado: str | Component,
    solido_1: str | Component,
    solido_2: str | Component,
    bombas_list: list[dict] | None = None,
):
    if estado == 'detenido':
        _estado = 'detenido'
    else:
        _estado = 'operando'
    return html.Div(
        className='d-flex flex-column gap-1',
        children=[
            html.Div(
                className='d-flex flex-column align-items-center',
                children=[
                    html.Div(
                        className='fs-io-bc-200 d-flex',
                        children=[
                            html.P(
                                className='pe-1',
                                children=['Ducto']
                            ),
                            html.P(
                                className='fw-bold',
                                children=[
                                    label
                                ]
                            ),
                            html.P(
                                className='',
                                children=['"']
                            )
                        ]
                    ),
                    html.Img(
                        className='img-fluid str-v1-img',
                        src=f'assets/img/industrial/str/{_estado}.svg'
                    ),
                    html.Div(
                        className='d-flex justify-content-evenly align-items-center w-100 fs-io-bc-200',
                        children=[
                            html.Div(
                                className='d-flex',
                                children=[
                                    html.P(
                                        className='fw-bold',
                                        children=[solido_1]
                                    ),
                                    html.P(
                                        className='',
                                        children=['%']
                                    ),
                                ]
                            ),
                            html.I(className='bi bi-arrow-right-short'),
                            html.P(
                                className='',
                                children=['Sólido']
                            ),
                            html.I(className='bi bi-arrow-right-short'),
                            html.Div(
                                className='d-flex',
                                children=[
                                    html.P(
                                        className='fw-bold',
                                        children=[solido_2]
                                    ),
                                    html.P(
                                        className='',
                                        children=['%']
                                    ),
                                ]
                            ),
                        ]
                    )
                ]
            ),
            html.Div(
                className='d-flex fs-io-bc-400 justify-content-center',
                children=[
                    _build_bomba(label=x.get('label'), estado=x.get('estado')) for x in bombas_list
                ]
            )
        ]
    )

def _build_bomba(
    *,
    label: str,
    estado: str | Component,
):
    return html.Div(
        className='d-flex flex-column align-items-center',
        children=[
            html.Img(
                className='img-fluid bomba-img',
                src=f'assets/img/industrial/bomba/{estado}.svg'
            ) if not isinstance(estado, Component) else estado,
            html.P(
                className='fw-bold',
                children=[label]
            )
        ]
    )