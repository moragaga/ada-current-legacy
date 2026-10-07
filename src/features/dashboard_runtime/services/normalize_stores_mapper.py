from __future__ import annotations

from typing import Any

from src.features.dashboard_runtime.models.dashboard_runtime_context import DashboardRuntimeContext
from src.features.dashboard_runtime.models.dashboard_runtime_store_spec import (
    DashboardRuntimeStoreKind,
    DashboardRuntimeStoreSpec,
)


def build_normalized_runtime_stores(
    *,
    context: DashboardRuntimeContext,
    store_specs: tuple[DashboardRuntimeStoreSpec, ...],
    runtime_store: dict[str, Any],
    add_missing_component: bool = True,
) -> list[dict[str, Any]]:
    normalized_stores: list[dict[str, Any]] = []

    for spec in store_specs:
        data = _resolve_store_data(context=context, spec=spec)

        if spec.kind == DashboardRuntimeStoreKind.DATA and add_missing_component:
            data.setdefault('', {'value': None, 'status': 'missing'})

        normalized_stores.append(
            {
                'data': data,
                **runtime_store.copy(),
            }
        )

    return normalized_stores


def rebuild_runtime_stores_from_current_state(
    *,
    current_store_values: list[dict[str, Any] | None],
    runtime_store: dict[str, Any],
) -> list[dict[str, Any]]:
    stores: list[dict[str, Any]] = []

    for current_store in current_store_values:
        current_store = current_store or {}
        current_data = current_store.get('data', {})

        if not isinstance(current_data, dict):
            current_data = {}

        stores.append(
            {
                'data': current_data.copy(),
                **runtime_store.copy(),
            }
        )

    return stores


def _resolve_store_data(
    *,
    context: DashboardRuntimeContext,
    spec: DashboardRuntimeStoreSpec,
) -> dict[str, Any]:
    if spec.kind == DashboardRuntimeStoreKind.DATA:
        return context.get_component(spec.component_key)

    if spec.kind == DashboardRuntimeStoreKind.TIMELINES:
        return context.get_timeline(spec.component_key)

    if spec.kind == DashboardRuntimeStoreKind.TIMESTAMPS:
        return context.timestamps.copy()

    return {}
