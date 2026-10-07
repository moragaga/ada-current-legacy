from __future__ import annotations

_DASHBOARD_RUNTIME_STORE_PREFIX = 'dashboard-runtime-store'


def build_dashboard_runtime_store_id(
    *,
    component_key: str,
    kind: str,
) -> str:
    safe_component_key = component_key.strip().replace('_', '-')
    safe_kind = kind.strip().replace('_', '-')

    return f'{_DASHBOARD_RUNTIME_STORE_PREFIX}-{safe_component_key}-{safe_kind}'
