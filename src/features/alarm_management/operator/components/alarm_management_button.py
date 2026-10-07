from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from ..ids import build_alarm_management_open_button_id


def build_alarm_management_button(
    *,
    alarm_id: str | None,
    group_occurrence_id: str | None,
    alarm_key: str | None,
    visibility_group_key: str | None,
    management_scope_key: str | None,
    priority_order: int | str | None,
    target_occurrence_started_at: str | None = None,
    allow_management: bool = True,
    class_name: str = 'bi bi-bell-slash-fill text-white',
) -> Component:
    normalized_alarm_id = str(alarm_id or '').strip()
    normalized_group_occurrence_id = str(group_occurrence_id or '').strip()
    normalized_alarm_key = str(alarm_key or '').strip()
    normalized_visibility_group_key = str(visibility_group_key or '').strip()
    normalized_management_scope_key = str(management_scope_key or '').strip()
    normalized_target_occurrence_started_at = str(target_occurrence_started_at or '').strip()
    normalized_priority_order = _normalize_priority_order(
        priority_order=priority_order,
    )

    if (
        not allow_management
        or not normalized_alarm_id
        or not normalized_group_occurrence_id
        or not normalized_alarm_key
        or not normalized_visibility_group_key
        or not normalized_management_scope_key
        or normalized_priority_order is None
    ):
        return html.Span()

    return html.Button(
        id=build_alarm_management_open_button_id(
            alarm_id=normalized_alarm_id,
            group_occurrence_id=normalized_group_occurrence_id,
            alarm_key=normalized_alarm_key,
            visibility_group_key=normalized_visibility_group_key,
            management_scope_key=normalized_management_scope_key,
            priority_order=normalized_priority_order,
            target_occurrence_started_at=normalized_target_occurrence_started_at,
        ),
        className='alarm-management-icon-button',
        title='Gestionar alarma',
        n_clicks=0,
        children=[
            html.I(
                className=class_name,
            ),
        ],
    )


def _normalize_priority_order(
    *,
    priority_order: int | str | None,
) -> int | None:
    if priority_order is None or priority_order == '':
        return None

    try:
        return int(float(priority_order))
    except Exception:
        return None
