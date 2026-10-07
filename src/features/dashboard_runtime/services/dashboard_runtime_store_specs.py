from __future__ import annotations

from src.features.configuration.models.app_runtime_profile import AppRuntimeProfile
from src.features.dashboard_runtime.models.dashboard_runtime_store_spec import (
    DashboardRuntimeStoreKind,
    DashboardRuntimeStoreSpec,
)

from .dashboard_runtime_store_ids import build_dashboard_runtime_store_id


def build_dashboard_io_runtime_store_specs() -> tuple[DashboardRuntimeStoreSpec, ...]:
    return build_dashboard_runtime_store_specs(
        components=AppRuntimeProfile.INTEGRATED_OPERATIONS.build_components(),
        include_timelines=True,
        include_timestamps=True,
    )


def build_dashboard_process_runtime_store_specs() -> tuple[DashboardRuntimeStoreSpec, ...]:
    return build_dashboard_runtime_store_specs(
        components=AppRuntimeProfile.PROCESS.build_components(),
        include_timelines=True,
        include_timestamps=True,
    )


def build_dashboard_strategic_runtime_store_specs() -> tuple[DashboardRuntimeStoreSpec, ...]:
    return build_dashboard_runtime_store_specs(
        components=AppRuntimeProfile.STRATEGIC.build_components(),
        include_timelines=True,
        include_timestamps=True,
    )


def build_dashboard_runtime_store_specs_for_profile(
    *,
    profile: AppRuntimeProfile,
) -> tuple[DashboardRuntimeStoreSpec, ...]:
    if profile == AppRuntimeProfile.INTEGRATED_OPERATIONS:
        return build_dashboard_io_runtime_store_specs()

    if profile == AppRuntimeProfile.PROCESS:
        return build_dashboard_process_runtime_store_specs()

    if profile == AppRuntimeProfile.STRATEGIC:
        return build_dashboard_strategic_runtime_store_specs()

    raise ValueError(f'[ERROR] Invalid dashboard runtime profile: {profile}')


def build_dashboard_runtime_store_specs(
    *,
    components: tuple[str, ...],
    include_timelines: bool = True,
    include_timestamps: bool = True,
) -> tuple[DashboardRuntimeStoreSpec, ...]:
    specs: list[DashboardRuntimeStoreSpec] = []

    for component_key in components:
        specs.append(
            DashboardRuntimeStoreSpec(
                component_key=component_key,
                kind=DashboardRuntimeStoreKind.DATA,
                store_id=build_dashboard_runtime_store_id(
                    component_key=component_key,
                    kind=DashboardRuntimeStoreKind.DATA.value,
                ),
            )
        )

        if include_timelines:
            specs.append(
                DashboardRuntimeStoreSpec(
                    component_key=component_key,
                    kind=DashboardRuntimeStoreKind.TIMELINES,
                    store_id=build_dashboard_runtime_store_id(
                        component_key=component_key,
                        kind=DashboardRuntimeStoreKind.TIMELINES.value,
                    ),
                )
            )

    if include_timestamps:
        specs.append(
            DashboardRuntimeStoreSpec(
                component_key='timestamps',
                kind=DashboardRuntimeStoreKind.TIMESTAMPS,
                store_id=build_dashboard_runtime_store_id(
                    component_key='timestamps',
                    kind=DashboardRuntimeStoreKind.DATA.value,
                ),
            )
        )

    return tuple(specs)
