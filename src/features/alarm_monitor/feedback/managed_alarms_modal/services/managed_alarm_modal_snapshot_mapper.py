from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.shared.time.timestamps import (
    parse_utc_datetime,
    utc_to_local,
)

from ..constants import (
    DEFAULT_CRITICITY_FILTER,
    DEFAULT_SORT_ORDER,
    DEFAULT_STATUS_FILTER,
    DEFAULT_TURN_SCOPE_FILTER,
    TURN_SCOPE_ALL,
    TURN_SCOPE_CURRENT,
    TURN_SCOPE_PREVIOUS,
)
from ..models import (
    ManagedAlarmModalItem,
)


def build_managed_alarm_modal_snapshot(
    *,
    analytics_snapshot: dict[str, Any] | None,
) -> dict[str, Any]:
    captured_at = datetime.now(timezone.utc)
    source_snapshot = analytics_snapshot or {}

    artifacts = _as_dict(source_snapshot.get('artifacts'))
    managed_alarm_items_artifact = _as_dict(artifacts.get('managed_alarm_items'))
    detail_seed_artifact = _as_dict(artifacts.get('detail_seed'))

    raw_items = _as_list(managed_alarm_items_artifact.get('items'))
    detail_by_action_id = _as_dict(detail_seed_artifact.get('by_action_id'))

    items = [
        _normalize_item(
            raw=item,
            detail_by_action_id=detail_by_action_id,
            index=index,
        ).to_dict()
        for index, item in enumerate(raw_items)
        if isinstance(item, dict)
    ]

    snapshot_timestamp = _safe_str(source_snapshot.get('snapshot_timestamp'))

    snapshot = {
        'captured_at': captured_at.isoformat(),
        'captured_at_display': _format_datetime(
            value=utc_to_local(captured_at),
        ),
        'source_snapshot_timestamp': snapshot_timestamp,
        'source_snapshot_timestamp_display': _format_datetime(
            value=utc_to_local(parse_utc_datetime(value=snapshot_timestamp))
            if snapshot_timestamp
            else None,
        ),
        'window': _as_dict(source_snapshot.get('window')),
        'summary_metrics': _as_dict(artifacts.get('summary_metrics')),
        'managed_alarm_counts': _as_dict(artifacts.get('managed_alarm_counts')),
        'recurrence_trends': _as_dict(artifacts.get('recurrence_trends')),
        'inactivity_expiration': _as_dict(artifacts.get('inactivity_expiration')),
        'items': items,
        'meta': {
            'items_total': len(items),
            'snapshot_type': _safe_str(source_snapshot.get('snapshot_type')),
            'schema_version': source_snapshot.get('schema_version'),
        },
        'turn_scope_options': get_turn_scope_options(),
        'default_turn_scope_filter': resolve_default_turn_scope_filter(),
    }

    return snapshot


