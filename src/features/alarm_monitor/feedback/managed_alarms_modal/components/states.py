from __future__ import annotations

from dash import html


def build_initial_state() -> html.Div:
    return html.Div(
        className='managed-alarms-empty-state',
        children=[
            html.I(className='bi bi-hourglass-split'),
            html.Div(children=['Esperando datos de gestiones.']),
        ],
    )


def build_initial_summary_state() -> html.Div:
    return html.Div(
        className='managed-alarms-empty-state managed-alarms-empty-state-summary',
        children=[
            html.I(className='bi bi-hourglass-split'),
            html.Div(children=['Esperando datos analíticos.']),
        ],
    )


def build_empty_state(
    *,
    empty_by_filter: bool,
) -> html.Div:
    message = (
        'No hay gestiones que coincidan con el filtro aplicado.'
        if empty_by_filter
        else 'No hay gestiones registradas en la ventana analítica.'
    )

    return html.Div(
        className='managed-alarms-empty-state',
        children=[
            html.I(className='bi bi-inbox'),
            html.Div(message),
        ],
    )
