from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from ...mappers.colectiva import build_vertimil_mapper, build_bomba_mapper

def build_colectiva_content(kpis: dict):
    return html.Div(
        className='d-flex gap-2 flex-column',
        children=[
            html.Div(
                className='d-flex gap-1 flex-column',
                children=[
                    _title(title='Rougher (R1-R9)'),
                    html.Div(
                        className='rougher-state-grid',
                        children=[
                            state_component(label='R1', state='operando'),
                            state_component(label='R2', state='detenido'),
                            state_component(label='R3', state='operando'),
                            state_component(label='R4', state='detenido'),
                            state_component(label='R5', state='operando'),
                            state_component(label='R6', state='detenido'),
                            state_component(label='R7', state='operando'),
                            state_component(label='R8', state='detenido'),
                            state_component(label='R9', state='detenido'),
                        ]
                    )
                ]
            ),
            html.Div(
                className='d-flex flex-column gap-1',
                children=[
                    _title(title='Molinos Verticales'),
                    html.Div(
                        className='d-flex gap-1 align-items-center',
                        children=[
                            html.Span(
                                className='w-100',
                                children=[build_vertimil_mapper(kpis=kpis).to_component(), ]
                            ),
                            html.Span(
                                className='w-100',
                                children=[build_bomba_mapper(kpis=kpis).to_component(), ]
                            )
                        ]
                    ),
                    html.Div(
                        className='d-flex justify-content-between w-100 app-border-bottom',
                        children=[
                            html.P(
                                className='fs-io-bc-200',
                                children=['N° Columnas']
                            ),
                            html.Div(
                                className='d-flex',
                                children=[
                                    html.P(
                                        className='fs-io-bc-200 fw-bold',
                                        children=['10']
                                    ),
                                    html.P(
                                        className='fs-io-bc-200',
                                        children=['/']
                                    ),
                                    html.P(
                                        className='fs-io-bc-200',
                                        children=['14']
                                    )
                                ]
                            )
                        ]
                    )
                ]
            ),
            html.Div(
                className='d-flex gap-1 flex-column',
                children=[
                    _title(title='Scavenger (SC1 - SC2)'),
                    html.Div(
                        className='d-flex gap-1',
                        children=[
                            state_component(label='SC1', state='operando'),
                            state_component(label='SC2', state='detenido')
                        ]
                    )
                ]
            ),
        ]
    )

def _title(title: str) -> Component:
    return html.Div(
        className='display-section-title fs-io-bc-100',
        children=[html.P(children=[title])],
    )

def state_component(label: str, state: str):
    normalized_state = state.strip().lower()

    return html.Span(
        className='flotation-state',
        children=[
            html.P(
                className='flotation-state__label fs-io-bc-100 fw-bold',
                children=label,
            ),
            html.Div(
                className='w-100 d-flex justify-content-center',
                children=[
                    html.Img(
                        className='flotation-state__icon',
                        src='assets/img/industrial/circle_status/{0}.svg'.format(normalized_state),
                        alt=normalized_state.capitalize(),
                    ),
                ]
            )
        ],
    )
