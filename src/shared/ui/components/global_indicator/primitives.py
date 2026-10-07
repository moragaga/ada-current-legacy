from __future__ import annotations

from typing import TypeAlias

import dash_bootstrap_components as dbc
from dash import html
from dash.development.base_component import Component

from src.shared.ui.theme import resolve_color_class

DisplayValue: TypeAlias = str | int | float | Component | None


def title(
    *,
    indicator: DisplayValue,
    unit: DisplayValue,
) -> Component:
    return html.Div(
        className='d-flex align-items-center justify-content-center fs-io-hg-200 '
                  'indicator-information',
        children=[
            html.P(
                children=[indicator],
            ),
            html.I(
                className='bi bi-arrow-right-short px-1',
            ),
            html.P(
                children=[unit],
            ),
        ],
    )


def table(
    *,
    real_dia: DisplayValue,
    plan_dia: DisplayValue,
    color_dia: DisplayValue,
    real_semana: DisplayValue,
    plan_semana: DisplayValue,
    color_semana: DisplayValue,
) -> Component:
    return dbc.Table(
        className='m-0 table-borderless d-flex justify-content-center',
        children=[
            html.Tbody(
                children=[
                    _table_row(
                        item='Día',
                        real=real_dia,
                        plan=plan_dia,
                        color=color_dia,
                    ),
                    _table_row(
                        item='Semana',
                        real=real_semana,
                        plan=plan_semana,
                        color=color_semana,
                    ),
                ],
            ),
        ],
    )


def _table_row(
    *,
    item: str,
    real: DisplayValue,
    plan: DisplayValue,
    color: DisplayValue,
) -> Component:
    color_class_name = resolve_color_class(
        value=color,
        color_type='text',
    ) or ''

    style_prop = {'color': color} if isinstance(color, str) and color.startswith('#') else None

    return html.Tr(
        children=[
            html.Th(
                className='item-name',
                children=[
                    html.P(
                        className='fs-io-hg-200',
                        children=[item],
                    ),
                ],
            ),
            html.Td(
                className='real-value',
                children=[
                    html.P(
                        className=f'{color_class_name} fs-io-hg-100'.strip(),
                        style=style_prop,
                        children=[_safe_text(value=real)],
                    ),
                ],
            ),
            html.Td(
                className='value-divider',
                children=[
                    html.P(
                        className='fs-io-hg-200',
                        children=['/'],
                    ),
                ],
            ),
            html.Td(
                className='plan-value',
                children=[
                    html.P(
                        className='fs-io-hg-200',
                        children=[_safe_text(value=plan)],
                    ),
                ],
            ),
        ],
    )

def _safe_text(value: DisplayValue) -> str:
    if isinstance(value, (str, Component)):
        return value

    return html.Img(className='img-fluid invalid-value-icon-md', src='assets/img/icons/internal_error.svg')

# def last_measurement(
#     *,
#     real_turno: DisplayValue,
# ) -> Component:
#     return html.Div(
#         className=('d-flex flex-column align-items-center justify-content-center last-measurement'),
#         children=[
#             html.P(
#                 children=[real_turno],
#             ),
#             html.P(
#                 children=['Última medición'],
#             ),
#         ],
#     )
