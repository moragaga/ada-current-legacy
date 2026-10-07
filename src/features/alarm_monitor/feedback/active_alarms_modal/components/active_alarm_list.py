from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html

from ..ids import ActiveAlarmsModalIds
from .states import build_empty_state, build_initial_state


def build_active_alarm_panel_shell() -> list[dbc.Card]:
    return html.Div(
        className='active-alarms-modal-content-grid',
        children=[
            _build_alarm_panel_shell(
                title='Alarmas activas',
                subtitle='Alarmas disponibles para gestión',
                icon_class_name='bi bi-person',
                count_id=ActiveAlarmsModalIds.OPERATOR_COUNT,
                list_id=ActiveAlarmsModalIds.OPERATOR_LIST,
                previous_button_id=ActiveAlarmsModalIds.OPERATOR_PREVIOUS_BUTTON,
                next_button_id=ActiveAlarmsModalIds.OPERATOR_NEXT_BUTTON,
                page_text_id=ActiveAlarmsModalIds.OPERATOR_PAGE_TEXT,
            ),
            _build_alarm_panel_shell(
                title='Alarmas gestionadas activas',
                subtitle='Seguimiento operativo de alarmas',
                icon_class_name='bi bi-crosshair',
                count_id=ActiveAlarmsModalIds.TRACKING_COUNT,
                list_id=ActiveAlarmsModalIds.TRACKING_LIST,
                previous_button_id=ActiveAlarmsModalIds.TRACKING_PREVIOUS_BUTTON,
                next_button_id=ActiveAlarmsModalIds.TRACKING_NEXT_BUTTON,
                page_text_id=ActiveAlarmsModalIds.TRACKING_PAGE_TEXT,
            ),
        ],
    )


