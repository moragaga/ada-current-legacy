from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.shared.time.timestamps import parse_utc_datetime, utc_to_local

from ..models.active_alarm_modal_item import (
    ActiveAlarmModalItem,
)


def build_active_alarm_modal_snapshot(
    *,
    runtime_store: dict[str, Any] | None,
) -> dict[str, Any]:
    captured_at = datetime.now(timezone.utc)
    information = _extract_information(runtime_store=runtime_store)

    source_last_updated = (
        _safe_str((runtime_store or {}).get('last_updated')) or captured_at.isoformat()
    )
    capture_at_display = utc_to_local(captured_at)
    source_last_updated_display = utc_to_local(parse_utc_datetime(value=source_last_updated))

    operator_raw_items = _extract_operator_items(
        information=information,
    )
    tracking_raw_items = _tag_modal_items(
        items=_as_list(information.get('tracking_view')),
        view_bucket_code='tracking',
        view_bucket_label='Tracking View',
        is_inactivity_locked=False,
    )

    operator_items = [
        _normalize_item(
            raw=item,
            source='operator_pool',
            index=index,
        ).to_dict()
        for index, item in enumerate(operator_raw_items)
    ]

    tracking_items = [
        _normalize_item(
            raw=item,
            source='tracking_view',
            index=index,
        ).to_dict()
        for index, item in enumerate(tracking_raw_items)
    ]

    return {
        'captured_at': captured_at.isoformat(),
        'captured_at_display': _format_datetime(value=capture_at_display),
        'source_last_updated': source_last_updated,
        'source_last_updated_display': _format_datetime(value=source_last_updated_display),
        'operator_items': operator_items,
        'tracking_items': tracking_items,
        'meta': {
            'operator_total': len(operator_items),
            'tracking_total': len(tracking_items),
        },
    }


