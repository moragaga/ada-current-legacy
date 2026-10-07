from __future__ import annotations

from dash import html


def build_app_alarm_shell(*, children=None) -> html.Div:
    children = children or []

    return html.Div(className='app-alarm-shell', children=children)
