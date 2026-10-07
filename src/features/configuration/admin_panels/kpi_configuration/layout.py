from __future__ import annotations

from src.app.dependencies import get_app_runtime_profile
from src.features.admin_framework.services import build_admin_layout

from .definition import build_kpi_configuration_admin_definition


def build_kpi_configuration_admin_layout():
    definition = build_kpi_configuration_admin_definition(
        app_runtime_profile=get_app_runtime_profile(),
    )

    return build_admin_layout(definition)
