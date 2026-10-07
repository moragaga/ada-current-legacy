from __future__ import annotations

from datetime import datetime
from typing import Any
from uuid import uuid4

from src.features.alarm_management.domain import SILENCE_POLICY_NONE

from ..models.alarm_management_action import AlarmManagementAction
from ..models.alarm_management_alarm import AlarmManagementAlarm
from ..models.alarm_management_request import AlarmManagementRequest
from ..models.alarm_management_result import AlarmManagementResult
from ..models.alarm_management_user import AlarmManagementUser
from .alarm_configuration_resolver import AlarmConfigurationResolver
from .alarm_management_message_resolver import AlarmManagementMessageResolver
from .alarm_management_policy_service import AlarmManagementPolicyService
from .alarm_runtime_snapshot_resolver import AlarmRuntimeSnapshotResolver


class AlarmManagementActionBuilder:
    ACTION_PARTITION_KEY = 'alarm_management_actions'

    def build_action(
        self,
        *,
        request: AlarmManagementRequest,
        user: AlarmManagementUser,
        runtime_snapshot: dict[str, Any],
        alarm_configuration_rows: list[dict[str, Any]],
        message_configuration: dict[str, Any],
        managed_alarm_ids: set[str],
        now_utc: datetime,
        shift_end_utc: datetime,
    ) -> AlarmManagementResult:
        if request.alarm_id in managed_alarm_ids:
            return AlarmManagementResult(
                status='exists',
                message='La alarma ya fue gestionada.',
            )

        runtime_alarm = AlarmRuntimeSnapshotResolver.find_active_alarm(
            snapshot=runtime_snapshot,
            alarm_id=request.alarm_id,
        )

        alarm_key = self._resolve_alarm_key(
            request=request,
            runtime_alarm=runtime_alarm,
        )

        if not alarm_key:
            return AlarmManagementResult(
                status='validation_error',
                message='No se pudo resolver la key técnica de la alarma.',
            )

        alarm_config = AlarmConfigurationResolver.find_by_alarm_key(
            alarm_configuration_rows=alarm_configuration_rows,
            alarm_key=alarm_key,
        )

        if alarm_config is None:
            return AlarmManagementResult(
                status='empty',
                message='No se encontró configuración para la alarma.',
            )

        resolved_runtime_alarm = runtime_alarm or self._build_stale_runtime_alarm(
            request=request,
            alarm_config=alarm_config,
        )

        alarm = AlarmManagementAlarm.from_runtime_and_config(
            runtime_alarm=resolved_runtime_alarm,
            alarm_config=alarm_config,
        )

        if not alarm.allow_management:
            return AlarmManagementResult(
                status='management_disabled',
                message='La alarma no permite gestión.',
            )

        messages = AlarmManagementMessageResolver.resolve_messages(
            message_configuration=message_configuration,
            message_group_key=alarm.message_group_key,
        )

        selected_message = AlarmManagementMessageResolver.find_message_by_id(
            messages=messages,
            message_id=request.selected_message_id,
        )

        validation_error = self._validate_description_and_message(
            request=request,
            selected_message=selected_message,
        )

        if validation_error:
            return AlarmManagementResult(
                status='validation_error',
                message=validation_error,
            )

        try:
            effective_policy = self._resolve_effective_policy(
                request=request,
                alarm=alarm,
                selected_message=selected_message,
            )

            if request.silence_requested and effective_policy == SILENCE_POLICY_NONE:
                return AlarmManagementResult(
                    status='validation_error',
                    message='Debe seleccionar una política válida para desactivar la alarma.',
                )

            if request.silence_requested:
                policy_available = AlarmManagementPolicyService.is_policy_available(
                    policy_code=effective_policy,
                    now_utc=now_utc,
                    shift_end_utc=shift_end_utc,
                )

                if not policy_available:
                    return AlarmManagementResult(
                        status='validation_error',
                        message=(
                            'La duración seleccionada ya no está disponible. '
                            'Selecciona una opción válida.'
                        ),
                    )

            silence_until = None

            if request.silence_requested:
                silence_until = AlarmManagementPolicyService.calculate_silence_until(
                    effective_policy_code=effective_policy,
                    now_utc=now_utc,
                    shift_end_utc=shift_end_utc,
                )

        except Exception as error:
            return AlarmManagementResult(
                status='validation_error',
                message=str(error),
            )

        if not alarm.group_occurrence_id:
            return AlarmManagementResult(
                status='validation_error',
                message='No se pudo resolver la ocurrencia de grupo de la alarma.',
            )

        action_id = str(uuid4())

        action = AlarmManagementAction(
            id=action_id,
            partition_key=self.ACTION_PARTITION_KEY,
            action_id=action_id,
            requested_at=now_utc.isoformat(),
            requested_by_email=user.email,
            requested_by_name=user.name,
            source_snapshot_timestamp=AlarmRuntimeSnapshotResolver.get_snapshot_timestamp(
                snapshot=runtime_snapshot,
            ),
            alarm_id=alarm.alarm_id,
            group_occurrence_id=alarm.group_occurrence_id,
            alarm_key=alarm.alarm_key,
            alarm_name=alarm.alarm_name,
            alarm_display_name=alarm.alarm_display_name,
            visibility_group_key=alarm.visibility_group_key,
            management_scope_key=alarm.management_scope_key,
            operator_bucket=alarm.operator_bucket,
            priority_order=alarm.priority_order,
            modal_title=alarm.modal_title,
            title=alarm.title,
            cause=alarm.cause,
            color=alarm.color,
            predefined_message_id=(selected_message.message_id if selected_message else None),
            predefined_message=(selected_message.message if selected_message else ''),
            personalized_message=request.personalized_message.strip(),
            silence_requested=request.silence_requested,
            selected_silence_policy_code=request.selected_silence_policy_code,
            effective_silence_policy_code=effective_policy,
            silence_until=self._datetime_to_iso(silence_until),
            target_occurrence_started_at=self._resolve_target_occurrence_started_at(
                request=request,
                runtime_alarm=runtime_alarm,
                resolved_runtime_alarm=resolved_runtime_alarm,
            ),
            status='pending',
        )

        return AlarmManagementResult(
            status='success',
            action=action,
        )

    @staticmethod
    def _resolve_alarm_key(
        *,
        request: AlarmManagementRequest,
        runtime_alarm: dict[str, Any] | None,
    ) -> str:
        if runtime_alarm is not None:
            alarm_key = str(runtime_alarm.get('alarm_key') or '').strip()
            if alarm_key:
                return alarm_key

        return str(request.alarm_key or '').strip()

    @staticmethod
    def _build_stale_runtime_alarm(
        *,
        request: AlarmManagementRequest,
        alarm_config: dict[str, Any],
    ) -> dict[str, Any]:
        alarm_key = str(alarm_config.get('alarm_key') or request.alarm_key or '').strip()

        target_occurrence_started_at = str(request.target_occurrence_started_at or '').strip()

        return {
            'alarm_id': request.alarm_id,
            'group_occurrence_id': request.group_occurrence_id or '',
            'alarm_key': alarm_key,
            'alarm_name': alarm_key,
            'alarm_display_name': str(alarm_config.get('alarm_display_name') or alarm_key),
            'message_group_key': str(alarm_config.get('message_group_key') or ''),
            'visibility_group_key': str(
                request.visibility_group_key or alarm_config.get('visibility_group_key') or ''
            ),
            'management_scope_key': str(
                request.management_scope_key or alarm_config.get('management_scope_key') or ''
            ),
            'operator_bucket': str(alarm_config.get('operator_bucket') or 'default'),
            'priority_order': (
                request.priority_order
                if request.priority_order is not None
                else alarm_config.get('priority_order')
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
            'target_occurrence_started_at': target_occurrence_started_at,
            'start_timestamp': target_occurrence_started_at,
            'status': 'STALE',
        }

    @staticmethod
    def _validate_description_and_message(
        *,
        request: AlarmManagementRequest,
        selected_message,
    ) -> str | None:
        has_selected_message_id = bool(request.selected_message_id)
        has_selected_message = selected_message is not None
        has_personalized_message = bool(request.personalized_message.strip())

        if has_selected_message_id and not has_selected_message:
            return 'El mensaje predefinido seleccionado ya no está disponible.'

        if not has_selected_message and not has_personalized_message:
            return 'Debe seleccionar un mensaje predefinido o ingresar una descripción.'

        return None

    @staticmethod
    def _resolve_effective_policy(
        *,
        request: AlarmManagementRequest,
        alarm: AlarmManagementAlarm,
        selected_message,
    ) -> str:
        if not request.silence_requested:
            return SILENCE_POLICY_NONE

        if selected_message is not None:
            if not selected_message.allow_silence_edit:
                return AlarmManagementPolicyService.resolve_effective_policy(
                    policy_code=selected_message.silence_policy_code,
                    default_policy_code=alarm.default_silence_policy_code,
                )

            policy_code = (
                request.selected_silence_policy_code or selected_message.silence_policy_code
            )

            return AlarmManagementPolicyService.resolve_effective_policy(
                policy_code=policy_code,
                default_policy_code=alarm.default_silence_policy_code,
            )

        if not alarm.allow_manual_silence:
            raise ValueError('Esta alarma no permite silencio manual sin mensaje predefinido.')

        return AlarmManagementPolicyService.resolve_effective_policy(
            policy_code=request.selected_silence_policy_code,
            default_policy_code=alarm.default_silence_policy_code,
        )

    @staticmethod
    def _datetime_to_iso(value: datetime | None) -> str | None:
        if value is None:
            return None

        return value.isoformat()

    @staticmethod
    def _resolve_target_occurrence_started_at(
        *,
        request: AlarmManagementRequest,
        runtime_alarm: dict[str, Any] | None,
        resolved_runtime_alarm: dict[str, Any],
    ) -> str:
        candidates: list[Any] = []

        if runtime_alarm is not None:
            candidates.extend(
                [
                    runtime_alarm.get('target_occurrence_started_at'),
                    runtime_alarm.get('start_timestamp'),
                ]
            )

        candidates.extend(
            [
                resolved_runtime_alarm.get('target_occurrence_started_at'),
                resolved_runtime_alarm.get('start_timestamp'),
                request.target_occurrence_started_at,
            ]
        )

        for value in candidates:
            normalized_value = str(value or '').strip()

            if normalized_value:
                return normalized_value

        return ''
