from __future__ import annotations

from dash import html


def build_slot_container(
    component_id: str,
    class_name: str,
) -> html.Div:
    return html.Div(
        id=component_id,
        className=class_name,
    )


def build_slot_ready_flag_container(id_flag: str):
    return html.Div(
        id=id_flag,
        className='d-none',
        **{'data-ready': 'false'},
    )
