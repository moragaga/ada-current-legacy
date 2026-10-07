from __future__ import annotations

from typing import Any

from ...services.alarm_query_service import AlarmQueryService
from .generic_alarm_front_context import GenericAlarmFrontContext
from .generic_alarm_front_context_builder import GenericAlarmFrontContextBuilder


class GenericAlarmContextService:
    def __init__(
        self,
        query_service: AlarmQueryService,
    ) -> None:
        self._query_service = query_service

    def get_alarm_context(self) -> dict[str, Any]:
        latest_snapshot = self._query_service.get_active_alarms()
        context = self._build_context(
            latest_snapshot=latest_snapshot,
        )

        total_active_alarms = self._get_total_active_alarms(
            context=context,
        )
        total_tracking_alarms = self._get_total_tracking_alarms(
            context=context,
        )

        return {
            'mode': 'generic',
            'last_updated': context.snapshot_timestamp,
            'total_active_alarms': total_active_alarms,
            'total_active_managed_alarms': total_tracking_alarms,
            'total_alarms': total_active_alarms + total_tracking_alarms,
            'distributed_process': False,
            'information': context.to_dict(),
        }

    @staticmethod
    def _build_context(
        *,
        latest_snapshot: dict[str, Any] | None,
    ) -> GenericAlarmFrontContext:
        return GenericAlarmFrontContextBuilder.build(
            snapshot=latest_snapshot,
        )

    @staticmethod
    def _get_total_active_alarms(
        *,
        context,
    ) -> int:
        alarm_keys: set[str] = set()

        for item in getattr(context, 'operator_view', tuple()) or tuple():
            unique_key = _build_alarm_unique_key(item=item)

            if unique_key:
                alarm_keys.add(unique_key)

        for item in getattr(context, 'operator_pool', tuple()) or tuple():
            unique_key = _build_alarm_unique_key(item=item)

            if unique_key:
                alarm_keys.add(unique_key)

        for item in getattr(context, 'inactive_reactivation_view', tuple()) or tuple():
            unique_key = _build_alarm_unique_key(item=item)
            if unique_key:
                alarm_keys.add(unique_key)

        return len(alarm_keys)

    @staticmethod
    def _get_total_tracking_alarms(
        *,
        context,
    ) -> int:
        alarm_keys: set[str] = set()

        for item in getattr(context, 'tracking_view', tuple()) or tuple():
            unique_key = _build_alarm_unique_key(item=item)

            if unique_key:
                alarm_keys.add(unique_key)

        return len(alarm_keys)


def _to_int(
    *,
    value: Any,
    default: int,
) -> int:
    if value is None or value == '':
        return default

    try:
        return int(float(value))
    except Exception:
        return default


def _build_alarm_unique_key(
    *,
    item,
) -> str:
    alarm_id = str(getattr(item, 'alarm_id', '') or '').strip()

    if alarm_id:
        return f'alarm_id::{alarm_id}'

    management_scope_key = str(getattr(item, 'management_scope_key', '') or '').strip()

    if management_scope_key:
        return f'management_scope_key::{management_scope_key}'

    alarm_key = str(getattr(item, 'alarm_key', '') or '').strip()

    if alarm_key:
        return f'alarm_key::{alarm_key}'

    return ''
