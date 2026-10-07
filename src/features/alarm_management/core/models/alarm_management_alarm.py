from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.features.alarm_management.domain import SILENCE_POLICY_NONE


@dataclass(frozen=True)
class AlarmManagementAlarm:
    alarm_id: str
    group_occurrence_id: str

    alarm_key: str
    alarm_name: str
    alarm_display_name: str

    message_group_key: str
    visibility_group_key: str
    management_scope_key: str
    operator_bucket: str

    priority_order: int
    modal_title: str
    alarm_kind: str
    title: str
    cause: str
    color: str

    default_silence_policy_code: str
    allow_manual_silence: bool
    allow_management: bool

    target_occurrence_started_at: str = ''

    @classmethod
    def from_runtime_and_config(
        cls,
        *,
        runtime_alarm: dict[str, Any],
        alarm_config: dict[str, Any],
    ) -> 'AlarmManagementAlarm':
        alarm_key = cls._text(runtime_alarm.get('alarm_key') or alarm_config.get('alarm_key'))

        return cls(
            alarm_id=cls._text(runtime_alarm.get('alarm_id')),
            group_occurrence_id=cls._text(runtime_alarm.get('group_occurrence_id')),
            alarm_key=alarm_key,
            alarm_name=cls._text(runtime_alarm.get('alarm_name') or alarm_key),
            alarm_display_name=cls._text(
                runtime_alarm.get('alarm_display_name')
                or alarm_config.get('alarm_display_name')
                or alarm_key
            ),
            message_group_key=cls._text(
                runtime_alarm.get('message_group_key') or alarm_config.get('message_group_key')
            ),
            visibility_group_key=cls._text(
                runtime_alarm.get('visibility_group_key')
                or alarm_config.get('visibility_group_key')
            ),
            management_scope_key=cls._text(
                runtime_alarm.get('management_scope_key')
                or alarm_config.get('management_scope_key')
            ),
            operator_bucket=cls._text(
                runtime_alarm.get('operator_bucket')
                or alarm_config.get('operator_bucket')
                or 'default'
            ),
            priority_order=cls._int(
                runtime_alarm.get('priority_order'),
                default=cls._int(
                    alarm_config.get('priority_order'),
                    default=999999,
                ),
            ),
            modal_title=cls._text(
                runtime_alarm.get('modal_title')
                or alarm_config.get('modal_title')
                or 'Gestión de alarma'
            ),
            alarm_kind=cls._text(runtime_alarm.get('alarm_kind') or alarm_config.get('alarm_kind')),
            title=cls._text(runtime_alarm.get('title') or alarm_config.get('title')),
            cause=cls._text(
                runtime_alarm.get('cause')
                or runtime_alarm.get('cause_template')
                or alarm_config.get('cause')
                or alarm_config.get('cause_template')
            ),
            color=cls._text(runtime_alarm.get('color') or alarm_config.get('color') or 'yellow'),
            default_silence_policy_code=cls._text(
                runtime_alarm.get('default_silence_policy_code')
                or alarm_config.get('default_silence_policy_code')
                or SILENCE_POLICY_NONE
            ),
            allow_manual_silence=cls._bool(
                runtime_alarm.get(
                    'allow_manual_silence',
                    alarm_config.get('allow_manual_silence', True),
                )
            ),
            allow_management=cls._bool(
                runtime_alarm.get(
                    'allow_management',
                    alarm_config.get('allow_management', True),
                )
            ),
            target_occurrence_started_at=cls._text(
                runtime_alarm.get('target_occurrence_started_at')
                or runtime_alarm.get('start_timestamp')
            ),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'alarm_id': self.alarm_id,
            'group_occurrence_id': self.group_occurrence_id,
            'alarm_key': self.alarm_key,
            'alarm_name': self.alarm_name,
            'alarm_display_name': self.alarm_display_name,
            'message_group_key': self.message_group_key,
            'visibility_group_key': self.visibility_group_key,
            'management_scope_key': self.management_scope_key,
            'operator_bucket': self.operator_bucket,
            'priority_order': self.priority_order,
            'modal_title': self.modal_title,
            'alarm_kind': self.alarm_kind,
            'title': self.title,
            'cause': self.cause,
            'color': self.color,
            'default_silence_policy_code': self.default_silence_policy_code,
            'allow_manual_silence': self.allow_manual_silence,
            'allow_management': self.allow_management,
            'target_occurrence_started_at': self.target_occurrence_started_at,
        }

    @staticmethod
    def _text(value: Any) -> str:
        if value is None:
            return ''

        return str(value).strip()

    @staticmethod
    def _int(
        value: Any,
        *,
        default: int,
    ) -> int:
        if value is None or value == '':
            return default

        try:
            return int(float(value))
        except Exception:
            return default

    @staticmethod
    def _bool(value: Any) -> bool:
        if isinstance(value, bool):
            return value

        if value is None:
            return False

        if isinstance(value, str):
            return value.strip().lower() in {'true', '1', 'yes', 'si', 'sí'}

        return bool(value)
