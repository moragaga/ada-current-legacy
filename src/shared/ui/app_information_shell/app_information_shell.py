from __future__ import annotations

from dash import html


def build_app_information_shell(*, content=None) -> html.Div:
    content = content or []
    return html.Div(className='app-information-shell', children=content)
