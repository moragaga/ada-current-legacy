from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objs as go
from dash import dcc
from dash.development.base_component import Component

if TYPE_CHECKING:
    from .models import StockpileMinaData

from ..config import GRAPH_BASIC_GRID, GRAPH_BASIC_LAYOUT, GRAPH_CONFIGURATION_STATIC
from ..support import resolve_color, resolve_value


def build_stockpile_mina_chart(
    *,
    model: StockpileMinaData,
) -> Component:
    fig = go.Figure()

    y_values, inside_texts, outside_texts, colors = _prepare_data(model=model)
    _build_bars(
        fig=fig,
        y_values=y_values,
        inside_texts=inside_texts,
        outside_texts=outside_texts,
        colors=colors,
    )

    _configure_layout(fig=fig)
    _configure_xaxis(fig=fig)
    _configure_yaxis(fig=fig)

    return dcc.Graph(
        className='stockpile-mina-chart',
        figure=fig,
        config=GRAPH_CONFIGURATION_STATIC,
    )


def _build_bars(
    *,
    fig: go.Figure,
    y_values: list[int],
    inside_texts: list[str],
    outside_texts: list[str],
    colors: list[str],
) -> None:
    fig.add_traces(
        [
            go.Bar(
                name='',
                y=y_values,
                marker={
                    'color': colors,
                    'line': {
                        'width': 0,
                    },
                },
                width=[0.5] * len(y_values),
                text=inside_texts,
                textposition='inside',
                insidetextanchor='middle',
                textfont={'color': '#FFFFFF'},
                textangle=0,
                cliponaxis=False,
                hoverinfo='skip',
            ),
            go.Bar(
                name='',
                y=y_values,
                marker={
                    'color': 'rgba(0,0,0,0)',
                    'line': {
                        'width': 0,
                    },
                },
                width=[0.5] * len(y_values),
                text=outside_texts,
                textposition='outside',
                insidetextanchor='middle',
                textfont={'color': '#000000'},
                textangle=0,
                cliponaxis=False,
                hoverinfo='skip',
            ),
        ]
    )


def _prepare_data(
    *,
    model: StockpileMinaData,
) -> tuple[list[int], list[str], list[str], list[str]]:
    y_values = []
    inside_texts = []
    outside_texts = []
    colors = []
    for pile in model.piles:
        is_valid, percentage = resolve_value(value=pile.percentage_value, default=100)
        _, meters = resolve_value(value=pile.meters_value, default=0)
        color = resolve_color(color=pile.percentage_value, opacity_value=not is_valid)

        y_values.append(meters)
        inside_texts.append(f'{percentage}%')
        outside_texts.append(f'{meters}m')
        colors.append(color)

    return y_values, inside_texts, outside_texts, colors


def _configure_layout(
    *,
    fig: go.Figure,
) -> None:
    layout = GRAPH_BASIC_LAYOUT.copy()
    layout['margin'] = {'l': 0, 'r': 0, 't': 20, 'b': 0}

    fig.update_layout(
        barmode='overlay',
        bargap=0,
        **layout,
    )


def _configure_xaxis(
    *,
    fig: go.Figure,
) -> None:
    fig.update_xaxes(
        tickangle=0,
        showticklabels=False,
        showline=False,
        **GRAPH_BASIC_GRID,
    )


def _configure_yaxis(
    *,
    fig: go.Figure,
) -> None:
    fig.update_yaxes(visible=False, range=[0, 28], **GRAPH_BASIC_GRID)
