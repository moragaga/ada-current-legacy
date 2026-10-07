from __future__ import annotations

from typing import TYPE_CHECKING

import plotly.graph_objects as go
from dash import dcc
from dash.development.base_component import Component

if TYPE_CHECKING:
    from .models import FeedersData

from ..config import GRAPH_BASIC_GRID, GRAPH_BASIC_LAYOUT, GRAPH_CONFIGURATION_STATIC
from ..support import resolve_color, resolve_value


def build_feeders_chart(
    *,
    model: FeedersData,
) -> Component:
    fig = go.Figure()

    y_values, y_difference_values, x_labels, colors = _prepare_data(model=model)
    _build_bars(
        fig=fig,
        x_labels=x_labels,
        y_values=y_values,
        y_difference_values=y_difference_values,
        colors=colors,
    )

    _configure_layout(fig=fig)
    _configure_xaxis(fig=fig, labels=x_labels)
    _configure_yaxis(fig=fig)
    _add_layout_image(fig=fig)

    return dcc.Graph(
        className='feeders-chart',
        figure=fig,
        config=GRAPH_CONFIGURATION_STATIC,
    )


def _build_bars(
    *,
    fig: go.Figure,
    x_labels: list[str],
    y_values: list[int],
    y_difference_values: list[int],
    colors: list[str],
) -> None:
    fig.add_traces(
        [
            go.Bar(
                x=x_labels,
                y=y_values,
                name='',
                marker={
                    'color': colors,
                    'line': {
                        'width': 0,
                    },
                },
                width=0.5,
                hoverinfo='skip',
            ),
            go.Bar(
                x=x_labels,
                y=y_difference_values,
                name='',
                marker={
                    'color': '#FFFFFF',
                    'line': {
                        'width': 0,
                    },
                },
                width=0.5,
                hoverinfo='skip',
            ),
        ]
    )


def _prepare_data(
    *,
    model: FeedersData,
) -> tuple[list[int], list[int], list[str], list[str]]:
    y_values = []
    y_difference_values = []
    x_labels = []
    colors = []
    for feeder in model.feeders:
        is_valid, value = resolve_value(value=feeder.value, default=100)
        color = resolve_color(color=feeder.color, opacity_value=not is_valid)

        y_values.append(value)
        y_difference_values.append(100 - value)
        x_labels.append(feeder.label)
        colors.append(color)

    return y_values, y_difference_values, x_labels, colors


def _configure_layout(
    *,
    fig: go.Figure,
) -> None:
    fig.update_layout(bargap=0.7, barmode='stack', **GRAPH_BASIC_LAYOUT)


def _add_layout_image(*, fig: go.Figure) -> None:
    fig.add_layout_image(
        source='assets/img/icons/extra/gradient_rectangle.svg',
        x=0,
        y=0,
        sizex=1,
        sizey=1,
        opacity=1,
        yanchor='bottom',
        sizing='stretch',
        layer='below',
    )


def _configure_xaxis(
    *,
    fig: go.Figure,
    labels: list[str],
) -> None:
    fig.update_xaxes(
        type='category',
        tickmode='array',
        tickvals=labels,
        ticktext=labels,
        nticks=len(labels),
        showline=False,
        **GRAPH_BASIC_GRID,
    )


def _configure_yaxis(
    *,
    fig: go.Figure,
) -> None:
    fig.update_yaxes(visible=False, range=[0, 105], **GRAPH_BASIC_GRID)
