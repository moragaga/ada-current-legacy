from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.app.auth.identity_context import get_current_profile
from src.features.alarm_runtime.front_context.generic import (
    GenericAlarmFrontContextBuilder,
)
from src.features.alarm_runtime.front_context.models import AlarmFrontItem
from src.features.identity.services import AuthorizationService
from src.shared.formatters.duration import format_optional_elapsed_time

from ..models.alarm_card_view_definition import AlarmCardViewDefinition
from ..models.alarm_panel_view_definition import (
    AlarmPanelViewDefinition,
    build_empty_alarm_panel_view_definition,
)
from ..services.alarm_slot_allocator import allocate_alarm_slots


def map_alarm_panel_view_model(
    *,
    alarm_context: dict[str, Any] | None,
) -> AlarmPanelViewDefinition:
    if not alarm_context:
        return build_empty_alarm_panel_view_definition()

    information = alarm_context.get('information')

    front_context = GenericAlarmFrontContextBuilder.build(
        snapshot=information,
    )

    is_management_user = _resolve_is_management_user()

    alarms = [
        _map_alarm_card(
            item=item,
            is_management_user=is_management_user,
        )
        for item in front_context.operator_view
    ]

    alarms.sort(
        key=lambda item: (
            item.ranking,
            item.priority_order,
            item.alarm_key,
        )
    )

    slots = allocate_alarm_slots(
        alarms=alarms,
        total_slots=6,
    )

    return AlarmPanelViewDefinition(
        slots=slots,
        is_management_user=is_management_user,
    )


def _resolve_is_management_user() -> bool:
    profile = get_current_profile()

    return AuthorizationService.can_manage_alarms(
        profile=profile,
    )


def _map_alarm_card(
    *,
    item: AlarmFrontItem,
    is_management_user: bool,
) -> AlarmCardViewDefinition:
    return AlarmCardViewDefinition(
        alarm_id=item.alarm_id,
        group_occurrence_id=item.group_occurrence_id,
        alarm_key=item.alarm_key,
        alarm_name=item.alarm_name,
        visibility_group_key=item.visibility_group_key,
        management_scope_key=item.management_scope_key,
        message_group_key=item.message_group_key,
        target_occurrence_started_at=item.start_timestamp,
        alarm_kind=item.alarm_kind,
        activity_time=_calculate_activity_time(item.start_timestamp),
        title=item.title,
        modal_title=item.modal_title,
        cause_lines=_split_cause_lines(item.cause),
        color=item.color,
        ranking=item.ranking,
        priority_order=item.priority_order,
        is_show_delete=is_management_user,
    )


def _split_cause_lines(value: Any) -> tuple[str, ...]:
    if value is None:
        return tuple()

    lines = [line.strip() for line in str(value).split('\n')]

    return tuple(line for line in lines if line)


def _calculate_activity_time(value: str) -> str:
    if not value:
        return ''

    try:
        normalized_value = str(value).strip()

        if normalized_value.endswith('Z'):
            normalized_value = normalized_value[:-1] + '+00:00'

        activity_time = datetime.fromisoformat(normalized_value)

        if activity_time.tzinfo is None:
            activity_time = activity_time.replace(tzinfo=timezone.utc)

        delta_seconds = (
            datetime.now(timezone.utc) - activity_time.astimezone(timezone.utc)
        ).total_seconds()

        return format_optional_elapsed_time(
            total_seconds=delta_seconds,
        )

    except Exception:
        return ''
