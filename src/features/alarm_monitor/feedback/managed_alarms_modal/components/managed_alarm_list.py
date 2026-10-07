from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from ..constants import ZOOM_IN_CONTENT_MAIN_BUTTON_CLASSNAME
from ..ids import (
    ManagedAlarmsModalIds,
)
from .states import (
    build_empty_state,
    build_initial_state,
)


def build_managed_alarm_panel_shell() -> dbc.Card:
    return dbc.Card(
        className='managed-alarms-panel-card',
        children=[
            dbc.CardHeader(
                className='managed-alarms-panel-header',
                children=[
                    html.Div(
                        className='managed-alarms-panel-title-wrapper',
                        children=[
                            html.I(className='bi bi-list-check managed-alarms-panel-icon'),
                            html.Div(
                                children=[
                                    html.Div(
                                        className='managed-alarms-panel-title',
                                        children=['Gestiones efectivas'],
                                    ),
                                    html.Div(
                                        className='managed-alarms-panel-subtitle',
                                        children=[
                                            'Listado de gestiones registradas en la ventana analítica.'
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className='d-flex gap-3',
                        children=[
                            html.Span(
                                id=ManagedAlarmsModalIds.ITEMS_COUNT,
                                className='managed-alarms-panel-count',
                                children=['0 gestiones'],
                            ),
                            html.I(
                                id=ManagedAlarmsModalIds.ZOOM_MAIN_CONTENT_BUTTON,
                                className=ZOOM_IN_CONTENT_MAIN_BUTTON_CLASSNAME,
                                n_clicks=0,
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className='managed-alarms-table-scroll',
                children=[
                    html.Div(
                        className='managed-alarms-table-header',
                        children=[
                            html.Div(className='managed-alarms-col-severity', children=['Sev.']),
                            html.Div(className='managed-alarms-col-alarm', children=['Alarma']),
                            html.Div(className='managed-alarms-col-turn', children=['Turno']),
                            html.Div(className='managed-alarms-col-status', children=['Estado']),
                            html.Div(
                                className='managed-alarms-col-time', children=['Gestión / Tiempo']
                            ),
                            html.Div(className='managed-alarms-col-action', children=['Detalle']),
                        ],
                    ),
                    dcc.Loading(
                        type='default',
                        delay_show=180,
                        delay_hide=350,
                        parent_className='managed-alarms-internal-loader',
                        className='loading-component-spinner',
                        children=html.Div(
                            className='managed-alarms-list-shell',
                            children=[
                                html.Div(
                                    id=ManagedAlarmsModalIds.ITEMS_LIST,
                                    className='managed-alarms-list',
                                    children=[build_initial_state()],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
            html.Div(
                className='managed-alarms-pagination',
                children=[
                    dbc.Button(
                        id=ManagedAlarmsModalIds.ITEMS_PREVIOUS_BUTTON,
                        color='light',
                        className='managed-alarms-pagination-button',
                        n_clicks=0,
                        disabled=True,
                        children=[html.I(className='bi bi-chevron-left')],
                    ),
                    html.Div(
                        id=ManagedAlarmsModalIds.ITEMS_PAGE_TEXT,
                        className='managed-alarms-pagination-text',
                        children=['Página 1 de 1'],
                    ),
                    dbc.Button(
                        id=ManagedAlarmsModalIds.ITEMS_NEXT_BUTTON,
                        color='light',
                        className='managed-alarms-pagination-button',
                        n_clicks=0,
                        disabled=True,
                        children=[html.I(className='bi bi-chevron-right')],
                    ),
                ],
            ),
        ],
    )


def build_managed_alarm_list_children(
    *,
    items: list[dict[str, Any]],
    page_size: int,
    has_snapshot: bool,
    empty_by_filter: bool,
) -> list[Any]:
    if not has_snapshot:
        return [build_initial_state()]

    if not items:
        return [build_empty_state(empty_by_filter=empty_by_filter)]

    rows = [_build_managed_alarm_row(item=item) for item in items]

    filler_count = max(0, page_size - len(items))
    rows.extend(_build_filler_row(index=index) for index in range(filler_count))

    return rows


def _build_managed_alarm_row(
    *,
    item: dict[str, Any],
) -> html.Details:
    severity_code = item.get('severity_code') or 'unknown'
    severity_label = item.get('severity_label') or 'Sin severidad'

    row_class_name = f'managed-alarm-row managed-alarm-row-{severity_code}'

    if item.get('is_inactive_management'):
        row_class_name = f'{row_class_name} managed-alarm-row-inactive'

    return html.Details(
        className=row_class_name,
        children=[
            html.Summary(
                className='managed-alarm-row-summary',
                children=[
                    html.Div(
                        className='managed-alarms-col-severity',
                        children=[
                            html.Span(
                                severity_label,
                                className=(
                                    f'managed-alarm-severity managed-alarm-severity-{severity_code}'
                                ),
                            ),
                        ],
                    ),
                    html.Div(
                        className='managed-alarms-col-alarm',
                        children=[
                            html.Div(
                                item.get('alarm_display_name')
                                or item.get('title')
                                or 'Alarma sin título',
                                className='managed-alarm-title',
                            ),
                            html.Div(
                                item.get('cause') or 'Sin causa informada.',
                                className='managed-alarm-cause',
                            ),
                        ],
                    ),
                    html.Div(
                        className='managed-alarms-col-turn',
                        children=[
                            _build_turn_badge(item=item),
                        ],
                    ),
                    html.Div(
                        className='managed-alarms-col-status',
                        children=[
                            html.Span(
                                item.get('status_label') or 'Gestionada',
                                className='managed-alarm-state-chip',
                            ),
                        ],
                    ),
                    html.Div(
                        className='managed-alarms-col-time',
                        children=[
                            html.Div(
                                item.get('requested_display') or 'Sin fecha',
                                className='managed-alarm-requested',
                            ),
                            html.Div(
                                item.get('time_to_management_display') or '--:--:--',
                                className='managed-alarm-duration',
                            ),
                        ],
                    ),
                    html.Div(
                        className='managed-alarms-col-action managed-alarm-chevron-wrapper',
                        children=[
                            html.I(className='bi bi-chevron-down managed-alarm-chevron'),
                        ],
                    ),
                ],
            ),
            _build_managed_alarm_detail(item=item),
        ],
    )


def _build_turn_badge(
    *,
    item: dict[str, Any],
) -> html.Div:
    label = item.get('turn_scope_label') or 'Sin turno'
    group = item.get('turn_group_label') or ''

    return html.Div(
        className='managed-alarm-turn',
        children=[
            html.Span(label),
            html.Span(group, className='managed-alarm-turn-group') if group else None,
        ],
    )


def _build_managed_alarm_detail(
    *,
    item: dict[str, Any],
) -> html.Div:
    return html.Div(
        className=f'managed-alarm-detail managed-alarm-detail-{item.get("severity_code")}',
        children=[
            html.Div(
                className='managed-alarm-detail-title',
                children=[
                    html.I(className='bi bi-file-earmark-text'),
                    html.Span('Detalle de la gestión'),
                ],
            ),
            html.Div(
                className='managed-alarm-detail-grid',
                children=[
                    _build_detail_block('Alarma', item.get('alarm_display_name')),
                    _build_detail_block('Turno', item.get('turn_scope_label')),
                    _build_detail_block('Grupo', item.get('turn_group_label')),
                    _build_detail_block('Causa probable', item.get('cause')),
                    _build_detail_block('Tipo de gestión', item.get('management_status_label')),
                    _build_detail_block('Estado alarma', item.get('alarm_status_label')),
                    _build_detail_block('Operador', item.get('requested_by_name')),
                    _build_detail_block('Correo', item.get('requested_by_email')),
                    _build_detail_block(
                        'Inicio ocurrencia', item.get('occurrence_started_display')
                    ),
                    _build_detail_block('Fecha gestión', item.get('requested_display')),
                    _build_detail_block(
                        'Tiempo hasta gestión', item.get('time_to_management_display')
                    ),
                    _build_detail_block('Vencimiento', item.get('expires_display')),
                    _build_detail_block('Mensaje', item.get('message_display')),
                ],
            ),
        ],
    )


def _build_detail_block(
    label: str,
    value: str | None,
) -> html.Div:
    return html.Div(
        className='managed-alarm-detail-block',
        children=[
            html.Div(label, className='managed-alarm-detail-label'),
            html.Div(value or 'Sin información', className='managed-alarm-detail-value'),
        ],
    )


def _build_filler_row(
    *,
    index: int,
) -> html.Div:
    return html.Div(
        key=f'filler-{index}',
        className='managed-alarm-row managed-alarm-row-filler',
    )
