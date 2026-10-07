from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from src.features.configuration.models.app_runtime_profile import AppRuntimeProfile


@dataclass(slots=True)
class DashboardRuntimeContext:
    snapshot_timestamp: str | None
    components: dict[str, dict[str, Any]] = field(default_factory=dict)
    timelines: dict[str, dict[str, Any]] = field(default_factory=dict)
    timestamps: dict[str, Any] = field(default_factory=dict)
    meta: dict[str, Any] = field(default_factory=dict)
    profile: AppRuntimeProfile | None = None

    @classmethod
    def empty(
        cls,
        *,
        profile: AppRuntimeProfile | None = None,
        allowed_components: tuple[str, ...] = (),
    ) -> DashboardRuntimeContext:
        return cls(
            snapshot_timestamp=None,
            components={component: {} for component in allowed_components},
            timelines={component: {} for component in allowed_components},
            timestamps={},
            meta={},
            profile=profile,
        )

    @classmethod
    def from_snapshot(
        cls,
        *,
        snapshot: dict[str, Any] | None,
        profile: AppRuntimeProfile,
        allowed_components: tuple[str, ...],
        meta: dict[str, Any] | None = None,
    ) -> DashboardRuntimeContext:
        if not isinstance(snapshot, dict):
            return cls.empty(profile=profile, allowed_components=allowed_components)

        raw_components = snapshot.get('components', {}) or {}
        raw_timelines = snapshot.get('timelines', {}) or snapshot.get('time_series', {}) or {}
        raw_timestamps = snapshot.get('timestamps', {}) or {}

        components = {
            component: _safe_dict(raw_components.get(component)) for component in allowed_components
        }

        timelines = {
            component: _safe_dict(raw_timelines.get(component)) for component in allowed_components
        }

        return cls(
            snapshot_timestamp=snapshot.get('timestamp') or snapshot.get('snapshot_timestamp'),
            components=components,
            timelines=timelines,
            timestamps=_safe_dict(raw_timestamps),
            meta=meta or {},
            profile=profile,
        )

    def get_component(self, component_key: str) -> dict[str, Any]:
        return _safe_dict(self.components.get(component_key))

    def get_timeline(self, component_key: str) -> dict[str, Any]:
        return _safe_dict(self.timelines.get(component_key))


def _safe_dict(value: Any) -> dict[str, Any]:
    if isinstance(value, dict):
        return value.copy()

    return {}
