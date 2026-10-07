from __future__ import annotations

from typing import Any

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.development.base_component import Component

from ..ids import (
    build_distributed_alarm_bulk_management_open_button_id,
    build_distributed_alarm_bulk_management_source_store_id,
)


def build_distributed_alarm_bulk_management_button(
    *,
    group_key: str,
    group_label: str,
    alarm_items: list[Any] | tuple[Any, ...] | None,
    count: int,
    icon_class_name: str = 'bi bi-collection',
) -> Component:
    normalized_group_key = str(group_key or '').strip()
    normalized_group_label = str(group_label or normalized_group_key or 'Grupo').strip()
    normalized_icon_class_name = str(icon_class_name or 'bi bi-collection').strip()

    if not normalized_group_key or count <= 0:
        return html.Span()

    normalized_items = _normalize_alarm_items(items=alarm_items)

    if not normalized_items:
        return dbc.Badge(
            style={'border': '1px solid #000000'},
            text_color='dark',
            pill=True,
            color='white',
            children=[count],
        )

    return html.Span(
        children=[
            dcc.Store(
                id=build_distributed_alarm_bulk_management_source_store_id(
                    group_key=normalized_group_key,
                ),
                data={
                    'group_key': normalized_group_key,
                    'group_label': normalized_group_label,
                    'icon_class_name': normalized_icon_class_name,
                    'alarm_items': normalized_items,
                },
                storage_type='memory',
            ),
            html.Button(
                id=build_distributed_alarm_bulk_management_open_button_id(
                    group_key=normalized_group_key,
                ),
                className=(
                    'alarm-bulk-management-button border-0 bg-transparent p-0 active-cursor'
                ),
                title=f'Gestionar alarmas {normalized_group_label}',
                n_clicks=0,
                children=[
                    dbc.Badge(
                        style={'border': '1px solid #000000'},
                        text_color='dark',
                        pill=True,
                        color='white',
                        children=[
                            html.I(className=f'{normalized_icon_class_name} pe-1'),
                            count,
                        ],
                    ),
                ],
            ),
        ],
    )


def _normalize_alarm_items(
    *,
    items: list[Any] | tuple[Any, ...] | None,
) -> list[dict[str, Any]]:
    if not items:
        return []

    normalized: list[dict[str, Any]] = []
    seen_alarm_ids: set[str] = set()

    for item in items:
        alarm_id = _read_text(item=item, name='alarm_id')
        group_occurrence_id = _read_text(item=item, name='group_occurrence_id')
        alarm_key = _read_text(item=item, name='alarm_key')
        visibility_group_key = _read_text(item=item, name='visibility_group_key')
        management_scope_key = _read_text(item=item, name='management_scope_key')
        priority_order = _normalize_priority_order(
            value=_read_value(item=item, name='priority_order'),
        )
        target_occurrence_started_at = _read_text(
            item=item, name='target_occurrence_started_at'
        ) or _read_text(item=item, name='start_timestamp')

        if (
            not alarm_id
            or not group_occurrence_id
            or not alarm_key
            or not visibility_group_key
            or not management_scope_key
            or priority_order is None
            or alarm_id in seen_alarm_ids
        ):
            continue

        seen_alarm_ids.add(alarm_id)

        normalized.append(
            {
                'alarm_id': alarm_id,
                'group_occurrence_id': group_occurrence_id,
                'alarm_key': alarm_key,
                'visibility_group_key': visibility_group_key,
                'management_scope_key': management_scope_key,
                'priority_order': priority_order,
                'target_occurrence_started_at': target_occurrence_started_at,
                'operator_bucket': _read_text(item=item, name='operator_bucket') or 'default',
                'alarm_display_name': (
                    _read_text(item=item, name='alarm_display_name')
                    or _read_text(item=item, name='alarm_name')
                    or _read_text(item=item, name='modal_title')
                    or _read_text(item=item, name='title')
                    or alarm_key
                ),
                'title': _read_text(item=item, name='title'),
                'cause': _read_cause(item=item),
                'alarm_kind': _read_text(item=item, name='alarm_kind'),
                'color': _read_text(item=item, name='color'),
            }
        )

    return normalized


def _read_cause(
    *,
    item: Any,
) -> str:
    cause = _read_text(item=item, name='cause')

    if cause:
        return cause

    cause_lines = _read_value(item=item, name='cause_lines')

    if isinstance(cause_lines, (list, tuple)):
        return ' '.join(str(line) for line in cause_lines if line is not None)

    return ''


def _read_text(
    *,
    item: Any,
    name: str,
) -> str:
    value = _read_value(
        item=item,
        name=name,
    )

    return str(value or '').strip()


def _read_value(
    *,
    item: Any,
    name: str,
) -> Any:
    if isinstance(item, dict):
        return item.get(name)

    return getattr(item, name, None)


def _normalize_priority_order(
    *,
    value: Any,
) -> int | None:
    if value is None or value == '':
        return None

    try:
        return int(float(value))
    except Exception:
        return None
