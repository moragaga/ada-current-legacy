from __future__ import annotations

from src.app.dependencies import get_app_runtime_profile
from src.features.configuration.models.app_runtime_profile import AppRuntimeProfile
from src.features.dashboard_runtime.callbacks.refresh_dashboard_runtime_callback import (
    register_dashboard_runtime_refresh_callback,
)


def register_dashboard_home_callbacks() -> None:
    profile = get_app_runtime_profile().get_profile_value()

    register_dashboard_runtime_refresh_callback()

    if profile == AppRuntimeProfile.INTEGRATED_OPERATIONS:
        from src.features.dashboards.io import register_io_callback

        register_io_callback()
        return

    if profile == AppRuntimeProfile.PROCESS:
        from src.features.dashboards.process import register_process_callback

        register_process_callback()
        return

    if profile == AppRuntimeProfile.STRATEGIC:
        from src.features.dashboards.strategic import register_strategic_callback

        register_strategic_callback()
        return

    raise ValueError(f'[ERROR] Unsupported dashboard profile: {profile}')
