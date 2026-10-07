from __future__ import annotations

from dash import html

from src.app.dependencies import get_app_runtime_profile
from src.features.configuration.models.app_runtime_profile import AppRuntimeProfile

from .io.layout import build_integrated_operations_home_layout
from .process.layout import build_process_home_layout
from .strategic.layout import build_strategic_home_layout

_DASHBOARD_HOME_ROOT_ID = 'dashboard-home-root'


def build_dashboard_home_layout():
    profile = get_app_runtime_profile().get_profile_value()

    if profile == AppRuntimeProfile.INTEGRATED_OPERATIONS:
        children = build_integrated_operations_home_layout()
    elif profile == AppRuntimeProfile.PROCESS:
        children = build_process_home_layout()
    elif profile == AppRuntimeProfile.STRATEGIC:
        children = build_strategic_home_layout()
    else:
        raise ValueError(f'[ERROR] Unsupported dashboard profile: {profile}')

    return html.Div(
        id=_DASHBOARD_HOME_ROOT_ID,
        **{'data-dashboard-profile': profile.value},
        children=children,
    )
