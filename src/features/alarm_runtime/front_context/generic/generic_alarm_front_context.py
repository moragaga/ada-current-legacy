from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..models import AlarmFrontItem


@dataclass(frozen=True, slots=True)
class GenericAlarmFrontContext:
    snapshot_timestamp: str
    operator_view: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    operator_pool: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    tracking_view: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    inactive_reactivation_view: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def visible_alarms(self) -> tuple[AlarmFrontItem, ...]:
        return self.operator_view

    @property
    def all_operator_alarms(self) -> tuple[AlarmFrontItem, ...]:
        return (
            *self.operator_view,
            *self.operator_pool,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'snapshot_timestamp': self.snapshot_timestamp,
            'operator_view': [item.to_dict() for item in self.operator_view],
            'operator_pool': [item.to_dict() for item in self.operator_pool],
            'tracking_view': [item.to_dict() for item in self.tracking_view],
            'inactive_reactivation_view': [
                item.to_dict() for item in self.inactive_reactivation_view
            ],
            'meta': self.meta,
        }
