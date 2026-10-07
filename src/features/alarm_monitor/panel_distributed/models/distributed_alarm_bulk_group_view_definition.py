from __future__ import annotations

from dataclasses import dataclass

from .distributed_alarm_card_view_definition import (
    DistributedAlarmCardViewDefinition,
)


@dataclass(frozen=True, slots=True)
class DistributedAlarmBulkGroupViewDefinition:
    key: str
    label: str
    count: int
    items: tuple[DistributedAlarmCardViewDefinition, ...]
    anchor_alarm_id: str
    icon_class_name: str = 'bi bi-collection'
