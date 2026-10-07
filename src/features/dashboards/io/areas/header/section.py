from __future__ import annotations

from src.shared.ui.app_header_shell.app_header_shell import build_app_header_shell

from .builders.slot_builder import (
    build_global_indicator_container,
    build_information_container,
    build_alarm_notifications_container,
    build_time_status_container,
    build_header_time_status_ready_flag,
    build_header_alarm_notifications_ready_flag,
    build_header_ready_flag
)


def build_header_section():
    return build_app_header_shell(
        app_name='OPERACIONES INTEGRADAS',
        global_indicator_content=[
            build_global_indicator_container(),
            build_header_ready_flag(),
        ],
        information_content=[
            build_information_container(),
        ],
        alarm_notifications_content=[
            build_alarm_notifications_container(),
            build_header_alarm_notifications_ready_flag()
        ],
        time_status_content=[
            build_time_status_container(),
            build_header_time_status_ready_flag(),
        ],
    )