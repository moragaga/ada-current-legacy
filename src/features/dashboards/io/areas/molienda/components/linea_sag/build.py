from __future__ import annotations

from dash import html
from dash.development.base_component import Component
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .model import LineaSagData, LineaSagGroupData


def build_linea_sag_component(*, model: LineaSagData) -> Component:
    return html.Div(
        className='linea-sag-wrapper',
        children=[
            _title(linea_number=model.linea_number),
            html.Div(
                className='d-flex flex-column align-items-center gap-1',
                children=[
                    model.sag.to_component(),
                    html.Div(
                        className='d-flex gap-1 w-100',
                        children=[
                            html.Div(
                                style={'width': '80%'},
                                children=model.metrics.to_components()
                            ),
                            model.molinos_bolas.to_component()
                        ]
                    )
                ]
            )
        ]
    )

def build_lineas_sag_component(*, models: LineaSagGroupData) -> Component:
    return html.Div(
        className='lineas-sag-container d-flex flex-column gap-1',
        children=[
            build_linea_sag_component(model=model) for model in models.lineas_sag
        ]
    )


def _title(linea_number: str) -> Component:
    return html.Div(
        className='display-section-title fs-io-bc-100',
        children=[html.P(children=[f'Línea {linea_number}'])],
    )