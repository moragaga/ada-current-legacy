from __future__ import annotations

from dash import html

from ..services.admin_component_ids import (
    build_admin_component_ids,
)


def build_admin_modal_host(admin_key: str) -> html.Div:
    ids = build_admin_component_ids(admin_key)
    return html.Div(id=ids['modal_host'])
