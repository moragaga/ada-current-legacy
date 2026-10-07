from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from ..ids import ActiveAlarmsModalIds


def build_active_alarms_modal_toolbar() -> html.Div:
    return html.Div(
        className='active-alarms-modal-toolbar',
        children=[
            _build_search_control(),
            _build_sort_control(),
            _build_criticity_filter(),
        ],
    )


def _build_search_control() -> html.Div:
    return html.Div(
        className='active-alarms-control',
        children=[
            html.Label(
                htmlFor=ActiveAlarmsModalIds.SEARCH_INPUT,
                className='active-alarms-control-label',
                children=['Buscar alarma'],
            ),
            dbc.InputGroup(
                className='active-alarms-modal-search',
                children=[
                    dbc.InputGroupText(
                        html.I(className='bi bi-search'),
                    ),
                    dbc.Input(
                        id=ActiveAlarmsModalIds.SEARCH_INPUT,
                        type='text',
                        size='sm',
                        placeholder='Buscar alarma por título...',
                        debounce=False,
                    ),
                ],
            ),
        ],
    )


def _build_sort_control() -> html.Div:
    return html.Div(
        className='active-alarms-control',
        children=[
            html.Label(
                htmlFor=ActiveAlarmsModalIds.SORT_SELECT_TIME,
                className='active-alarms-control-label',
                children=['Ordenar por'],
            ),
            dbc.Select(
                id=ActiveAlarmsModalIds.SORT_SELECT_TIME,
                className='active-alarms-modal-sort',
                value='recent',
                size='sm',
                placeholder='Ordenar por',
                options=[
                    {
                        'label': 'Más recientes',
                        'value': 'recent',
                    },
                    {
                        'label': 'Más antiguas',
                        'value': 'oldest',
                    },
                ],
            ),
        ],
    )


def _build_criticity_filter() -> html.Div:
    return html.Div(
        className='active-alarms-control',
        children=[
            html.Label(
                htmlFor=ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY,
                className='active-alarms-control-label',
                children=['Filtrar por criticidad'],
            ),
            dbc.Select(
                id=ActiveAlarmsModalIds.FILTER_SELECT_CRITICITY,
                className='active-alarms-modal-filter',
                size='sm',
                value='all',
                placeholder='Filtrar por criticidad',
                options=[
                    {
                        'label': 'Todas',
                        'value': 'all',
                    },
                    {
                        'label': 'Riesgo',
                        'value': 'riesgo',
                    },
                    {
                        'label': 'Impacto',
                        'value': 'impacto',
                    },
                ],
            ),
        ],
    )
