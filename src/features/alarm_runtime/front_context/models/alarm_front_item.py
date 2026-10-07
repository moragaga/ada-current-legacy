from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class AlarmFrontItem:
    alarm_id: str
    group_occurrence_id: str

    alarm_key: str
    alarm_name: str

    visibility_group_key: str
    management_scope_key: str
    message_group_key: str

    priority_order: int
    alarm_kind: str
    parameters_json: str

    start_timestamp: str
    last_seen_at: str
    duration: int

    status: str
    ranking: int
    operator_bucket: str
    bucket_count: int

    family: str
    modal_title: str
    title: str
    cause: str
    color: str

    source_view: str

    @classmethod
    def from_dict(
        cls,
        *,
        data: dict[str, Any],
        source_view: str,
    ) -> 'AlarmFrontItem':
        return cls(
            alarm_id=cls._text(data.get('alarm_id')),
            group_occurrence_id=cls._text(data.get('group_occurrence_id')),
            alarm_key=cls._text(data.get('alarm_key')),
            alarm_name=cls._text(data.get('alarm_name')),
            visibility_group_key=cls._text(data.get('visibility_group_key')),
            management_scope_key=cls._text(data.get('management_scope_key')),
            message_group_key=cls._text(data.get('message_group_key')),
            priority_order=cls._int(data.get('priority_order'), default=999999),
            alarm_kind=cls._text(data.get('alarm_kind')),
            parameters_json=cls._text(data.get('parameters_json')),
            start_timestamp=cls._text(data.get('start_timestamp')),
            last_seen_at=cls._text(data.get('last_seen_at')),
            duration=cls._int(data.get('duration'), default=0),
            status=cls._text(data.get('status')),
            ranking=cls._int(data.get('ranking'), default=999999),
            operator_bucket=cls._text(data.get('operator_bucket')) or 'default',
            bucket_count=cls._int(data.get('bucket_count'), default=0),
            family=cls._text(data.get('family')),
            modal_title=cls._text(data.get('modal_title')),
            title=cls._text(data.get('title')),
            cause=cls._text(data.get('cause')),
            color=cls._text(data.get('color')),
            source_view=source_view,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'alarm_id': self.alarm_id,
            'group_occurrence_id': self.group_occurrence_id,
            'alarm_key': self.alarm_key,
            'alarm_name': self.alarm_name,
            'visibility_group_key': self.visibility_group_key,
            'management_scope_key': self.management_scope_key,
            'message_group_key': self.message_group_key,
            'priority_order': self.priority_order,
            'alarm_kind': self.alarm_kind,
            'parameters_json': self.parameters_json,
            'start_timestamp': self.start_timestamp,
            'last_seen_at': self.last_seen_at,
            'duration': self.duration,
            'status': self.status,
            'ranking': self.ranking,
            'operator_bucket': self.operator_bucket,
            'bucket_count': self.bucket_count,
            'family': self.family,
            'modal_title': self.modal_title,
            'title': self.title,
            'cause': self.cause,
            'color': self.color,
            'source_view': self.source_view,
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
