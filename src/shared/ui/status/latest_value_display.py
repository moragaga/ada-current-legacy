from __future__ import annotations

from dash.development.base_component import Component
from typing import Any

from src.shared.runtime.logging.debug import debug_log

from .invalid_value_icon import build_alerting_icon


def resolve_latest_value_display(
    *,
    value: str | list | dict | None = None,
    value_kind: str | None = None,
    status: str | None = None,
) -> dict | Component | Any | str :
    statuses = {
        'missing': build_alerting_icon(invalid_type='not_mapped'),
        'invalid': build_alerting_icon(invalid_type='invalid_data'),
        'ok': value,
    }

    current_status = statuses.get(status)
    if current_status is None:
        debug_log(f'Invalid status: {status}')

    if value_kind == 'value':
        return current_status
    elif value_kind == 'json':
        validation = not isinstance(current_status, Component)
        return {
            'is_ok': validation,
            'payload': value if validation else None,
            'default': '' if validation else current_status
        }
    else:
        return build_alerting_icon(invalid_type='not_mapped')