def _build_alarm_panel_shell(
    *,
    title: str,
    subtitle: str,
    icon_class_name: str,
    count_id: str,
    list_id: str,
    previous_button_id: str,
    next_button_id: str,
    page_text_id: str,
) -> dbc.Card:
    return dbc.Card(
        className='active-alarms-panel-card',
        children=[
            dbc.CardHeader(
                className='active-alarms-panel-header',
                children=[
                    html.Div(
                        className='active-alarms-panel-title-wrapper',
                        children=[
                            html.I(className=f'{icon_class_name} active-alarms-panel-icon'),
                            html.Div(
                                children=[
                                    html.Div(
                                        children=[title],
                                        className='active-alarms-panel-title',
                                    ),
                                    html.Div(
                                        className='active-alarms-panel-subtitle',
                                        children=[subtitle],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Span(
                        id=count_id,
                        className='active-alarms-panel-count',
                        children=['0 activas'],
                    ),
                ],
            ),
            html.Div(
                className='active-alarms-table-scroll',
                children=[
                    html.Div(
                        className='active-alarms-table-header',
                        children=[
                            html.Div(className='active-alarms-col-severity', children=['Sev.']),
                            html.Div(
                                className='active-alarms-col-alarm',
                                children=['Alarma'],
                            ),
                            html.Div(
                                className='active-alarms-col-time', children=['Desde / Duración']
                            ),
                            html.Div(
                                className='active-alarms-col-action',
                                children=['Detalle'],
                            ),
                        ],
                    ),
                    dcc.Loading(
                        type='default',
                        delay_show=180,
                        delay_hide=350,
                        className='loading-component-spinner',
                        parent_className='active-alarms-internal-loader',
                        children=html.Div(
                            className='active-alarms-list-shell',
                            children=[
                                html.Div(
                                    id=list_id,
                                    className='active-alarms-list',
                                    children=[
                                        build_initial_state(),
                                    ],
                                ),
                            ],
                        ),
                    ),
                ],
            ),
            html.Div(
                className='active-alarms-pagination',
                children=[
                    dbc.Button(
                        id=previous_button_id,
                        color='light',
                        className='active-alarms-pagination-button',
                        n_clicks=0,
                        disabled=True,
                        children=[html.I(className='bi bi-chevron-left')],
                    ),
                    html.Div(
                        id=page_text_id,
                        className='active-alarms-pagination-text',
                        children=['Página 1 de 1'],
                    ),
                    dbc.Button(
                        id=next_button_id,
                        color='light',
                        className='active-alarms-pagination-button',
                        n_clicks=0,
                        disabled=True,
                        children=[html.I(className='bi bi-chevron-right')],
                    ),
                ],
            ),
        ],
    )


def build_alarm_list_children(
    *,
    items: list[dict[str, Any]],
    panel_kind: str,
    page_size: int,
    has_snapshot: bool,
    empty_by_filter: bool,
) -> list[Any]:
    if not has_snapshot:
        return [
            build_initial_state(),
        ]

    if not items:
        return [
            build_empty_state(
                panel_kind=panel_kind,
                empty_by_filter=empty_by_filter,
            ),
        ]

    rows = [
        _build_alarm_row(
            item=item,
            panel_kind=panel_kind,
        )
        for item in items
    ]

    filler_count = max(0, page_size - len(items))

    rows.extend(_build_filler_row(index=index) for index in range(filler_count))

    return rows


def _build_filler_row(
    *,
    index: int,
) -> html.Div:
    return html.Div(
        key=f'filler-{index}',
        className='active-alarm-row active-alarm-row-filler',
    )


def _build_alarm_row(
    *,
    item: dict[str, Any],
    panel_kind: str,
) -> html.Details:
    severity_code = item.get('severity_code') or 'unknown'
    severity_label = item.get('severity_label') or 'Sin severidad'

    row_class_name = f'active-alarm-row active-alarm-row-{severity_code}'

    if item.get('is_inactivity_locked'):
        row_class_name = f'{row_class_name} active-alarm-row-inactive-reactivation'
        severity_code += '-inactiva'

    return html.Details(
        className=row_class_name,
        children=[
            html.Summary(
                className='active-alarm-row-summary',
                children=[
                    html.Div(
                        className='active-alarms-col-severity',
                        children=[
                            html.Span(
                                className=f'active-alarm-severity active-alarm-severity-{severity_code}',
                                children=[severity_label],
                            ),
                        ],
                    ),
                    html.Div(
                        className='active-alarms-col-alarm',
                        children=[
                            html.Div(
                                className='active-alarm-title',
                                children=[item.get('modal_title') or 'Alarma sin título'],
                            ),
                            html.Div(
                                className='active-alarm-kind-wrapper',
                                children=[
                                    html.Div(
                                        className='active-alarm-kind',
                                        children=[item.get('alarm_kind') or 'Sin clasificación'],
                                    ),
                                    html.Span(
                                        className='active-alarm-state-chip active-alarm-state-chip--active',
                                        children=[item.get('status_label')],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className='active-alarms-col-time',
                        children=[
                            html.Div(
                                item.get('start_display') or 'Sin fecha',
                                className='active-alarm-start',
                            ),
                            html.Div(
                                item.get('duration_display') or '--:--:--',
                                className='active-alarm-duration',
                            ),
                        ],
                    ),
                    html.Div(
                        className='active-alarms-col-action active-alarm-chevron-wrapper',
                        children=[
                            html.I(className='bi bi-chevron-down active-alarm-chevron'),
                        ],
                    ),
                ],
            ),
            _build_alarm_detail(
                item=item,
                panel_kind=panel_kind,
            ),
        ],
    )


def _build_alarm_detail(
    *,
    item: dict[str, Any],
    panel_kind: str,
) -> html.Div:
    return html.Div(
        className=f'active-alarm-detail active-alarm-detail-{item.get("severity_code")}',
        children=[
            html.Div(
                className='active-alarm-detail-title',
                children=[
                    html.I(className='bi bi-file-earmark-text'),
                    html.Span('Detalle rápido'),
                ],
            ),
            html.Div(
                className='active-alarm-detail-grid',
                children=[
                    _build_detail_block(
                        label='Alarma',
                        value=item.get('modal_title'),
                    ),
                    _build_detail_block(
                        label='Tipo',
                        value=item.get('alarm_kind'),
                    ),
                    _build_detail_block(
                        label='Descripción',
                        value=item.get('description'),
                    ),
                    _build_detail_block(
                        label='Causa probable',
                        value=item.get('cause'),
                    ),
                    _build_detail_block(
                        label='Desde',
                        value=item.get('start_display'),
                    ),
                    _build_detail_block(
                        label='Última actualización',
                        value=item.get('last_seen_display'),
                    ),
                    _build_detail_block(
                        label='Severidad',
                        value=item.get('severity_label'),
                    ),
                    _build_detail_block(
                        label='Estado operativo',
                        value=item.get('operative_status'),
                    ),
                    _build_detail_block(
                        label='Estado técnico',
                        value=item.get('technical_status'),
                    ),
                ],
            ),
            html.Hr(className='text-muted'),
            html.Div(
                className='active-alarm-detail-actions',
                children=_build_detail_actions(
                    item=item,
                    panel_kind=panel_kind,
                ),
            ),
        ],
    )


def _build_detail_block(
    *,
    label: str,
    value: str,
) -> html.Div:
    return html.Div(
        className='active-alarm-detail-block',
        children=[
            html.Div(label, className='active-alarm-detail-label'),
            html.Div(value, className='active-alarm-detail-value'),
        ],
    )


def _build_detail_actions(
    *,
    item: dict[str, Any],
    panel_kind: str,
) -> list[Any]:
    if panel_kind == 'operator':
        management_enabled = bool(item.get('management_enabled', True))
        # TODO: Momentáneo
        management_enabled = False
        return [
            dbc.Button(
                id=ActiveAlarmsModalIds.build_manage_button_id(
                    row_id=item.get('row_id') or '',
                ),
                className=(
                    'active-alarm-manage-button'
                    if management_enabled
                    else 'active-alarm-manage-button active-alarm-manage-button--disabled'
                ),
                color='danger',
                n_clicks=0,
                disabled=not management_enabled,
                children=[
                    html.Span('Gestionar alarma' if management_enabled else 'Gestión bloqueada'),
                    html.I(className='bi bi-box-arrow-up-right ms-2'),
                ],
            ),
            html.Div(
                className='active-alarm-detail-hint pt-3',
                children=[
                    item.get('management_disabled_reason')
                    or 'Desde aquí puedes acceder a la gestión de alarmas.',
                ],
            ),
        ]

    return [
        html.Div(
            className='active-alarm-detail-hint',
            children=[
                'La información mostrada es solo de seguimiento; '
                'hace referencia a las alarmas que aún permanecen activas tras la gestión'
            ],
        ),
    ]
