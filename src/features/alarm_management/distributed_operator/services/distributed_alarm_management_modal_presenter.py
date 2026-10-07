from __future__ import annotations

from typing import Any

from src.features.alarm_management.core.models import (
    AlarmManagementContext,
    AlarmManagementContextResult,
    AlarmManagementResult,
)
from src.features.alarm_management.domain import (
    SILENCE_POLICY_INHERIT,
    SILENCE_POLICY_NONE,
)

from ..models.distributed_alarm_management_modal_view_model import (
    DistributedAlarmManagementFeedbackViewModel,
    DistributedAlarmManagementModalPresentation,
    DistributedAlarmManagementModalViewModel,
)


class DistributedAlarmManagementModalPresenter:
    _FEEDBACK_BY_STATUS = {
        'success': {
            'kind': 'success',
            'title': 'Información',
            'message': 'La alarma se gestionó correctamente.',
        },
        'empty': {
            'kind': 'empty',
            'title': 'Información',
            'message': 'La alarma dejó de estar activa.',
        },
        'exists': {
            'kind': 'exists',
            'title': 'Información',
            'message': 'La alarma ya fue gestionada.',
        },
        'management_disabled': {
            'kind': 'management_disabled',
            'title': 'Información',
            'message': 'La alarma no permite gestión.',
        },
        'validation_error': {
            'kind': 'validation_error',
            'title': 'Validación',
            'message': 'La información ingresada no es válida.',
        },
        'error': {
            'kind': 'error',
            'title': 'Error',
            'message': 'Ocurrió un error inesperado al gestionar la alarma.',
        },
    }

    @classmethod
    def present_context_result(
        cls,
        *,
        result: AlarmManagementContextResult,
    ) -> DistributedAlarmManagementModalPresentation:
        if result.is_ready and result.context is not None:
            return DistributedAlarmManagementModalPresentation(
                modal=cls._build_ready_modal(context=result.context),
                feedback=DistributedAlarmManagementFeedbackViewModel.closed(),
            )

        return DistributedAlarmManagementModalPresentation(
            modal=DistributedAlarmManagementModalViewModel.closed(),
            feedback=cls._build_feedback(
                status=result.status,
                message=result.message,
                fallback_status='error',
            ),
        )

    @classmethod
    def present_command_result(
        cls,
        *,
        result: AlarmManagementResult,
    ) -> DistributedAlarmManagementFeedbackViewModel:
        return cls._build_feedback(
            status=result.status,
            message=result.message,
            fallback_status='error',
        )

    @classmethod
    def _build_ready_modal(
        cls,
        *,
        context: AlarmManagementContext,
    ) -> DistributedAlarmManagementModalViewModel:
        context_data = context.to_dict()
        alarm = context.alarm

        messages_by_id = cls._build_messages_by_id(
            messages=context.messages,
        )

        silence_options = list(context.silence_options)

        has_message_silence_authorization = cls._has_message_silence_authorization(
            messages_by_id=messages_by_id,
        )

        silence_disabled = not silence_options or (
            not alarm.allow_manual_silence and not has_message_silence_authorization
        )

        warning_message = None
        warning_class_name = 'd-none'

        if context.is_stale:
            warning_message = (
                'La alarma ya no aparece en la vista actual. '
                'Puedes registrar la gestión; el backend validará si corresponde '
                'a una ocurrencia cerrada recientemente o a una vista antigua.'
            )
            warning_class_name = 'alert alert-warning py-2 px-3 mb-3'

        return DistributedAlarmManagementModalViewModel(
            is_open=True,
            context_data=context_data,
            alarm_id=alarm.alarm_id,
            group_occurrence_id=alarm.group_occurrence_id,
            alarm_key=alarm.alarm_key,
            visibility_group_key=alarm.visibility_group_key,
            management_scope_key=alarm.management_scope_key,
            priority_order=alarm.priority_order,
            operator_bucket=alarm.operator_bucket,
            target_occurrence_started_at=cls._resolve_target_occurrence_started_at(
                alarm=alarm,
                context_data=context_data,
            ),
            modal_title=alarm.modal_title or 'Gestión de alarma',
            alarm_title=alarm.alarm_display_name or alarm.title or alarm.alarm_key,
            alarm_cause=alarm.cause,
            alarm_color=alarm.color or 'yellow',
            warning_message=warning_message,
            warning_class_name=warning_class_name,
            message_options=context_data.get('message_options') or [],
            messages_by_id=messages_by_id,
            silence_options=silence_options,
            silence_disabled=silence_disabled,
            silence_container_class_name='d-none',
            silence_information=cls._build_silence_information(
                allow_manual_silence=alarm.allow_manual_silence,
                has_message_silence_authorization=has_message_silence_authorization,
                has_silence_options=bool(silence_options),
                default_silence_policy_code=alarm.default_silence_policy_code,
            ),
            selected_message_id=None,
            personalized_message='',
            silence_requested=False,
            selected_silence_policy_code=None,
        )

    @classmethod
    def _build_feedback(
        cls,
        *,
        status: str,
        message: str | None,
        fallback_status: str,
    ) -> DistributedAlarmManagementFeedbackViewModel:
        feedback = cls._FEEDBACK_BY_STATUS.get(
            status,
            cls._FEEDBACK_BY_STATUS[fallback_status],
        )

        return DistributedAlarmManagementFeedbackViewModel(
            is_open=True,
            kind=feedback['kind'],
            title=feedback['title'],
            message=message or feedback['message'],
        )

    @staticmethod
    def _build_messages_by_id(
        *,
        messages: tuple[Any, ...],
    ) -> dict[str, dict[str, Any]]:
        result: dict[str, dict[str, Any]] = {}

        for message in messages:
            message_id = str(getattr(message, 'message_id', '') or '').strip()

            if not message_id:
                continue

            if hasattr(message, 'to_dict'):
                result[message_id] = message.to_dict()
            else:
                result[message_id] = {
                    'message_id': message_id,
                    'message': str(getattr(message, 'message', '') or ''),
                    'allow_silence_edit': True,
                    'silence_policy_code': SILENCE_POLICY_INHERIT,
                }

        return result

    @classmethod
    def _has_message_silence_authorization(
        cls,
        *,
        messages_by_id: dict[str, dict[str, Any]],
    ) -> bool:
        for message in messages_by_id.values():
            policy_code = cls._get_message_policy_code(message=message)

            if policy_code not in {
                '',
                SILENCE_POLICY_INHERIT,
                SILENCE_POLICY_NONE,
            }:
                return True

        return False

    @staticmethod
    def _get_message_policy_code(
        *,
        message: dict[str, Any],
    ) -> str:
        return str(message.get('silence_policy_code') or '').strip().lower()

    @staticmethod
    def _build_silence_information(
        *,
        allow_manual_silence: bool,
        has_message_silence_authorization: bool,
        has_silence_options: bool,
        default_silence_policy_code: str,
    ) -> str:
        if not has_silence_options:
            return 'No existen opciones disponibles para desactivar la alarma.'

        if allow_manual_silence:
            if default_silence_policy_code == SILENCE_POLICY_NONE:
                return 'No es obligatorio desactivar la alarma.'

            return 'La alarma puede desactivarse según la política seleccionada.'

        if has_message_silence_authorization:
            return (
                'Esta alarma no permite desactivación libre. '
                'Selecciona un mensaje predefinido autorizado para desactivarla.'
            )

        return 'Esta alarma no permite desactivación manual.'

    @staticmethod
    def _resolve_target_occurrence_started_at(
        *,
        alarm: Any,
        context_data: dict[str, Any],
    ) -> str:
        candidates = (
            getattr(alarm, 'target_occurrence_started_at', None),
            getattr(alarm, 'start_timestamp', None),
            context_data.get('target_occurrence_started_at'),
            context_data.get('start_timestamp'),
        )

        for value in candidates:
            normalized_value = str(value or '').strip()

            if normalized_value:
                return normalized_value

        return ''
