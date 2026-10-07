from __future__ import annotations

from typing import Any

from ...services.alarm_query_service import AlarmQueryService
from .distributed_alarm_front_context import DistributedAlarmFrontContext
from .distributed_alarm_front_context_builder import DistributedAlarmFrontContextBuilder


class DistributedAlarmContextService:
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
            'mode': 'distributed',
            'last_updated': context.snapshot_timestamp,
            'total_active_alarms': total_active_alarms,
            'total_active_managed_alarms': total_tracking_alarms,
            'total_alarms': total_active_alarms + total_tracking_alarms,
            'distributed_process': True,
            'information': context.to_dict(),
        }

    @staticmethod
    def _build_context(
        *,
        latest_snapshot: dict[str, Any] | None,
    ) -> DistributedAlarmFrontContext:
        return DistributedAlarmFrontContextBuilder.build(
            snapshot=latest_snapshot,
        )

    @staticmethod
    def _get_total_active_alarms(
        *,
        context: DistributedAlarmFrontContext,
    ) -> int:
        alarm_keys: set[str] = set()

        for item in context.default_operator_view:
            unique_key = _build_alarm_unique_key(item=item)

            if unique_key:
                alarm_keys.add(unique_key)

        for group in context.distributed_groups:
            for item in group.items:
                unique_key = _build_alarm_unique_key(item=item)

                if unique_key:
                    alarm_keys.add(unique_key)

        for item in context.inactive_reactivation_view:
            unique_key = _build_alarm_unique_key(item=item)

            if unique_key:
                alarm_keys.add(unique_key)

        return len(alarm_keys)

    @staticmethod
    def _get_total_tracking_alarms(
        *,
        context: DistributedAlarmFrontContext,
    ) -> int:
        meta_value = context.meta.get('tracking_count')

        if meta_value is not None:
            return _to_int(
                value=meta_value,
                default=0,
            )

        return len(context.tracking_view)


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
    item: Any,
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
