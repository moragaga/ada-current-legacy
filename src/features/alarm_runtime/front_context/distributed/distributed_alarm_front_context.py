from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..models import AlarmFrontItem
from .distributed_alarm_group import DistributedAlarmGroup


@dataclass(frozen=True, slots=True)
class DistributedAlarmFrontContext:
    snapshot_timestamp: str
    default_operator_view: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    default_operator_pool: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    tracking_view: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    distributed_groups: tuple[DistributedAlarmGroup, ...] = field(default_factory=tuple)
    inactive_reactivation_view: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    meta: dict[str, Any] = field(default_factory=dict)

    @property
    def visible_default_alarms(self) -> tuple[AlarmFrontItem, ...]:
        return self.default_operator_view

    @property
    def all_default_operator_alarms(self) -> tuple[AlarmFrontItem, ...]:
        return (
            *self.default_operator_view,
            *self.default_operator_pool,
        )

    def get_group(
        self,
        *,
        group_key: str,
    ) -> DistributedAlarmGroup | None:
        target = str(group_key or '').strip()

        if not target:
            return None

        for group in self.distributed_groups:
            if group.group_key == target:
                return group

        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            'snapshot_timestamp': self.snapshot_timestamp,
            'default_operator_view': [item.to_dict() for item in self.default_operator_view],
            'default_operator_pool': [item.to_dict() for item in self.default_operator_pool],
            'tracking_view': [item.to_dict() for item in self.tracking_view],
            'distributed_groups': [group.to_dict() for group in self.distributed_groups],
            'inactive_reactivation_view': [
                item.to_dict() for item in self.inactive_reactivation_view
            ],
            'meta': self.meta,
        }
