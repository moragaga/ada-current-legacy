from __future__ import annotations

from ..models.alarm_card_view_definition import AlarmCardViewDefinition


def allocate_alarm_slots(
    *,
    alarms: list[AlarmCardViewDefinition],
    total_slots: int = 6,
) -> tuple[AlarmCardViewDefinition | None, ...]:
    slots: list[AlarmCardViewDefinition | None] = [None for _ in range(total_slots)]

    for index, alarm in enumerate(alarms[:total_slots]):
        slots[index] = alarm

    return tuple(slots)
