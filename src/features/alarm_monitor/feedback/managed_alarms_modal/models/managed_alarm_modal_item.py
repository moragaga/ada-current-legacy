from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ManagedAlarmModalItem:
    row_id: str

    action_id: str
    alarm_id: str
    alarm_key: str
    group_occurrence_id: str

    turn_scope_code: str
    turn_scope_label: str
    turn_group_code: str
    turn_group_label: str
    is_current_turn: bool
    is_previous_turn: bool

    title: str
    alarm_display_name: str
    cause: str

    severity_code: str
    severity_label: str

    action_type: str
    management_status: str
    status_label: str
    alarm_status_label: str
    management_status_label: str

    requested_at: str | None
    requested_display: str

    occurrence_started_at: str | None
    occurrence_started_display: str

    expires_at: str | None
    expires_display: str

    time_to_management_seconds: int | None
    time_to_management_display: str

    requested_by_name: str
    requested_by_email: str

    predefined_message: str
    personalized_message: str
    message_display: str

    is_inactive_management: bool
    is_still_active: bool
    is_inactivity_active: bool

    detail: dict[str, Any]
    raw: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            'row_id': self.row_id,
            'action_id': self.action_id,
            'alarm_id': self.alarm_id,
            'alarm_key': self.alarm_key,
            'group_occurrence_id': self.group_occurrence_id,
            'turn_scope_code': self.turn_scope_code,
            'turn_scope_label': self.turn_scope_label,
            'turn_group_code': self.turn_group_code,
            'turn_group_label': self.turn_group_label,
            'is_current_turn': self.is_current_turn,
            'is_previous_turn': self.is_previous_turn,
            'title': self.title,
            'alarm_display_name': self.alarm_display_name,
            'cause': self.cause,
            'severity_code': self.severity_code,
            'severity_label': self.severity_label,
            'action_type': self.action_type,
            'management_status': self.management_status,
            'status_label': self.status_label,
            'alarm_status_label': self.alarm_status_label,
            'management_status_label': self.management_status_label,
            'requested_at': self.requested_at,
            'requested_display': self.requested_display,
            'occurrence_started_at': self.occurrence_started_at,
            'occurrence_started_display': self.occurrence_started_display,
            'expires_at': self.expires_at,
            'expires_display': self.expires_display,
            'time_to_management_seconds': self.time_to_management_seconds,
            'time_to_management_display': self.time_to_management_display,
            'requested_by_name': self.requested_by_name,
            'requested_by_email': self.requested_by_email,
            'predefined_message': self.predefined_message,
            'personalized_message': self.personalized_message,
            'message_display': self.message_display,
            'is_inactive_management': self.is_inactive_management,
            'is_still_active': self.is_still_active,
            'is_inactivity_active': self.is_inactivity_active,
            'detail': self.detail,
            'raw': self.raw,
        }
