from __future__ import annotations

from dataclasses import dataclass

from .distributed_alarm_bulk_group_view_definition import (
    DistributedAlarmBulkGroupViewDefinition,
)
from .distributed_alarm_card_view_definition import (
    DistributedAlarmCardViewDefinition,
)


@dataclass(frozen=True, slots=True)
class DistributedAlarmPanelViewDefinition:
    slots: tuple[DistributedAlarmCardViewDefinition | None, ...]
    is_management_user: bool = False
    bulk_group: DistributedAlarmBulkGroupViewDefinition | None = None


def build_empty_distributed_alarm_panel_view_definition() -> DistributedAlarmPanelViewDefinition:
    return DistributedAlarmPanelViewDefinition(
        slots=(None, None, None, None, None, None),
        is_management_user=False,
        bulk_group=None,
    )
