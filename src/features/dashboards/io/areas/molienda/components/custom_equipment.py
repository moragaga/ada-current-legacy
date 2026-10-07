from __future__ import annotations

from dash import html

from dash.development.base_component import Component
from src.shared.ui.theme import resolve_color_class


def build_custom_equipment(
    *,
    label: str,
    state: str | Component | None,
    power: str | Component | None,
    power_color: str | Component | None,
    equipment: str,
    full_space: bool = True,
) -> Component:
    full_space_class_name = 'w-100' if full_space else 'w-50'
    return html.Div(
        className=f'd-flex flex-column align-items-center fs-io-bc-100 {full_space_class_name}',
        children=[
            html.P(
                className='fw-bold',
                children=[label]
            ),
            _safe_image(value=state, equipment=equipment),
            html.Span(
                className='d-flex',
                children=[
                    html.P(
                        className=f'{resolve_color_class(value=power_color)} fw-bold',
                        children=[power]
                    ),
                    html.P(
                        className='',
                        children=['kW']
                    )
                ]
            )
        ]
    )

def _safe_image(value: str | None | Component, equipment: str) -> Component:
    if value is None:
        return html.Img(src='/assets/img/icons/empty_data.svg')

    if not isinstance(value, str):
        return value


    return html.Img(
        className=f'img-fluid {equipment.replace('_', '-')}-img',
        src='assets/img/industrial/{0}/{1}.svg'.format(equipment, value)
    )