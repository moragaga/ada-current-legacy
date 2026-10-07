from __future__ import annotations

import dash

from src.features.configuration.admin_panels.kpi_configuration.layout import (
    build_kpi_configuration_admin_layout,
)

dash.register_page(__name__, path='/admin/kpi', name='Kpi Configuration Admin')
layout = build_kpi_configuration_admin_layout
