from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from ..constants import (
    DEFAULT_CRITICITY_FILTER,
    DEFAULT_RECURRENCE_MIN_DURATION,
    DEFAULT_SORT_ORDER,
    DEFAULT_STATUS_FILTER,
    DEFAULT_TURN_SCOPE_FILTER,
    RECURRENCE_MIN_DURATION_OPTIONS,
    TURN_SCOPE_ALL,
)
from ..ids import (
    ManagedAlarmsModalIds,
)


def build_managed_alarms_modal_toolbar() -> html.Div:
    return html.Div(
        className='managed-alarms-modal-toolbar',
        children=[
            _build_search_control(),
            _build_turn_scope_filter(),
            _build_criticity_filter(),
            _build_status_filter(),
            _build_sort_control(),
            _build_duration_filter(),
        ],
    )


def _build_search_control() -> html.Div:
    return html.Div(
        className='managed-alarms-control',
        children=[
            html.Label(
                htmlFor=ManagedAlarmsModalIds.SEARCH_INPUT,
                className='managed-alarms-control-label',
                children=['Buscar alarma'],
            ),
            dbc.InputGroup(
                className='managed-alarms-modal-search',
                children=[
                    dbc.InputGroupText(html.I(className='bi bi-search')),
                    dbc.Input(
                        id=ManagedAlarmsModalIds.SEARCH_INPUT,
                        type='text',
                        size='sm',
                        placeholder='Buscar por alarma, causa o mensaje...',
                        debounce=False,
                    ),
                ],
            ),
        ],
    )


def _build_turn_scope_filter() -> html.Div:
    return html.Div(
        className='managed-alarms-control',
        children=[
            html.Label(
                htmlFor=ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE,
                className='managed-alarms-control-label',
                children=['Turno'],
            ),
            dbc.Select(
                id=ManagedAlarmsModalIds.FILTER_SELECT_TURN_SCOPE,
                className='managed-alarms-modal-filter',
                placeholder='Filtrar por turno',
                size='sm',
                value=DEFAULT_TURN_SCOPE_FILTER,
                options=[
                    {
                        'label': 'Actual',
                        'value': 'current',
                    },
                    {
                        'label': 'Anterior',
                        'value': 'previous',
                    },
                    {
                        'label': 'Ambos',
                        'value': TURN_SCOPE_ALL,
                    },
                ],
            ),
        ],
    )


def _build_criticity_filter() -> html.Div:
    return html.Div(
        className='managed-alarms-control',
        children=[
            html.Label(
                htmlFor=ManagedAlarmsModalIds.FILTER_SELECT_CRITICITY,
                className='managed-alarms-control-label',
                children=['Criticidad'],
            ),
            dbc.Select(
                id=ManagedAlarmsModalIds.FILTER_SELECT_CRITICITY,
                className='managed-alarms-modal-filter',
                placeholder='Filtrar por criticidad',
                size='sm',
                value=DEFAULT_CRITICITY_FILTER,
                options=[
                    {
                        'label': 'Todas',
                        'value': 'all',
                    },
                    {
                        'label': 'Impacto',
                        'value': 'impacto',
                    },
                    {
                        'label': 'Riesgo',
                        'value': 'riesgo',
                    },
                ],
            ),
        ],
    )


def _build_status_filter() -> html.Div:
    return html.Div(
        className='managed-alarms-control',
        children=[
            html.Label(
                htmlFor=ManagedAlarmsModalIds.FILTER_SELECT_STATUS,
                className='managed-alarms-control-label',
                children=['Estado'],
            ),
            dbc.Select(
                id=ManagedAlarmsModalIds.FILTER_SELECT_STATUS,
                className='managed-alarms-modal-filter',
                placeholder='Filtrar por estado',
                size='sm',
                value=DEFAULT_STATUS_FILTER,
                options=[
                    {
                        'label': 'Todas',
                        'value': 'all',
                    },
                    {
                        'label': 'Gestionadas',
                        'value': 'managed',
                    },
                    {
                        'label': 'Desactivadas',
                        'value': 'inactive',
                    },
                    {
                        'label': 'Siguen activas',
                        'value': 'still_active',
                    },
                ],
            ),
        ],
    )


def _build_sort_control() -> html.Div:
    return html.Div(
        className='managed-alarms-control',
        children=[
            html.Label(
                htmlFor=ManagedAlarmsModalIds.SORT_SELECT_TIME,
                className='managed-alarms-control-label',
                children=['Ordenar por'],
            ),
            dbc.Select(
                id=ManagedAlarmsModalIds.SORT_SELECT_TIME,
                className='managed-alarms-modal-sort',
                value=DEFAULT_SORT_ORDER,
                placeholder='Ordenar por',
                size='sm',
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


def _build_duration_filter() -> html.Div:
    return html.Div(
        className='managed-alarms-control',
        children=[
            html.Label(
                htmlFor=ManagedAlarmsModalIds.RECURRENCE_MIN_DURATION_SELECT,
                className='managed-alarms-control-label',
                children=['Duración mínima'],
            ),
            dbc.Select(
                id=ManagedAlarmsModalIds.RECURRENCE_MIN_DURATION_SELECT,
                className='managed-alarms-modal-filter',
                placeholder='Filtrar por tiempo activo',
                size='sm',
                value=DEFAULT_RECURRENCE_MIN_DURATION,
                options=RECURRENCE_MIN_DURATION_OPTIONS,
            ),
        ],
    )
