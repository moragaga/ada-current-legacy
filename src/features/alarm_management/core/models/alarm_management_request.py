from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AlarmManagementRequest:
    alarm_id: str
    alarm_key: str | None = None

    group_occurrence_id: str | None = None
    visibility_group_key: str | None = None
    management_scope_key: str | None = None
    priority_order: int | None = None

    target_occurrence_started_at: str = ''

    selected_message_id: str | None = None
    personalized_message: str = ''

    silence_requested: bool = False
    selected_silence_policy_code: str | None = None
