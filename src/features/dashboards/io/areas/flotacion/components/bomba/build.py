from __future__ import annotations

from typing import TYPE_CHECKING

from dash.development.base_component import Component
from dash import html

if TYPE_CHECKING:
    from .models import BombaData, BombaGroupData

def build_bomba_component(*, model: BombaData) -> Component:
    return html.Div(
        className='d-flex flex-column align-items-center fs-io-bc-300 w-100',
        children=[
            _safe_image(value=model.bomba_state),
            html.P(
                className='fw-bold',
                children=[model.label]
            ),
        ]
    )

def build_bomba_group_component(*, models: BombaGroupData) -> Component:
    content = []
    for model in models.bombas_group:
        for position, component in model.items():
            content.append(
                html.Div(
                    className=f'd-flex {'flex-column' if position == 'vertical' else 'flex-row'} gap-1',
                    children=[data.to_component() for data in component],
                )
            )

    return html.Div(
        className='d-flex justify-content-evenly',
        style={'gap': '.1rem'},
        children=content
    )

def _safe_image(value: str | None | Component) -> Component:
    if value is None:
        return html.Img(src='/assets/img/icons/empty_data.svg')

    if not isinstance(value, str):
        return value

    return html.Img(
        className='img-fluid bomba-img',
        src='assets/img/industrial/bomba/{0}.svg'.format(value)
    )