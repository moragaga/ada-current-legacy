from __future__ import annotations

from datetime import datetime
from typing import Any

from src.features.alarm_management.domain import SILENCE_POLICY_NONE

from ..models.alarm_management_alarm import AlarmManagementAlarm
from ..models.alarm_management_context import AlarmManagementContext
from ..models.alarm_management_context_result import AlarmManagementContextResult
from .alarm_management_action_builder import AlarmConfigurationResolver
from .alarm_management_message_resolver import AlarmManagementMessageResolver
from .alarm_management_policy_service import AlarmManagementPolicyService
from .alarm_runtime_snapshot_resolver import AlarmRuntimeSnapshotResolver


class AlarmManagementContextService:
    def build_context(
        self,
        *,
        alarm_id: str,
        alarm_key: str | None,
        group_occurrence_id: str | None,
        visibility_group_key: str | None,
        management_scope_key: str | None,
        priority_order: int | None,
        runtime_snapshot: dict[str, Any],
        alarm_configuration_rows: list[dict[str, Any]],
        message_configuration: dict[str, Any],
        managed_alarm_ids: set[str],
        now_utc: datetime,
        shift_end_utc: datetime,
    ) -> AlarmManagementContextResult:
        if alarm_id in managed_alarm_ids:
            return AlarmManagementContextResult(
                status='exists',
                message='La alarma ya fue gestionada.',
            )

        runtime_alarm = AlarmRuntimeSnapshotResolver.find_active_alarm(
            snapshot=runtime_snapshot,
            alarm_id=alarm_id,
        )

        resolved_alarm_key = self._resolve_alarm_key(
            alarm_key=alarm_key,
            runtime_alarm=runtime_alarm,
        )

        if not resolved_alarm_key:
            return AlarmManagementContextResult(
                status='empty',
                message='No se pudo resolver la key técnica de la alarma.',
            )

        alarm_config = AlarmConfigurationResolver.find_by_alarm_key(
            alarm_configuration_rows=alarm_configuration_rows,
            alarm_key=resolved_alarm_key,
        )

        if alarm_config is None:
            return AlarmManagementContextResult(
                status='empty',
                message='No se encontró configuración para la alarma.',
            )

        is_stale = runtime_alarm is None

        resolved_runtime_alarm = runtime_alarm or self._build_stale_runtime_alarm(
            alarm_id=alarm_id,
            alarm_key=resolved_alarm_key,
            group_occurrence_id=group_occurrence_id,
            visibility_group_key=visibility_group_key,
            management_scope_key=management_scope_key,
            priority_order=priority_order,
            alarm_config=alarm_config,
        )

        alarm = AlarmManagementAlarm.from_runtime_and_config(
            runtime_alarm=resolved_runtime_alarm,
            alarm_config=alarm_config,
        )

        if not alarm.allow_management:
            return AlarmManagementContextResult(
                status='management_disabled',
                message='La alarma no permite gestión.',
            )

        messages = AlarmManagementMessageResolver.resolve_messages(
            message_configuration=message_configuration,
            message_group_key=alarm.message_group_key,
        )

        context = AlarmManagementContext(
            snapshot_timestamp=AlarmRuntimeSnapshotResolver.get_snapshot_timestamp(
                snapshot=runtime_snapshot,
            ),
            alarm=alarm,
            messages=messages,
            silence_options=AlarmManagementPolicyService.build_silence_options(
                now_utc=now_utc,
                shift_end_utc=shift_end_utc,
            ),
            is_stale=is_stale,
        )

        return AlarmManagementContextResult(
            status='ready',
            context=context,
        )

    @staticmethod
    def _resolve_alarm_key(
        *,
        alarm_key: str | None,
        runtime_alarm: dict[str, Any] | None,
    ) -> str:
        if runtime_alarm is not None:
            runtime_alarm_key = str(runtime_alarm.get('alarm_key') or '').strip()

            if runtime_alarm_key:
                return runtime_alarm_key

        return str(alarm_key or '').strip()

    @staticmethod
    def _build_stale_runtime_alarm(
        *,
        alarm_id: str,
        alarm_key: str,
        group_occurrence_id: str | None,
        visibility_group_key: str | None,
        management_scope_key: str | None,
        priority_order: int | None,
        alarm_config: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            'alarm_id': str(alarm_id or '').strip(),
            'group_occurrence_id': str(group_occurrence_id or '').strip(),
            'alarm_key': str(alarm_key or '').strip(),
            'alarm_name': str(alarm_key or '').strip(),
            'alarm_display_name': str(alarm_config.get('alarm_display_name') or alarm_key),
            'message_group_key': str(alarm_config.get('message_group_key') or ''),
            'visibility_group_key': str(
                visibility_group_key or alarm_config.get('visibility_group_key') or ''
            ),
            'management_scope_key': str(
                management_scope_key or alarm_config.get('management_scope_key') or ''
            ),
            'operator_bucket': str(alarm_config.get('operator_bucket') or 'default'),
            'priority_order': (
                priority_order if priority_order is not None else alarm_config.get('priority_order')
            ),
            'modal_title': str(alarm_config.get('modal_title') or 'Gestión de alarma'),
            'alarm_kind': str(alarm_config.get('alarm_kind') or ''),
            'title': str(alarm_config.get('title') or ''),
            'cause': str(alarm_config.get('cause') or ''),
            'color': str(alarm_config.get('color') or 'yellow'),
            'default_silence_policy_code': str(
                alarm_config.get('default_silence_policy_code') or SILENCE_POLICY_NONE
            ),
            'allow_manual_silence': bool(alarm_config.get('allow_manual_silence', True)),
            'allow_management': bool(alarm_config.get('allow_management', True)),
            'status': 'STALE',
        }
