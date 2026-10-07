from __future__ import annotations

from typing import Any

from src.app.env_configuration import EnvConfiguration

from ..models.app_runtime_profile import AppRuntimeProfile, AppRuntimeProfileSettings


class ConfigAppRuntimeProfile:
    def __init__(
        self,
        *,
        settings: EnvConfiguration,
    ) -> None:
        self._settings = settings
        self._profile = AppRuntimeProfileSettings.from_value(value=settings.app_runtime_profile)

    def get_profile_settings(self) -> AppRuntimeProfileSettings:
        return self._profile

    def get_profile_value(self) -> AppRuntimeProfile:
        return self._profile.profile_value

    def get_runtime_components(self) -> tuple[str, ...]:
        return self._profile.data.components

    def include_timelines(self) -> bool:
        return self._profile.data.include_timelines

    def include_timestamps(self) -> bool:
        return self._profile.data.include_timestamps

    def build_component_select_configuration(self) -> dict[str, Any]:
        return {
            'options': self._profile.data.components,
            'default_value': self._profile.data.default_component,
        }
