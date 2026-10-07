from __future__ import annotations

from typing import TYPE_CHECKING

from dash.development.base_component import Component
from dash import html
from src.shared.ui.theme import resolve_color_class

if TYPE_CHECKING:
    from .models import VertimilData, VertimilGroupData

def build_vertimil_component(*, model: VertimilData) -> Component:
    return html.Div(
        className='d-flex flex-column align-items-center fs-io-bc-300 w-100',
        children=[
            _safe_image(value=model.vertimil_state),
            html.P(
                className='fw-bold',
                children=[model.label]
            ),
            html.Span(
                className='d-flex',
                children=[
                    html.P(
                        className=f'{resolve_color_class(value=model.vertimil_color)} fw-bold',
                        children=[model.vertimil_value]
                    ),
                    html.P(
                        className='',
                        children=[model.vertimil_unit]
                    )
                ]
            )
        ]
    )

def build_vertimil_group_component(*, models: VertimilGroupData) -> Component:
    return html.Div(
        className='d-flex justify-content-evenly',
        children=[vertimil.to_component() for vertimil in models.vertimils],
    )

def _safe_image(value: str | None | Component) -> Component:
    if value is None:
        return html.Img(src='/assets/img/icons/empty_data.svg')

    if not isinstance(value, str):
        return value

    return html.Img(
        className='img-fluid vertimil-img',
        src='assets/img/industrial/vertimil/{0}.svg'.format(value)
    )