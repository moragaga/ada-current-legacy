from __future__ import annotations

from typing import Any

DISTRIBUTED_ALARM_MANAGEMENT_OPERATOR_KEY = 'distributed-alarm-management-operator'

DISTRIBUTED_ALARM_MANAGEMENT_OPEN_BUTTON_TYPE = 'distributed-alarm-management-open-button'

DISTRIBUTED_ALARM_BULK_MANAGEMENT_OPEN_BUTTON_TYPE = 'distributed-alarm-management-bulk-open-button'

DISTRIBUTED_ALARM_BULK_MANAGEMENT_SOURCE_STORE_TYPE = (
    'distributed-alarm-management-bulk-source-store'
)


def build_distributed_alarm_management_open_button_id(
    *,
    alarm_id: str,
    group_occurrence_id: str,
    alarm_key: str,
    visibility_group_key: str,
    management_scope_key: str,
    priority_order: int | str,
    target_occurrence_started_at: str = '',
) -> dict[str, str]:
    return {
        'type': DISTRIBUTED_ALARM_MANAGEMENT_OPEN_BUTTON_TYPE,
        'alarm_id': str(alarm_id),
        'group_occurrence_id': str(group_occurrence_id),
        'alarm_key': str(alarm_key),
        'visibility_group_key': str(visibility_group_key),
        'management_scope_key': str(management_scope_key),
        'priority_order': str(priority_order),
        'target_occurrence_started_at': str(target_occurrence_started_at or ''),
    }


def build_distributed_alarm_bulk_management_open_button_id(
    *,
    group_key: str,
) -> dict[str, str]:
    return {
        'type': DISTRIBUTED_ALARM_BULK_MANAGEMENT_OPEN_BUTTON_TYPE,
        'group_key': group_key,
    }


def build_distributed_alarm_bulk_management_source_store_id(
    *,
    group_key: str,
) -> dict[str, str]:
    return {
        'type': DISTRIBUTED_ALARM_BULK_MANAGEMENT_SOURCE_STORE_TYPE,
        'group_key': group_key,
    }


def build_distributed_alarm_management_operator_ids() -> dict[str, str]:
    base = DISTRIBUTED_ALARM_MANAGEMENT_OPERATOR_KEY

    return {
        'context_store': f'{base}-context-store',
        'feedback_store': f'{base}-feedback-store',
        'validation_attempt_store': f'{base}-validation-attempt-store',
        'bulk_context_store': f'{base}-bulk-context-store',
        'bulk_validation_attempt_store': f'{base}-bulk-validation-attempt-store',
        'modal': f'{base}-modal',
        'modal_close_button': f'{base}-modal-close-button',
        'modal_cancel_button': f'{base}-modal-cancel-button',
        'modal_save_button': f'{base}-modal-save-button',
        'modal_title': f'{base}-modal-title',
        'alarm_title': f'{base}-alarm-title',
        'alarm_cause': f'{base}-alarm-cause',
        'alarm_warning': f'{base}-alarm-warning',
        'message_dropdown': f'{base}-message-dropdown',
        'message_validation': f'{base}-message-validation',
        'personalized_message': f'{base}-personalized-message',
        'personalized_message_validation': f'{base}-personalized-message-validation',
        'silence_checkbox': f'{base}-silence-checkbox',
        'silence_container': f'{base}-silence-container',
        'silence_dropdown': f'{base}-silence-dropdown',
        'silence_validation': f'{base}-silence-validation',
        'silence_information': f'{base}-silence-information',
        'bulk_modal': f'{base}-bulk-modal',
        'bulk_modal_close_button': f'{base}-bulk-modal-close-button',
        'bulk_modal_cancel_button': f'{base}-bulk-modal-cancel-button',
        'bulk_modal_save_button': f'{base}-bulk-modal-save-button',
        'bulk_title': f'{base}-bulk-title',
        'bulk_summary': f'{base}-bulk-summary',
        'bulk_alarm_list': f'{base}-bulk-alarm-list',
        'bulk_alarm_list_button': f'{base}-bulk-alarm-list-button',
        'bulk_alarm_list_collapse': f'{base}-bulk-alarm-list-collapse',
        'bulk_message_dropdown': f'{base}-bulk-message-dropdown',
        'bulk_message_validation': f'{base}-bulk-message-validation',
        'bulk_personalized_message': f'{base}-bulk-personalized-message',
        'bulk_personalized_message_validation': f'{base}-bulk-personalized-message-validation',
        'bulk_silence_checkbox': f'{base}-bulk-silence-checkbox',
        'bulk_silence_container': f'{base}-bulk-silence-container',
        'bulk_silence_dropdown': f'{base}-bulk-silence-dropdown',
        'bulk_silence_validation': f'{base}-bulk-silence-validation',
        'bulk_silence_information': f'{base}-bulk-silence-information',
        'feedback_modal': f'{base}-feedback-modal',
        'feedback_modal_close_button': f'{base}-feedback-modal-close-button',
        'feedback_modal_footer_close_button': f'{base}-feedback-modal-footer-close-button',
        'feedback_title': f'{base}-feedback-title',
        'feedback_message': f'{base}-feedback-message',
    }


def get_distributed_alarm_open_payload_from_trigger(
    *,
    triggered_id: Any,
) -> dict[str, Any] | None:
    if not isinstance(triggered_id, dict):
        return None

    if triggered_id.get('type') != DISTRIBUTED_ALARM_MANAGEMENT_OPEN_BUTTON_TYPE:
        return None

    alarm_id = _text(triggered_id.get('alarm_id'))
    group_occurrence_id = _text(triggered_id.get('group_occurrence_id'))
    alarm_key = _text(triggered_id.get('alarm_key'))
    visibility_group_key = _text(triggered_id.get('visibility_group_key'))
    management_scope_key = _text(triggered_id.get('management_scope_key'))
    target_occurrence_started_at = _text(triggered_id.get('target_occurrence_started_at'))
    priority_order = _optional_int(triggered_id.get('priority_order'))

    if (
        not alarm_id
        or not group_occurrence_id
        or not alarm_key
        or not visibility_group_key
        or not management_scope_key
        or priority_order is None
    ):
        return None

    return {
        'alarm_id': alarm_id,
        'group_occurrence_id': group_occurrence_id,
        'alarm_key': alarm_key,
        'visibility_group_key': visibility_group_key,
        'management_scope_key': management_scope_key,
        'priority_order': priority_order,
        'target_occurrence_started_at': target_occurrence_started_at,
    }


def get_distributed_alarm_bulk_open_payload_from_trigger(
    *,
    triggered_id: Any,
) -> dict[str, str] | None:
    if not isinstance(triggered_id, dict):
        return None

    if triggered_id.get('type') != DISTRIBUTED_ALARM_BULK_MANAGEMENT_OPEN_BUTTON_TYPE:
        return None

    group_key = _text(triggered_id.get('group_key'))

    if not group_key:
        return None

    return {
        'group_key': group_key,
    }


def _text(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


def _optional_int(value: Any) -> int | None:
    if value is None or value == '':
        return None

    try:
        return int(float(value))
    except Exception:
        return None
