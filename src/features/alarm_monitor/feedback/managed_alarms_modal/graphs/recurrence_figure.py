from __future__ import annotations

from typing import Any

import plotly.graph_objects as go

from src.shared.time.timestamps import parse_utc_datetime, utc_to_local

from ..constants import (
    DEFAULT_RECURRENCE_MIN_DURATION,
)
from ..services.managed_alarm_modal_snapshot_mapper import (
    get_recurrence_payload_for_turn_scope,
    get_time_range_for_turn_scope,
)

GRAPH_CONFIGURATION: dict[str, Any] = {
    'displayModeBar': False,
    'responsive': True,
    'staticPlot': False,
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
        'l': 42,
        'r': 12,
        't': 30,
        'b': 42,
    },
    'font': {
        'family': 'Inter, Roboto, sans-serif, Arial',
        'color': '#5B5C64',
    },
    'hoverlabel': {
        'font_family': 'Inter, Roboto, sans-serif, Arial',
    },
    'hovermode': 'x unified',
    'clickmode': 'none',
    'dragmode': False,
    'xaxis': {
        'gridwidth': 0,
        'linewidth': 1,
        'automargin': True,
        'tickmode': 'auto',
        'tickformat': '%H:%M',
        'tickangle': 0,
    },
    'legend': {
        'orientation': 'h',
        'yanchor': 'bottom',
        'y': 1.02,
        'xanchor': 'center',
        'x': 0.5,
    },
    'yaxis': {
        'title': 'Cantidad',
        'tickformat': '.0f',
        'gridwidth': 0,
        'linewidth': 1,
        'automargin': True,
        'tickmode': 'auto',
    },
}

GRIDS_CONFIGURATION: dict[str, Any] = {
    'showgrid': False,
    'zeroline': False,
    'linecolor': '#5B5E65',
}


def build_recurrence_figure(
    *,
    snapshot: dict[str, Any] | None,
    min_duration: str | None,
    turn_scope_filter: str | None,
) -> go.Figure:
    if not snapshot:
        return build_empty_recurrence_figure(
            message='Sin snapshot analítico.',
        )

    recurrence = get_recurrence_payload_for_turn_scope(
        snapshot=snapshot,
        turn_scope_filter=turn_scope_filter,
    )

    if not recurrence:
        return build_empty_recurrence_figure(
            message='Sin tendencia para el turno seleccionado.',
        )

    by_duration = _as_dict(recurrence.get('by_min_activation_duration'))

    selected_key = _safe_str(min_duration) or DEFAULT_RECURRENCE_MIN_DURATION
    selected_data = _as_dict(by_duration.get(selected_key))

    buckets = _as_list(selected_data.get('buckets'))

    if not buckets:
        return build_empty_recurrence_figure(
            message='Sin datos de recurrencia para mostrar.',
        )

    x_values = _time_xaxis_builder(buckets=buckets)
    activations = [int(bucket.get('activations') or 0) for bucket in buckets]
    managements = [int(bucket.get('managements') or 0) for bucket in buckets]
    reactivations = [int(bucket.get('reactivations') or 0) for bucket in buckets]

    figure = go.Figure()
    try:
        figure.add_trace(
            go.Bar(
                name='Activaciones',
                x=x_values,
                y=activations,
            )
        )

        figure.add_trace(
            go.Scatter(
                name='Gestiones',
                x=x_values,
                y=managements,
                mode='lines+markers',
            )
        )

        figure.add_trace(
            go.Scatter(
                name='Reactivaciones',
                x=x_values,
                y=reactivations,
                mode='lines+markers',
            )
        )
    except Exception as e:
        print('[ERROR] datetime wrong to build recurrence figure', str(e))
        return build_empty_recurrence_figure(
            message='Sin snapshot analítico.',
        )

    figure.update_layout(
        **GRAPH_BASIC_LAYOUT,
    )

    start_range, end_range = get_time_range_for_turn_scope(
        snapshot=snapshot,
        turn_scope_filter=turn_scope_filter,
    )

    range_values = {}
    if start_range is not None and end_range is not None:
        range_values = {
            'range': [start_range, end_range],
            'autorange': False,
            'rangeslider': {'visible': False},
            'rangebreaks': [
                {
                    'values': [
                        '1969-12-31',
                        '1970-01-01',
                    ]
                }
            ],
        }

    figure.update_xaxes(
        {
            'fixedrange': True,
            'type': 'date',
            'nticks': 8,
            'hoverformat': '%Y-%m-%d %H:%M',
        },
        **range_values,
        **GRIDS_CONFIGURATION,
    )
    figure.update_yaxes(**GRIDS_CONFIGURATION)

    return figure


def build_empty_recurrence_figure(
    *,
    message: str,
) -> go.Figure:
    figure = go.Figure()

    figure.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref='paper',
        yref='paper',
        showarrow=False,
    )

    figure.update_layout(
        margin={
            'l': 42,
            'r': 12,
            't': 30,
            'b': 42,
        },
        xaxis={
            'visible': False,
        },
        yaxis={
            'visible': False,
        },
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff',
        font={
            'size': 10,
        },
    )

    return figure


def _safe_str(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    return {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    return []


def _time_xaxis_builder(buckets: list) -> list:
    buckets_utc = [parse_utc_datetime(bucket.get('bucket_start')) for bucket in buckets]
    return [utc_to_local(bucket) for bucket in buckets_utc]
