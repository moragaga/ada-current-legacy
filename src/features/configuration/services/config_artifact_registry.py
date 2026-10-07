from __future__ import annotations

from dataclasses import dataclass

from src.features.admin_framework.models import AdminDefinition

from ..admin_panels.alarm_configuration.definition import (
    ALARM_CONFIGURATION_ADMIN_DEFINITION,
)
from ..admin_panels.alarm_management.messages.definition import (
    ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION,
)
from ..admin_panels.kpi_configuration.definition import build_kpi_configuration_admin_definition
from ..admin_panels.navigation.groups.definition import NAVIGATION_GROUPS_ADMIN_DEFINITION
from ..admin_panels.navigation.links.definition import (
    NAVIGATION_LINKS_ADMIN_DEFINITION,
)
from .config_app_runtime_profile import ConfigAppRuntimeProfile


@dataclass(frozen=True)
class ConfigArtifactRegistry:
    definitions: tuple[AdminDefinition, ...]

    def get_definitions(self) -> tuple[AdminDefinition, ...]:
        return self.definitions


def build_config_artifact_registry(
    *,
    app_runtime_profile: ConfigAppRuntimeProfile,
) -> ConfigArtifactRegistry:
    return ConfigArtifactRegistry(
        definitions=(
            NAVIGATION_LINKS_ADMIN_DEFINITION,
            NAVIGATION_GROUPS_ADMIN_DEFINITION,
            ALARM_CONFIGURATION_ADMIN_DEFINITION,
            ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION,
            build_kpi_configuration_admin_definition(
                app_runtime_profile=app_runtime_profile,
            ),
        )
    )
