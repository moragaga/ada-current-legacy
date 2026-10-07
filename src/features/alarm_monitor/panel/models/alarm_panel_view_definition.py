from __future__ import annotations

from dataclasses import dataclass

from .alarm_card_view_definition import AlarmCardViewDefinition


@dataclass(frozen=True, slots=True)
class AlarmPanelViewDefinition:
    slots: tuple[AlarmCardViewDefinition | None, ...]
    is_management_user: bool = False


def build_empty_alarm_panel_view_definition() -> AlarmPanelViewDefinition:
    return AlarmPanelViewDefinition(
        slots=(None, None, None, None, None, None),
        is_management_user=False,
    )
