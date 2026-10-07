from __future__ import annotations

import dash

from src.features.configuration.admin_panels.alarm_management.messages.layout import (
    build_alarm_management_messages_admin_layout,
)

dash.register_page(
    __name__,
    path='/admin/alarm/messages',
    name='Alarm Management Messages Admin',
)

layout = build_alarm_management_messages_admin_layout
