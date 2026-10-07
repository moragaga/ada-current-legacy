from __future__ import annotations

import dash

from src.features.configuration.admin_panels.alarm_management.images.layout import (
    build_alarm_image_definition_layout,
)

dash.register_page(
    __name__,
    path='/admin/alarm/images',
    name='Alarm Management Images Admin',
)

layout = build_alarm_image_definition_layout
