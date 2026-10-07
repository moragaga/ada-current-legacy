from __future__ import annotations

from typing import TypeAlias

from dash import dcc, html
from dash.development.base_component import Component

from src.shared.ui.theme import resolve_color_class

from .config import GaugeVariant
from .figures import build_level_gauge_figure

DisplayValue: TypeAlias = str | Component | None
DisplayNumeric: TypeAlias = float | int | str | Component | None


def build_level_gauge_component(
    *,
    variant: GaugeVariant,
    image_name: str,
    percentage: DisplayNumeric,
    unit: str = '%',
    name: str = '',
    color: DisplayValue = None,
    state: DisplayValue = None,
) -> Component:
    figure = build_level_gauge_figure(
        variant=variant,
        value=percentage,
        assets_src=_build_asset_src(
            image_name=image_name,
            state=state,
        ),
        color=color,
    )

    graph = _build_graph(
        figure=figure,
    )

    return html.Div(
        className='d-flex flex-column aling-items-center justify-content-center px-2 position-relative',
        children=[
            _build_value_header(
                value=percentage,
                unit=unit,
                color=color,
            ),
            html.Span(
                className='d-flex justify-content-center',
                children=[
                    graph,
                ],
            ),
            html.P(
                className='text-center fs-io-bc-200 fw-bold',
                children=[name],
            ),
        ],
    )


def build_level_gauge_group_component(
    *,
    level_gauges: tuple,
    class_name: str = 'd-flex align-items-center justify-content-center w-100',
) -> Component:
    return html.Div(
        className=class_name,
        children=[level_gauge.to_component() for level_gauge in level_gauges],
    )


def _build_graph(
    *,
    figure,
) -> dcc.Graph:
    return dcc.Graph(
        className='chart vertical-bar',
        figure=figure,
        config={
            'displayModeBar': False,
            'responsive': True,
            'staticPlot': True,
        },
    )


def _build_value_header(
    *,
    value: DisplayNumeric,
    unit: str,
    color: DisplayValue,
) -> Component:
    return html.Div(
        className='d-flex justify-content-center',
        children=[
            html.P(
                className=(f'fw-bold text-center fs-io-bc-200 {resolve_color_class(value=color)}'),
                children=[value],
            ),
            html.P(
                className='text-center fs-io-bc-200',
                style={'paddingLeft': '.1rem'},
                children=[unit],
            ),
        ],
    )


def _build_asset_src(
    *,
    image_name: str,
    state: DisplayValue,
) -> str | None:
    if not isinstance(state, str):
        return None

    normalized_image_name = image_name.strip().lower()
    normalized_state = state.strip().lower()

    if not normalized_image_name or not normalized_state:
        return None

    return f'assets/img/industrial/{normalized_image_name}/{normalized_state}.svg'