def build_paginated_view(
    *,
    snapshot: dict[str, Any] | None,
    source_key: str,
    search_text: str | None,
    sort_order_time: str | None,
    filter_criticity: str | None,
    page: int | None,
    page_size: int,
) -> dict[str, Any]:
    has_snapshot = bool(snapshot)
    snapshot = snapshot or {}

    items = _as_list(snapshot.get(source_key))

    filtered_items = _filter_by_title(
        items=items,
        query=(search_text or '').strip().lower(),
    )

    sorted_items = _sort_by_time(
        items=filtered_items,
        sort_order_time=sort_order_time,
    )

    filtered_items = _filter_criticity(
        items=sorted_items,
        filter_criticity=filter_criticity,
    )

    total_items = len(filtered_items)
    total_pages = max(1, (total_items + page_size - 1) // page_size)

    safe_page = page or 1
    safe_page = max(1, min(safe_page, total_pages))

    start_index = (safe_page - 1) * page_size
    end_index = start_index + page_size

    page_items = filtered_items[start_index:end_index]

    return {
        'has_snapshot': has_snapshot,
        'items': page_items,
        'total_items': total_items,
        'total_pages': total_pages,
        'page': safe_page,
        'page_size': page_size,
        'has_previous': safe_page > 1,
        'has_next': safe_page < total_pages,
        'empty_by_filter': has_snapshot and bool(search_text) and total_items == 0,
    }


def get_total_pages_for_source(
    *,
    snapshot: dict[str, Any] | None,
    source_key: str,
    search_text: str | None,
    sort_order_time: str | None,
    filter_criticity: str | None,
    page_size: int,
) -> int:
    view = build_paginated_view(
        snapshot=snapshot,
        source_key=source_key,
        search_text=search_text,
        sort_order_time=sort_order_time,
        filter_criticity=filter_criticity,
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


def _extract_information(
    *,
    runtime_store: dict[str, Any] | None,
) -> dict[str, Any]:
    if not runtime_store:
        return {}

    information = runtime_store.get('information')

    if isinstance(information, dict):
        return information

    return runtime_store


def _extract_operator_items(
    *,
    information: dict[str, Any],
) -> list[dict[str, Any]]:
    base_items = _tag_modal_items(
        items=(
            _as_list(information.get('default_operator_pool'))
            or _as_list(information.get('operator_pool'))
            or _as_list(information.get('default_operator_view'))
            or _as_list(information.get('operator_view'))
        ),
        view_bucket_code='operator',
        view_bucket_label='Operator Pool',
        is_inactivity_locked=False,
    )

    distributed_items: list[dict[str, Any]] = []

    for group in _as_list(information.get('distributed_groups')):
        if not isinstance(group, dict):
            continue

        distributed_items.extend(
            _tag_modal_items(
                items=_as_list(group.get('items')),
                view_bucket_code='distributed_group',
                view_bucket_label=_safe_str(group.get('group_label')) or 'Grupo distribuido',
                is_inactivity_locked=False,
            ),
        )

    inactive_reactivation_items = _tag_modal_items(
        items=(
            _as_list(information.get('inactive_reactivation_items'))
            or _as_list(information.get('inactive_reactivation_view'))
            or _as_list(information.get('inactive_reactivation_pool'))
        ),
        view_bucket_code='inactive_reactivation',
        view_bucket_label='Reactivada con bloqueo',
        is_inactivity_locked=True,
    )

    return _deduplicate_items(
        items=[
            *base_items,
            *distributed_items,
            *inactive_reactivation_items,
        ],
    )


def _tag_modal_items(
    *,
    items: list[dict[str, Any]],
    view_bucket_code: str,
    view_bucket_label: str,
    is_inactivity_locked: bool,
) -> list[dict[str, Any]]:
    tagged_items: list[dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        tagged_items.append(
            {
                **item,
                '_modal_view_bucket_code': view_bucket_code,
                '_modal_view_bucket_label': view_bucket_label,
                '_modal_is_inactivity_locked': is_inactivity_locked,
            },
        )

    return tagged_items


def _normalize_item(
    *,
    raw: dict[str, Any],
    source: str,
    index: int,
) -> ActiveAlarmModalItem:
    if not isinstance(raw, dict):
        raw = {}

    alarm_id = _safe_str(raw.get('alarm_id'))
    alarm_key = _safe_str(raw.get('alarm_key'))

    severity_code, severity_label = _resolve_severity(
        raw=raw,
    )

    start_timestamp = utc_to_local(parse_utc_datetime(_safe_str(raw.get('start_timestamp'))))
    last_seen_timestamp = utc_to_local(parse_utc_datetime(_safe_str(raw.get('last_seen_at'))))

    row_key = (
        _safe_str(raw.get('alarm_occurrence_id'))
        or _safe_str(raw.get('group_occurrence_id'))
        or alarm_id
        or alarm_key
        or f'{source}-{index}'
    )

    view_bucket_code = (
        _safe_str(raw.get('_modal_view_bucket_code')) or _safe_str(raw.get('source_view')) or source
    )

    view_bucket_label = (
        _safe_str(raw.get('_modal_view_bucket_label'))
        or _safe_str(raw.get('source_view_label'))
        or _resolve_default_view_bucket_label(source=source)
    )

    is_inactivity_locked = (
        bool(raw.get('_modal_is_inactivity_locked')) or view_bucket_code == 'inactive_reactivation'
    )

    technical_status = _translate_status(value=raw.get('status'))

    if is_inactivity_locked:
        state_label = 'Activa · bloqueo por inactividad'
        management_enabled = False
        management_disabled_reason = (
            'Esta alarma está activa, pero mantiene un bloqueo por inactividad.'
        )
    else:
        management_disabled_reason = ''
        if source == 'operator_pool':
            state_label = 'Activa'
            management_enabled = True
        else:
            state_label = 'Activa · {0}'.format(technical_status)
            management_enabled = False

    return ActiveAlarmModalItem(
        row_id=f'{source}-{index}-{row_key}',
        source=source,
        alarm_id=alarm_id,
        alarm_key=alarm_key,
        title=_safe_str(raw.get('title')) or 'Alarma sin título',
        modal_title=_clean_title(raw.get('modal_title')),
        alarm_kind=_safe_str(raw.get('alarm_kind')) or 'unknown',
        severity_code=severity_code,
        severity_label=severity_label,
        start_timestamp=start_timestamp,
        start_display=_format_datetime(value=start_timestamp),
        last_seen_display=_format_datetime(value=last_seen_timestamp),
        duration_display=_format_duration_from_seconds(value=_safe_str(raw.get('duration'))),
        description=_safe_str(raw.get('title'))
        or 'Descripción no informada',  # TODO: Ver si agregar una descripción
        cause=_safe_str(raw.get('cause')) or 'Sin causa informada.',
        operative_status='Activa',
        status_label=state_label,
        operator_bucket=_safe_str(raw.get('operator_bucket')),
        family=_safe_str(raw.get('family')),
        view_bucket_code=view_bucket_code,
        view_bucket_label=view_bucket_label,
        technical_status=technical_status,
        is_inactivity_locked=is_inactivity_locked,
        management_enabled=management_enabled,
        management_disabled_reason=management_disabled_reason,
        raw=raw,
    )


def _resolve_default_view_bucket_label(
    *,
    source: str,
) -> str:
    if source == 'tracking_view':
        return 'Tracking View'

    if source == 'operator_pool':
        return 'Operator Pool'

    return 'Vista de alarmas'


def _resolve_severity(
    *,
    raw: dict[str, Any],
) -> tuple[str, str]:
    value = _safe_str(raw.get('color'))

    if value == 'yellow':
        return 'riesgo', 'Riesgo'

    if value == 'red':
        return 'impacto', 'Impacto'

    if value == 'blue':
        return '', ''

    return 'unknown', 'Sin severidad'


def _filter_by_title(
    *,
    items: list[dict[str, Any]],
    query: str,
) -> list[dict[str, Any]]:
    if not query:
        return items

    return [item for item in items if query in _safe_str(item.get('title')).lower()]


def _sort_by_time(
    *,
    items: list[dict[str, Any]],
    sort_order_time: str | None,
) -> list[dict[str, Any]]:
    reverse = sort_order_time != 'oldest'

    return sorted(
        items,
        key=lambda item: (
            _parse_datetime(item.get('start_timestamp'))
            or datetime.min.replace(tzinfo=timezone.utc)
        ),
        reverse=reverse,
    )


def _filter_criticity(
    *,
    items: list[dict[str, Any]],
    filter_criticity: str | None,
) -> list[dict[str, Any]]:

    if (filter_criticity or 'all').lower() == 'all':
        return items

    return list(
        filter(
            lambda item: filter_criticity in _safe_str(item.get('alarm_kind')).lower(),
            items,
        )
    )


def _deduplicate_items(
    *,
    items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()

    for index, item in enumerate(items):
        if not isinstance(item, dict):
            continue

        key = _build_item_identity_key(
            item=item,
            index=index,
        )

        if key in seen:
            continue

        seen.add(key)
        result.append(item)

    return result


def _build_item_identity_key(
    *,
    item: dict[str, Any],
    index: int,
) -> str:
    alarm_occurrence_id = _safe_str(item.get('alarm_occurrence_id'))
    group_occurrence_id = _safe_str(item.get('group_occurrence_id'))
    alarm_id = _safe_str(item.get('alarm_id'))
    alarm_key = _safe_str(item.get('alarm_key'))
    start_timestamp = (
        _safe_str(item.get('start_timestamp'))
        or _safe_str(item.get('first_seen_at'))
        or _safe_str(item.get('timestamp'))
    )
    view_bucket_code = _safe_str(item.get('_modal_view_bucket_code'))

    if alarm_occurrence_id:
        return f'occurrence::{alarm_occurrence_id}'

    if group_occurrence_id and alarm_key:
        return f'group_occurrence::{group_occurrence_id}::alarm::{alarm_key}'

    if alarm_id and start_timestamp:
        return f'alarm_id::{alarm_id}::start::{start_timestamp}'

    if alarm_key and start_timestamp:
        return f'alarm_key::{alarm_key}::start::{start_timestamp}'

    if alarm_id:
        return f'{view_bucket_code}::alarm_id::{alarm_id}'

    if alarm_key:
        return f'{view_bucket_code}::alarm_key::{alarm_key}'

    return f'{view_bucket_code}::index::{index}'


def _as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value

    return []


def _safe_str(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


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


def _format_datetime(value: Any) -> str:
    if value is None:
        return _safe_str(value) or 'Sin fecha'

    return value.strftime('%Y-%m-%d %H:%M:%S')


# TODO: CAMBIAR TEXTO EN CONFIGURACIÓN
def _clean_title(title: str) -> str:
    if title is None:
        return ''

    return _safe_str(title).replace('Impacto', '').replace('Riesgo', '').strip()


def _format_duration_from_seconds(value: Any) -> str | None:
    if value is None:
        return '--:--:--'

    if isinstance(value, str):
        value = int(float(value))

    hours = value // 3600
    minutes = value % 3600 // 60
    remaining_seconds = value % 60

    return f'{hours:02d}:{minutes:02d}:{remaining_seconds:02d}'


def _translate_status(value: Any) -> str | None:
    if value is None:
        return None

    translation_dict = {'managed': 'Gestionada', 'inactive': 'Desactivada'}

    value = _safe_str(value).lower()
    return translation_dict.get(value, 'Activa')
