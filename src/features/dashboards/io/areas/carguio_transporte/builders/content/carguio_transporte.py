from __future__ import annotations

from ...mappers.carguio_transporte import build_gestion_carguio_turno_mapper

from dash import html

def build_carguio_transporte_content(kpis: dict):
    return html.Div(
        className='d-flex flex-column h-100 gap-2',
        children=[
            build_gestion_carguio_turno_mapper(kpis=kpis).to_component(),
            html.Div(
                className='d-flex w-100 fs-io-300 gap-2 fst-italic',
                children=[
                    html.Span(
                        children=['E • Efectivo']
                    ),
                    html.Span(
                        children=['D • Demora']
                    ),
                    html.Span(
                        children=['R • Reserva']
                    ),
                    html.Span(
                        children=['M • Mantención']
                    )
                ]
            )
        ]
    )
