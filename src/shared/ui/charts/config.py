from __future__ import annotations

from typing import Any

GRAPH_CONFIGURATION_STATIC: dict[str, Any] = {
    'displayModeBar': False,
    'responsive': True,
    'staticPlot': True,
    'scrollZoom': False,
    'doubleClick': False,
    'displaylogo': False,
    'modeBarButtonsToRemove': [
        'zoom2d',
        'pan2d',
        'select2d',
        'lasso2d',
        'zoomIn2d',
        'zoomOut2d',
        'autoScale2d',
        'resetScale2d',
    ],
}

GRAPH_BASIC_LAYOUT: dict[str, Any] = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'margin': {
        'l': 0,
        'r': 0,
        't': 10,
        'b': 15,
    },
    'font': {
        'family': 'Inter, Roboto, sans-serif, Arial',
        'color': '#5B5C64',
    },
    'showlegend': False,
}

GRAPH_BASIC_GRID: dict[str, Any] = {
    'showgrid': False,
    'zeroline': False,
}
