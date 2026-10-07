from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .alarm_management_alarm import AlarmManagementAlarm


@dataclass(frozen=True)
class AlarmManagementContext:
    snapshot_timestamp: str | None
    alarm: AlarmManagementAlarm
    messages: tuple[Any, ...] = field(default_factory=tuple)
    silence_options: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    is_stale: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            'snapshot_timestamp': self.snapshot_timestamp,
            'is_stale': self.is_stale,
            'alarm': self.alarm.to_dict(),
            'alarm_id': self.alarm.alarm_id,
            'group_occurrence_id': self.alarm.group_occurrence_id,
            'alarm_key': self.alarm.alarm_key,
            'alarm_name': self.alarm.alarm_name,
            'alarm_display_name': self.alarm.alarm_display_name,
            'target_occurrence_started_at': self.alarm.target_occurrence_started_at,
            'visibility_group_key': self.alarm.visibility_group_key,
            'management_scope_key': self.alarm.management_scope_key,
            'operator_bucket': self.alarm.operator_bucket,
            'priority_order': self.alarm.priority_order,
            'modal_title': self.alarm.modal_title,
            'title': self.alarm.title,
            'cause': self.alarm.cause,
            'color': self.alarm.color,
            'message_group_key': self.alarm.message_group_key,
            'default_silence_policy_code': self.alarm.default_silence_policy_code,
            'allow_manual_silence': self.alarm.allow_manual_silence,
            'allow_management': self.alarm.allow_management,
            'message_options': [
                message.to_option()
                if hasattr(message, 'to_option')
                else message.to_dict()
                if hasattr(message, 'to_dict')
                else {
                    'label': str(message),
                    'value': str(message),
                }
                for message in self.messages
            ],
            'silence_options': list(self.silence_options),
        }
