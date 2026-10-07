from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.app.auth.identity_context import get_current_profile
from src.features.identity.services import AuthorizationService
from src.shared.formatters.duration import format_optional_elapsed_time

from ..models.distributed_alarm_bulk_group_view_definition import (
    DistributedAlarmBulkGroupViewDefinition,
)
from ..models.distributed_alarm_card_view_definition import (
    DistributedAlarmCardViewDefinition,
)
from ..models.distributed_alarm_panel_view_definition import (
    DistributedAlarmPanelViewDefinition,
    build_empty_distributed_alarm_panel_view_definition,
)
from ..services.distributed_alarm_slot_allocator import (
    allocate_distributed_alarm_slots,
)


def map_distributed_alarm_panel_view_model(
    *,
    alarm_context: dict[str, Any] | None,
) -> DistributedAlarmPanelViewDefinition:
    information = _resolve_information(
        alarm_context=alarm_context,
    )

    if not information:
        return build_empty_distributed_alarm_panel_view_definition()

    is_management_user = _resolve_is_management_user()

    default_alarms = [
        _map_alarm_card(
            item=item,
            is_management_user=is_management_user,
        )
        for item in _read_list(
            data=information,
            key='default_operator_view',
        )
    ]

    default_alarms.sort(
        key=lambda item: (
            item.ranking,
            item.priority_order,
            item.alarm_key,
        )
    )

    bulk_group = _map_first_bulk_group(
        groups=_read_list(
            data=information,
            key='distributed_groups',
        ),
        is_management_user=is_management_user,
    )

    bulk_group_alarm = None

    if bulk_group is not None and bulk_group.items:
        bulk_group_alarm = bulk_group.items[0]

    slots = allocate_distributed_alarm_slots(
        normal_alarms=default_alarms,
        bulk_group_alarm=bulk_group_alarm,
        total_slots=6,
    )

    return DistributedAlarmPanelViewDefinition(
        slots=slots,
        is_management_user=is_management_user,
        bulk_group=bulk_group,
    )


def _resolve_is_management_user() -> bool:
    profile = get_current_profile()

    return AuthorizationService.can_manage_alarms(
        profile=profile,
    )


def _resolve_information(
    *,
    alarm_context: dict[str, Any] | None,
) -> dict[str, Any] | None:
    if not isinstance(alarm_context, dict) or not alarm_context:
        return None

    information = alarm_context.get('information')

    if isinstance(information, dict) and information:
        return information

    if _looks_like_distributed_information(
        data=alarm_context,
    ):
        return alarm_context

    return None


def _looks_like_distributed_information(
    *,
    data: dict[str, Any],
) -> bool:
    return any(
        key in data
        for key in (
            'default_operator_view',
            'default_operator_pool',
            'tracking_view',
            'distributed_groups',
            'snapshot_timestamp',
            'meta',
        )
    )


def _map_first_bulk_group(
    *,
    groups: list[Any],
    is_management_user: bool,
) -> DistributedAlarmBulkGroupViewDefinition | None:
    if not groups:
        return None

    group = groups[0]

    group_key = _read_text(
        item=group,
        key='group_key',
    )
    group_label = (
        _read_text(
            item=group,
            key='group_label',
        )
        or group_key
        or 'Grupo'
    )
    icon_class_name = (
        _read_text(
            item=group,
            key='icon_class_name',
        )
        or 'bi bi-collection'
    )

    raw_items = _read_list(
        data=group,
        key='items',
    )

    items = tuple(
        _deduplicate_cards_by_alarm_id(
            cards=[
                _map_alarm_card(
                    item=item,
                    is_management_user=is_management_user,
                )
                for item in raw_items
            ]
        )
    )

    if not items:
        return None

    return DistributedAlarmBulkGroupViewDefinition(
        key=group_key,
        label=group_label,
        count=len(items),
        items=items,
        anchor_alarm_id=items[0].alarm_id,
        icon_class_name=icon_class_name,
    )


def _map_alarm_card(
    *,
    item: Any,
    is_management_user: bool,
) -> DistributedAlarmCardViewDefinition:
    alarm_id = _read_text(
        item=item,
        key='alarm_id',
    )
    alarm_key = _read_text(
        item=item,
        key='alarm_key',
    )
    start_timestamp = _read_text(
        item=item,
        key='start_timestamp',
    )

    return DistributedAlarmCardViewDefinition(
        alarm_id=alarm_id,
        group_occurrence_id=_read_text(
            item=item,
            key='group_occurrence_id',
        ),
        alarm_key=alarm_key,
        alarm_name=(
            _read_text(
                item=item,
                key='alarm_name',
            )
            or alarm_key
        ),
        visibility_group_key=_read_text(
            item=item,
            key='visibility_group_key',
        ),
        management_scope_key=_read_text(
            item=item,
            key='management_scope_key',
        ),
        message_group_key=_read_text(
            item=item,
            key='message_group_key',
        ),
        target_occurrence_started_at=start_timestamp,
        alarm_kind=_read_text(
            item=item,
            key='alarm_kind',
        ),
        activity_time=_calculate_activity_time(
            start_timestamp,
        ),
        title=_read_text(
            item=item,
            key='title',
        ),
        modal_title=_read_text(
            item=item,
            key='modal_title',
        ),
        cause_lines=_split_cause_lines(
            _read_value(
                item=item,
                key='cause',
            )
        ),
        color=_read_text(
            item=item,
            key='color',
        ),
        ranking=_read_int(
            item=item,
            key='ranking',
            default=999999,
        ),
        priority_order=_read_int(
            item=item,
            key='priority_order',
            default=999999,
        ),
        is_show_delete=is_management_user,
        operator_bucket=(
            _read_text(
                item=item,
                key='operator_bucket',
            )
            or 'default'
        ),
    )


def _deduplicate_cards_by_alarm_id(
    *,
    cards: list[DistributedAlarmCardViewDefinition],
) -> list[DistributedAlarmCardViewDefinition]:
    result: list[DistributedAlarmCardViewDefinition] = []
    seen_alarm_ids: set[str] = set()

    for card in cards:
        alarm_id = str(card.alarm_id or '').strip()

        if not alarm_id:
            continue

        if alarm_id in seen_alarm_ids:
            continue

        seen_alarm_ids.add(alarm_id)
        result.append(card)

    return result


def _read_list(
    *,
    data: Any,
    key: str,
) -> list[Any]:
    value = _read_value(
        item=data,
        key=key,
    )

    if isinstance(value, list):
        return value

    if isinstance(value, tuple):
        return list(value)

    return []


def _read_text(
    *,
    item: Any,
    key: str,
) -> str:
    value = _read_value(
        item=item,
        key=key,
    )

    return str(value or '').strip()


def _read_int(
    *,
    item: Any,
    key: str,
    default: int,
) -> int:
    value = _read_value(
        item=item,
        key=key,
    )

    try:
        return int(float(value))
    except Exception:
        return default


def _read_value(
    *,
    item: Any,
    key: str,
) -> Any:
    if isinstance(item, dict):
        return item.get(key)

    return getattr(item, key, None)


def _split_cause_lines(value: Any) -> tuple[str, ...]:
    if value is None:
        return tuple()

    lines = [line.strip() for line in str(value).split('\n')]

    return tuple(line for line in lines if line)


def _calculate_activity_time(value: str | None) -> str:
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
