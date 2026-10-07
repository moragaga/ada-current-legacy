from __future__ import annotations

import dash

from src.features.configuration.admin_panels.alarm_configuration.layout import (
    build_alarm_configuration_admin_layout,
)

dash.register_page(__name__, path='/admin/alarm', name='Alarm Configuration Admin')
layout = build_alarm_configuration_admin_layout
