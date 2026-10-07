from __future__ import annotations

from ..models.distributed_alarm_card_view_definition import (
    DistributedAlarmCardViewDefinition,
)


def allocate_distributed_alarm_slots(
    *,
    normal_alarms: list[DistributedAlarmCardViewDefinition],
    bulk_group_alarm: DistributedAlarmCardViewDefinition | None,
    total_slots: int = 6,
) -> tuple[DistributedAlarmCardViewDefinition | None, ...]:
    if total_slots <= 0:
        return tuple()

    slots: list[DistributedAlarmCardViewDefinition | None] = [None for _ in range(total_slots)]

    if bulk_group_alarm is None:
        for index, alarm in enumerate(normal_alarms[:total_slots]):
            slots[index] = alarm

        return tuple(slots)

    normal_capacity = max(total_slots - 1, 0)
    bulk_alarm_id = str(bulk_group_alarm.alarm_id or '').strip()

    filtered_normal_alarms = [
        alarm for alarm in normal_alarms if str(alarm.alarm_id or '').strip() != bulk_alarm_id
    ]

    for index, alarm in enumerate(filtered_normal_alarms[:normal_capacity]):
        slots[index] = alarm

    slots[total_slots - 1] = bulk_group_alarm

    return tuple(slots)
