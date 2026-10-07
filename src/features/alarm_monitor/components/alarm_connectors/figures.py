from __future__ import annotations

import plotly.graph_objects as go
from dash import dcc


def build_alarm_connectors_graph(
    *,
    occupied_slot_indexes: list[int],
    total_slots: int = 6,
) -> dcc.Graph:
    fig = go.Figure()

    fig.update_layout(
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        autosize=True,
        xaxis={
            'range': [-0.03, 1.03],
            'visible': False,
            'fixedrange': True,
        },
        yaxis={
            'range': [-0.20, 1.10],
            'visible': False,
            'fixedrange': True,
        },
        shapes=[],
    )

    if not occupied_slot_indexes:
        return _build_graph(fig)

    occupied_slot_indexes = sorted(set(occupied_slot_indexes))
    slot_centers = _build_slot_centers(total_slots=total_slots)
    selected_x = [slot_centers[index] for index in occupied_slot_indexes if index in slot_centers]

    if not selected_x:
        return _build_graph(fig)

    root_x = 0.5
    root_bottom_y = 0.02
    # trunk_y = 0.28
    trunk_y = 0.18
    # card_top_y = 0.98
    card_top_y = 0.6

    rail_start_x = min([root_x, *selected_x])
    rail_end_x = max([root_x, *selected_x])

    line_style = {
        'color': '#E1E1E1',
        'width': 1.5,
    }

    shapes: list[dict] = [
        {
            'type': 'line',
            'x0': root_x,
            'y0': root_bottom_y,
            'x1': root_x,
            'y1': trunk_y,
            'line': line_style,
        },
        {
            'type': 'line',
            'x0': rail_start_x,
            'y0': trunk_y,
            'x1': rail_end_x,
            'y1': trunk_y,
            'line': line_style,
        },
    ]

    for x in selected_x:
        shapes.append(
            {
                'type': 'line',
                'x0': x,
                'y0': trunk_y,
                'x1': x,
                'y1': card_top_y,
                'line': line_style,
            }
        )

    fig.update_layout(shapes=shapes)

    fig.add_trace(
        go.Scatter(
            x=[root_x],
            y=[trunk_y],
            mode='markers',
            marker={
                'size': 10,
                'color': '#E1E1E1',
            },
            hoverinfo='skip',
            showlegend=False,
            cliponaxis=False,
        )
    )

    return _build_graph(fig)


def _build_slot_centers(*, total_slots: int) -> dict[int, float]:
    if total_slots <= 0:
        return {}

    step = 1 / total_slots
    return {index: (index * step) + (step / 2) for index in range(total_slots)}


def _build_graph(fig: go.Figure) -> dcc.Graph:
    return dcc.Graph(
        className='graph alarm-connectors-graph',
        figure=fig,
        config={
            'displayModeBar': False,
            'responsive': True,
            'staticPlot': True,
        },
    )
