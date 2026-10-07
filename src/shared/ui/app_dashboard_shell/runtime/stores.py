from __future__ import annotations

from dash import dcc

from src.features.dashboard_runtime.models.dashboard_runtime_store_spec import (
    DashboardRuntimeStoreSpec,
)
from src.features.dashboard_runtime.services.dashboard_runtime_refresh import (
    build_released_dashboard_refresh_lock,
)
from src.features.dashboard_runtime.services.dashboard_runtime_store_specs import (
    build_dashboard_io_runtime_store_specs,
    build_dashboard_process_runtime_store_specs,
    build_dashboard_strategic_runtime_store_specs,
)

from .ids import DashboardRuntimeShellIds


def build_dashboard_runtime_base_store_components(
    *,
    interval_ms: int,
) -> list:
    return [
        dcc.Interval(
            id=DashboardRuntimeShellIds.INTERVAL_DASHBOARD,
            interval=interval_ms,
            n_intervals=0,
            max_intervals=-1,
        ),
        dcc.Store(
            id=DashboardRuntimeShellIds.STORE_REFRESH_LOCK,
            data=build_released_dashboard_refresh_lock(),
            storage_type='memory',
        ),
        dcc.Store(
            id=DashboardRuntimeShellIds.STORE_REFRESH_SIGNAL,
            data=None,
            storage_type='memory',
        ),
        dcc.Store(
            id=DashboardRuntimeShellIds.STORE_INFORMATION_STATUS,
            data=None,
            storage_type='memory',
        ),
    ]


def build_dashboard_io_runtime_store_components(
    *,
    interval_ms: int,
) -> list:
    return [
        *build_dashboard_runtime_base_store_components(interval_ms=interval_ms),
        *_build_store_components(specs=build_dashboard_io_runtime_store_specs()),
    ]


def build_dashboard_process_runtime_store_components(
    *,
    interval_ms: int,
) -> list:
    return [
        *build_dashboard_runtime_base_store_components(interval_ms=interval_ms),
        *_build_store_components(specs=build_dashboard_process_runtime_store_specs()),
    ]


def build_dashboard_strategic_runtime_store_components(
    *,
    interval_ms: int,
) -> list:
    return [
        *build_dashboard_runtime_base_store_components(interval_ms=interval_ms),
        *_build_store_components(specs=build_dashboard_strategic_runtime_store_specs()),
    ]


def _build_store_components(
    *,
    specs: tuple[DashboardRuntimeStoreSpec, ...],
) -> list:
    return [
        dcc.Store(
            id=spec.store_id,
            data=None,
            storage_type='memory',
        )
        for spec in specs
    ]