def build_paginated_view(
    *,
    snapshot: dict[str, Any] | None,
    search_text: str | None,
    sort_order_time: str | None,
    filter_criticity: str | None,
    filter_status: str | None,
    filter_turn_scope: str | None,
    page: int | None,
    page_size: int,
) -> dict[str, Any]:
    has_snapshot = bool(snapshot)
    snapshot = snapshot or {}

    items = _as_list(snapshot.get('items'))

    filtered_items = _filter_by_search_text(
        items=items,
        query=(search_text or '').strip().lower(),
    )

    filtered_items = _filter_criticity(
        items=filtered_items,
        filter_criticity=filter_criticity,
    )

    filtered_items = _filter_status(
        items=filtered_items,
        filter_status=filter_status,
    )

    filtered_items = _filter_turn_scope(
        items=filtered_items,
        filter_turn_scope=filter_turn_scope,
    )

    sorted_items = _sort_by_requested_time(
        items=filtered_items,
        sort_order_time=sort_order_time,
    )

    total_items = len(sorted_items)
    total_pages = max(1, (total_items + page_size - 1) // page_size)

    safe_page = page or 1
    safe_page = max(1, min(safe_page, total_pages))

    start_index = (safe_page - 1) * page_size
    end_index = start_index + page_size

    return {
        'has_snapshot': has_snapshot,
        'items': sorted_items[start_index:end_index],
        'total_items': total_items,
        'total_pages': total_pages,
        'page': safe_page,
        'page_size': page_size,
        'has_previous': safe_page > 1,
        'has_next': safe_page < total_pages,
        'empty_by_filter': has_snapshot
        and total_items == 0
        and (
            bool(search_text)
            or (filter_criticity or DEFAULT_CRITICITY_FILTER) != 'all'
            or (filter_status or DEFAULT_STATUS_FILTER) != 'all'
            or (filter_turn_scope or DEFAULT_TURN_SCOPE_FILTER) != 'all'
        ),
    }


def get_total_pages_for_items(
    *,
    snapshot: dict[str, Any] | None,
    search_text: str | None,
    sort_order_time: str | None,
    filter_criticity: str | None,
    filter_status: str | None,
    filter_turn_scope: str | None,
    page_size: int,
) -> int:
    view = build_paginated_view(
        snapshot=snapshot,
        search_text=search_text,
        sort_order_time=sort_order_time,
        filter_criticity=filter_criticity,
        filter_status=filter_status,
        filter_turn_scope=filter_turn_scope,
        page=1,
        page_size=page_size,
    )

    return int(view['total_pages'])


def get_next_page(
    *,
    current_page: int | None,
    direction: str,
    total_pages: int,
) -> int:
    page = current_page or 1

    if direction == 'previous':
        return max(1, page - 1)

    if direction == 'next':
        return min(total_pages, page + 1)

    return max(1, min(page, total_pages))


def get_turn_scope_options() -> list[dict[str, str]]:
    return [
        {
            'label': 'Actual',
            'value': TURN_SCOPE_CURRENT,
        },
        {
            'label': 'Anterior',
            'value': TURN_SCOPE_PREVIOUS,
        },
        {
            'label': 'Ambos',
            'value': TURN_SCOPE_ALL,
        },
    ]


def resolve_default_turn_scope_filter() -> str:
    return TURN_SCOPE_CURRENT


def get_recurrence_payload_for_turn_scope(
    *,
    snapshot: dict[str, Any] | None,
    turn_scope_filter: str | None,
) -> dict[str, Any]:
    snapshot = snapshot or {}
    recurrence = _as_dict(snapshot.get('recurrence_trends'))
    selected_scope = _safe_str(turn_scope_filter) or DEFAULT_TURN_SCOPE_FILTER

    if selected_scope == TURN_SCOPE_ALL:
        return recurrence

    by_turn_scope = _as_dict(recurrence.get('by_turn_scope'))

    return _as_dict(by_turn_scope.get(selected_scope))


def get_time_range_for_turn_scope(
    *,
    snapshot: dict[str, Any] | None,
    turn_scope_filter: str | None,
) -> tuple[datetime, datetime]:
    snapshot = snapshot or {}
    window = _as_dict(snapshot.get('window'))
    selected_scope = _safe_str(turn_scope_filter) or DEFAULT_TURN_SCOPE_FILTER

    if selected_scope == TURN_SCOPE_ALL:
        return (
            utc_to_local(
                value=parse_utc_datetime(
                    value=window.get('previous_turn', {}).get('turn_start_utc')
                )
            ),
            utc_to_local(
                value=parse_utc_datetime(value=window.get('current_turn', {}).get('turn_end_utc'))
            ),
        )

    normalize_turn = f'{turn_scope_filter}_turn'
    return (
        utc_to_local(
            value=parse_utc_datetime(value=window.get(normalize_turn, {}).get('turn_start_utc'))
        ),
        utc_to_local(
            value=parse_utc_datetime(value=window.get(normalize_turn, {}).get('turn_end_utc'))
        ),
    )


def _normalize_item(
    *,
    raw: dict[str, Any],
    detail_by_action_id: dict[str, Any],
    index: int,
) -> ManagedAlarmModalItem:
    action_id = _safe_str(raw.get('action_id'))
    alarm_id = _safe_str(raw.get('alarm_id'))
    alarm_key = _safe_str(raw.get('alarm_key'))

    requested_at = _safe_str(raw.get('requested_at'))
    occurrence_started_at = _safe_str(raw.get('source_occurrence_started_at')) or _safe_str(
        raw.get('target_occurrence_started_at')
    )
    expires_at = _safe_str(raw.get('expires_at'))

    requested_at_local = (
        utc_to_local(parse_utc_datetime(value=requested_at)) if requested_at else None
    )

    occurrence_started_at_local = (
        utc_to_local(parse_utc_datetime(value=occurrence_started_at))
        if occurrence_started_at
        else None
    )

    expires_at_local = utc_to_local(parse_utc_datetime(value=expires_at)) if expires_at else None

    severity_code, severity_label = _resolve_severity(raw=raw)

    action_type = _safe_str(raw.get('action_type'))
    management_status = _safe_str(raw.get('management_status'))

    predefined_message = _safe_str(raw.get('predefined_message'))
    personalized_message = _safe_str(raw.get('personalized_message'))

    return ManagedAlarmModalItem(
        row_id=f'managed-{index}-{action_id or alarm_id or alarm_key}',
        action_id=action_id,
        alarm_id=alarm_id,
        alarm_key=alarm_key,
        group_occurrence_id=_safe_str(raw.get('group_occurrence_id')),
        turn_scope_code=_safe_str(raw.get('turn_scope_code')),
        turn_scope_label=_safe_str(raw.get('turn_scope_label')),
        turn_group_code=_safe_str(raw.get('turn_group_code')),
        turn_group_label=_safe_str(raw.get('turn_group_code')),
        is_current_turn=bool(raw.get('is_current_turn')),
        is_previous_turn=bool(raw.get('is_previous_turn')),
        title=_safe_str(raw.get('title')) or 'Alarma sin título',
        alarm_display_name=(
            _safe_str(raw.get('alarm_display_name'))
            or _safe_str(raw.get('alarm_name'))
            or alarm_key
        ),
        cause=_safe_str(raw.get('cause')) or 'Sin causa informada.',
        severity_code=severity_code,
        severity_label=severity_label,
        action_type=action_type,
        management_status=management_status,
        status_label=_resolve_status_label(
            action_type=action_type,
            management_status=management_status,
            is_still_active=bool(raw.get('is_still_active')),
            is_inactivity_active=bool(raw.get('is_inactivity_active')),
        ),
        alarm_status_label=_resolve_alarm_status_label(
            is_still_active=bool(raw.get('is_still_active'))
        ),
        management_status_label=_resolve_management_status_label(
            action_type=action_type,
            management_status=management_status,
        ),
        requested_at=requested_at or None,
        requested_display=_format_datetime(value=requested_at_local),
        occurrence_started_at=occurrence_started_at or None,
        occurrence_started_display=_format_datetime(
            value=occurrence_started_at_local,
        ),
        expires_at=expires_at or None,
        expires_display=_format_datetime(
            value=expires_at_local,
            fallback='Sin vencimiento',
        ),
        time_to_management_seconds=_optional_int(
            raw.get('time_to_management_seconds'),
        ),
        time_to_management_display=_format_duration_from_seconds(
            raw.get('time_to_management_seconds'),
        ),
        requested_by_name=_safe_str(raw.get('requested_by_name')) or 'Sin usuario',
        requested_by_email=_safe_str(raw.get('requested_by_email')),
        predefined_message=predefined_message,
        personalized_message=personalized_message,
        message_display=_build_message_display(
            predefined_message=predefined_message,
            personalized_message=personalized_message,
        ),
        is_inactive_management=bool(raw.get('is_inactive_management')),
        is_still_active=bool(raw.get('is_still_active')),
        is_inactivity_active=bool(raw.get('is_inactivity_active')),
        detail=_as_dict(detail_by_action_id.get(action_id)),
        raw=raw,
    )


def _filter_by_search_text(
    *,
    items: list[dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    if not query:
        return items

    searchable_fields = (
        'alarm_display_name',
        'title',
        'cause',
        'alarm_key',
        'turn_scope_label',
        'turn_group_label',
        'predefined_message',
        'personalized_message',
    )

    return [
        item
        for item in items
        if any(query in _safe_str(item.get(field)).lower() for field in searchable_fields)
    ]


def _sort_by_requested_time(
    *,
    items: list[dict[str, Any]],
    sort_order_time: str | None,
) -> list[dict[str, Any]]:
    reverse = (sort_order_time or DEFAULT_SORT_ORDER) != 'oldest'

    return sorted(
        items,
        key=lambda item: (
            _parse_datetime(item.get('requested_at')) or datetime.min.replace(tzinfo=timezone.utc)
        ),
        reverse=reverse,
    )


def _filter_criticity(
    *,
    items: list[dict[str, Any]],
    filter_criticity: str | None,
) -> list[dict[str, Any]]:
    value = (filter_criticity or DEFAULT_CRITICITY_FILTER).lower()

    if value == 'all':
        return items

    return [item for item in items if _safe_str(item.get('severity_code')).lower() == value]


def _filter_status(
    *,
    items: list[dict[str, Any]],
    filter_status: str | None,
) -> list[dict[str, Any]]:
    value = (filter_status or DEFAULT_STATUS_FILTER).lower()

    if value == 'all':
        return items

    if value == 'managed':
        return [
            item
            for item in items
            if (
                _safe_str(item.get('action_type')).lower() == 'manual'
                or _safe_str(item.get('management_status')).lower() == 'managed'
            )
            and not bool(item.get('is_inactive_management'))
        ]

    if value == 'inactive':
        return [
            item
            for item in items
            if (
                bool(item.get('is_inactive_management'))
                or _safe_str(item.get('action_type')).lower() == 'inactive'
            )
        ]

    if value == 'still_active':
        return [item for item in items if bool(item.get('is_still_active'))]

    return items


def _filter_turn_scope(
    *,
    items: list[dict[str, Any]],
    filter_turn_scope: str | None,
) -> list[dict[str, Any]]:
    value = (filter_turn_scope or DEFAULT_TURN_SCOPE_FILTER).lower()

    if value == TURN_SCOPE_ALL:
        return items

    return [item for item in items if _safe_str(item.get('turn_scope_code')).lower() == value]


def _resolve_severity(
    *,
    raw: dict[str, Any],
) -> tuple[str, str]:
    alarm_key = _safe_str(raw.get('alarm_key')).upper()
    alarm_display_name = _safe_str(raw.get('alarm_display_name')).upper()

    if alarm_key.startswith('IMPACTO_') or 'IMPACTO' in alarm_display_name:
        return 'impacto', 'Impacto'

    if alarm_key.startswith('RIESGO_') or 'RIESGO' in alarm_display_name:
        return 'riesgo', 'Riesgo'

    return 'unknown', 'Sin severidad'


def _resolve_status_label(
    *,
    action_type: str,
    management_status: str,
    is_still_active: bool,
    is_inactivity_active: bool,
) -> str:
    if is_inactivity_active:
        return 'Desactivada vigente'

    if action_type == 'inactive':
        return 'Desactivada'

    if is_still_active:
        return 'Gestionada · sigue activa'

    if management_status == 'managed' or action_type == 'manual':
        return 'Gestionada'

    return 'Gestionada'


def _resolve_alarm_status_label(
    *,
    is_still_active: bool,
):
    return 'Activa' if is_still_active else 'Inactiva'


def _resolve_management_status_label(*, action_type: bool, management_status: str):
    if action_type == 'inactive':
        return 'Desactivada'
    elif management_status == 'managed' or action_type == 'manual':
        return 'Gestionada'
    else:
        return 'Estado desconocido'


def _build_message_display(
    *,
    predefined_message: str,
    personalized_message: str,
) -> str:
    if predefined_message and personalized_message:
        return f'{predefined_message} · {personalized_message}'

    if personalized_message:
        return personalized_message

    if predefined_message:
        return predefined_message

    return 'Sin mensaje informado'


def _format_datetime(
    *,
    value: Any,
    fallback: str = 'Sin fecha',
) -> str:
    if value is None:
        return fallback

    try:
        return value.strftime('%Y-%m-%d %H:%M:%S')
    except Exception:
        return _safe_str(value) or fallback


def _format_duration_from_seconds(value: Any) -> str:
    seconds = _optional_int(value)

    if seconds is None:
        return '--:--:--'

    hours = seconds // 3600
    minutes = seconds % 3600 // 60
    remaining_seconds = seconds % 60

    return f'{hours:02d}:{minutes:02d}:{remaining_seconds:02d}'


def _parse_datetime(value: Any) -> datetime | None:
    text = _safe_str(value)

    if not text:
        return None

    try:
        normalized = text.replace('Z', '+00:00')
        parsed = datetime.fromisoformat(normalized)

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)

    except ValueError:
        return None


def _optional_int(value: Any) -> int | None:
    if value is None or value == '':
        return None

    try:
        return int(float(value))
    except Exception:
        return None


def _safe_str(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


def _as_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    return {}


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    return []
