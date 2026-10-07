from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AlarmCardViewDefinition:
    alarm_id: str
    group_occurrence_id: str

    alarm_key: str
    alarm_name: str

    visibility_group_key: str
    management_scope_key: str
    message_group_key: str

    target_occurrence_started_at: str

    alarm_kind: str
    activity_time: str
    title: str
    cause_lines: tuple[str, ...]
    color: str
    modal_title: str

    ranking: int
    priority_order: int

    is_show_delete: bool
