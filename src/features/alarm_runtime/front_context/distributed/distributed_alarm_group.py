from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..models import AlarmFrontItem


@dataclass(frozen=True, slots=True)
class DistributedAlarmGroup:
    group_key: str
    group_label: str
    operator_bucket: str
    items: tuple[AlarmFrontItem, ...] = field(default_factory=tuple)
    icon_class_name: str = 'bi bi-collection'

    @property
    def count(self) -> int:
        return len(self.items)

    @property
    def representative_alarm(self) -> AlarmFrontItem | None:
        if not self.items:
            return None

        return self.items[0]

    def to_dict(self) -> dict[str, Any]:
        return {
            'group_key': self.group_key,
            'group_label': self.group_label,
            'operator_bucket': self.operator_bucket,
            'icon_class_name': self.icon_class_name,
            'count': self.count,
            'items': [item.to_dict() for item in self.items],
        }
