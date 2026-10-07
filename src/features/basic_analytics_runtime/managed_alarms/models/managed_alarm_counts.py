from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from src.features.basic_analytics_runtime.managed_alarms.constants import (
    TURN_SCOPE_ALL,
    TURN_SCOPE_CURRENT,
    TURN_SCOPE_PREVIOUS,
)


@dataclass(frozen=True, slots=True)
class ManagedAlarmTurnCount:
    turn_scope_code: str
    turn_scope_label: str
    turn_group_code: str
    turn_group_label: str
    management_count: int

    @classmethod
    def from_payload(
        cls,
        payload: dict[str, Any] | None,
        *,
        fallback_scope_code: str,
        fallback_scope_label: str,
    ) -> ManagedAlarmTurnCount:
        payload = payload or {}

        return cls(
            turn_scope_code=_safe_str(payload.get('turn_scope_code')) or fallback_scope_code,
            turn_scope_label=_safe_str(payload.get('turn_scope_label')) or fallback_scope_label,
            turn_group_code=_safe_str(payload.get('turn_group_code')),
            turn_group_label=_safe_str(payload.get('turn_group_label')),
            management_count=_safe_int(payload.get('management_count')),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'turn_scope_code': self.turn_scope_code,
            'turn_scope_label': self.turn_scope_label,
            'turn_group_code': self.turn_group_code,
            'turn_group_label': self.turn_group_label,
            'management_count': self.management_count,
        }


@dataclass(frozen=True, slots=True)
class ManagedAlarmAnalyticsCounts:
    all: ManagedAlarmTurnCount
    current_turn: ManagedAlarmTurnCount
    previous_turn: ManagedAlarmTurnCount

    @classmethod
    def empty(cls) -> ManagedAlarmAnalyticsCounts:
        return cls(
            all=ManagedAlarmTurnCount(
                turn_scope_code=TURN_SCOPE_ALL,
                turn_scope_label='Todos',
                turn_group_code='',
                turn_group_label='',
                management_count=0,
            ),
            current_turn=ManagedAlarmTurnCount(
                turn_scope_code=TURN_SCOPE_CURRENT,
                turn_scope_label='Turno actual',
                turn_group_code='',
                turn_group_label='',
                management_count=0,
            ),
            previous_turn=ManagedAlarmTurnCount(
                turn_scope_code=TURN_SCOPE_PREVIOUS,
                turn_scope_label='Turno anterior',
                turn_group_code='',
                turn_group_label='',
                management_count=0,
            ),
        )

    @classmethod
    def from_payload(
        cls,
        payload: dict[str, Any] | None,
    ) -> ManagedAlarmAnalyticsCounts:
        if not isinstance(payload, dict):
            return cls.empty()

        return cls(
            all=ManagedAlarmTurnCount.from_payload(
                payload.get('all'),
                fallback_scope_code=TURN_SCOPE_ALL,
                fallback_scope_label='Todos',
            ),
            current_turn=ManagedAlarmTurnCount.from_payload(
                payload.get('current_turn'),
                fallback_scope_code=TURN_SCOPE_CURRENT,
                fallback_scope_label='Turno actual',
            ),
            previous_turn=ManagedAlarmTurnCount.from_payload(
                payload.get('previous_turn'),
                fallback_scope_code=TURN_SCOPE_PREVIOUS,
                fallback_scope_label='Turno anterior',
            ),
        )

    @property
    def current_turn_management_count(self) -> int:
        return self.current_turn.management_count

    def to_dict(self) -> dict[str, Any]:
        return {
            'all': self.all.to_dict(),
            'current_turn': self.current_turn.to_dict(),
            'previous_turn': self.previous_turn.to_dict(),
        }


def _safe_str(value: Any) -> str:
    if value is None:
        return ''

    return str(value).strip()


def _safe_int(value: Any) -> int:
    if value is None or value == '':
        return 0

    try:
        return int(float(value))
    except Exception:
        return 0
