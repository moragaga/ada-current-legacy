from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class ActiveAlarmModalItem:
    row_id: str
    source: str

    alarm_id: str
    alarm_key: str
    title: str
    modal_title: str
    alarm_kind: str
    severity_code: int
    severity_label: str
    alarm_kind: str

    severity_code: str
    severity_label: str

    start_timestamp: str | None
    start_display: str
    last_seen_display: str
    duration_display: str

    description: str
    cause: str
    technical_status: str
    status_label: str
    operator_bucket: str
    family: str

    view_bucket_code: str
    view_bucket_label: str
    operative_status: str
    is_inactivity_locked: bool
    management_enabled: bool
    management_disabled_reason: str

    raw: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            'row_id': self.row_id,
            'source': self.source,
            'alarm_id': self.alarm_id,
            'alarm_key': self.alarm_key,
            'title': self.title,
            'modal_title': self.modal_title,
            'alarm_kind': self.alarm_kind,
            'severity_code': self.severity_code,
            'severity_label': self.severity_label,
            'start_timestamp': self.start_timestamp,
            'start_display': self.start_display,
            'last_seen_display': self.last_seen_display,
            'duration_display': self.duration_display,
            'description': self.description,
            'cause': self.cause,
            'operative_status': self.operative_status,
            'status_label': self.status_label,
            'operator_bucket': self.operator_bucket,
            'family': self.family,
            'view_bucket_code': self.view_bucket_code,
            'view_bucket_label': self.view_bucket_label,
            'technical_status': self.technical_status,
            'is_inactivity_locked': self.is_inactivity_locked,
            'management_enabled': self.management_enabled,
            'management_disabled_reason': self.management_disabled_reason,
            'raw': self.raw,
        }
