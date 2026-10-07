from __future__ import annotations

from src.shared.ui.app_time_status_shell.app_time_status_shell import build_app_time_status_shell
from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import HeaderIds


def build_global_indicator_container():
    return build_slot_container(component_id=HeaderIds.GLOBAL_INDICATOR, class_name='')

def build_information_container():
    return build_slot_container(component_id=HeaderIds.INFORMATION, class_name='w-100 h-100 background-secondary disabled')

def build_alarm_notifications_container():
    return build_slot_container(component_id=HeaderIds.ALARM_NOTIFICATIONS, class_name='w-100 h-100')

def build_time_status_container():
    return build_app_time_status_shell()

def build_header_ready_flag():
    return build_slot_ready_flag_container(id_flag=HeaderIds.READY_FLAG_HEADER)

def build_header_alarm_notifications_ready_flag():
    return build_slot_ready_flag_container(id_flag=HeaderIds.READY_FLAG_ALARM_NOTIFICATIONS)

def build_header_time_status_ready_flag():
    return build_slot_ready_flag_container(id_flag=HeaderIds.READY_FLAG_TIME_STATUS)

