from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from src.features.configuration.services.config_app_runtime_profile import ConfigAppRuntimeProfile
from src.features.dashboard_runtime.models.dashboard_runtime_context import DashboardRuntimeContext

from .dashboard_query_service import DashboardQueryService


class DashboardContextService:
    def __init__(
        self,
        dashboard_query_service: DashboardQueryService,
        app_runtime_profile: ConfigAppRuntimeProfile,
    ) -> None:
        self._dashboard_query_service = dashboard_query_service
        self._app_runtime_profile = app_runtime_profile

    def get_dashboard_latest_update(self):
        return self._dashboard_query_service.get_latest_update()

    def get_dashboard_context(self) -> DashboardRuntimeContext:
        latest_snapshot = self._dashboard_query_service.get_latest_snapshot() or {}
        components = latest_snapshot.get('components', {}) or {}
        allowed_components = self._app_runtime_profile.get_runtime_components()
        profile = self._app_runtime_profile.get_profile_value()

        return DashboardRuntimeContext.from_snapshot(
            snapshot=latest_snapshot,
            profile=profile,
            allowed_components=allowed_components,
            meta=self._build_meta(
                components=components,
                allowed_components=allowed_components,
                profile_value=profile.value,
            ),
        )

    @staticmethod
    def _build_meta(
        *,
        components: dict[str, dict[str, Any]],
        allowed_components: tuple[str, ...],
        profile_value: str,
    ) -> dict[str, Any]:
        visible_components = {
            component: components.get(component, {}) for component in allowed_components
        }

        return {
            'generated_at_utc': datetime.now(tz=UTC).isoformat(),
            'profile': profile_value,
            'component_count': len(allowed_components),
            'instant_item_count': sum(
                len(items) for items in visible_components.values() if isinstance(items, dict)
            ),
        }
