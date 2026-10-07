from __future__ import annotations

from dash import html

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import (
    DistributedAlarmPanelIds,
)


def build_distributed_alarm_panel():
    return build_slot_container(
        component_id=DistributedAlarmPanelIds.ALARM_PANEL,
        class_name='alarm-panel-wrapper w-100',
    )


def build_distributed_alarm_panel_ready_flag() -> html.Div:
    return build_slot_ready_flag_container(id_flag=DistributedAlarmPanelIds.READY_FLAG)
