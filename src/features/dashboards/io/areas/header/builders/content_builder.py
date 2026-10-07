from __future__ import annotations

from src.shared.ui.rendering import KpiBuildDefinition

from .content.global_indicator import build_global_indicator_content
from .content.time_status import build_time_status_content
from .content.information import build_information_content
from .content.alarm_notifications import build_alarm_notification_content

CONTENT_BUILDER_DEFINITION = [
    KpiBuildDefinition(
        slot_name='HEADER - INDICADORES GLOBALES',
        builder=build_global_indicator_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
]

CONTENT_BUILDER_TIME_DEFINITION = [
    KpiBuildDefinition(
        slot_name='HEADER - TIME - STATUS',
        builder=build_time_status_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    )
]

CONTENT_BUILDER_ALARM_NOTIFICATION = [
    KpiBuildDefinition(
        slot_name='HEADER - ALARM INFORMATION',
        builder=build_information_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    ),
    KpiBuildDefinition(
        slot_name='HEADER - ALARM NOTIFICATION',
        builder=build_alarm_notification_content,
        ui_size='large',
        exclude_parameters=('timestamps', 'timeseries'),
    )
]