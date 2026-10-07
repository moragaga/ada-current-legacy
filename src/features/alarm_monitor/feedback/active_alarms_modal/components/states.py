from __future__ import annotations

from dash import html


def build_initial_state() -> html.Div:
    return html.Div(
        className='active-alarms-empty-state',
        children=[
            html.I(className='bi bi-hourglass-split'),
            html.Div('Esperando datos de alarmas.'),
        ],
    )


def build_empty_state(
    *,
    panel_kind: str,
    empty_by_filter: bool,
) -> html.Div:
    if empty_by_filter:
        message = 'No hay alarmas que coincidan con el filtro aplicado.'
    elif panel_kind == 'operator':
        message = 'No hay alarmas disponibles para gestión.'
    else:
        message = 'No hay alarmas disponibles en seguimiento.'

    return html.Div(
        className='active-alarms-empty-state',
        children=[
            html.I(className='bi bi-inbox'),
            html.Div(message),
        ],
    )
