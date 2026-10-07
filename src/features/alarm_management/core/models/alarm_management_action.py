from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AlarmManagementAction:
    id: str
    partition_key: str
    action_id: str

    requested_at: str
    requested_by_email: str
    requested_by_name: str

    source_snapshot_timestamp: str | None

    alarm_id: str
    group_occurrence_id: str
    alarm_key: str
    alarm_name: str
    alarm_display_name: str

    visibility_group_key: str
    management_scope_key: str
    operator_bucket: str
    priority_order: int

    modal_title: str
    title: str
    cause: str
    color: str

    predefined_message_id: str | None
    predefined_message: str
    personalized_message: str

    silence_requested: bool
    selected_silence_policy_code: str | None
    effective_silence_policy_code: str
    silence_until: str | None

    target_occurrence_started_at: str = ''

    status: str = 'pending'
    processing_result: str | None = None
    processing_message: str | None = None
    processing_error: str | None = None
    processed_at: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            'id': self.id,
            'partition_key': self.partition_key,
            'action_id': self.action_id,
            'requested_at': self.requested_at,
            'requested_by_email': self.requested_by_email,
            'requested_by_name': self.requested_by_name,
            'source_snapshot_timestamp': self.source_snapshot_timestamp,
            'alarm_id': self.alarm_id,
            'group_occurrence_id': self.group_occurrence_id,
            'alarm_key': self.alarm_key,
            'alarm_name': self.alarm_name,
            'alarm_display_name': self.alarm_display_name,
            'visibility_group_key': self.visibility_group_key,
            'management_scope_key': self.management_scope_key,
            'operator_bucket': self.operator_bucket,
            'priority_order': self.priority_order,
            'modal_title': self.modal_title,
            'title': self.title,
            'cause': self.cause,
            'color': self.color,
            'predefined_message_id': self.predefined_message_id,
            'predefined_message': self.predefined_message,
            'personalized_message': self.personalized_message,
            'silence_requested': self.silence_requested,
            'selected_silence_policy_code': self.selected_silence_policy_code,
            'effective_silence_policy_code': self.effective_silence_policy_code,
            'silence_until': self.silence_until,
            'target_occurrence_started_at': self.target_occurrence_started_at,
            'status': self.status,
            'processing_result': self.processing_result,
            'processing_message': self.processing_message,
            'processing_error': self.processing_error,
            'processed_at': self.processed_at,
        }
