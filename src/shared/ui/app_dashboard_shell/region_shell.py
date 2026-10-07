from __future__ import annotations

import dash_bootstrap_components as dbc


def build_region_shell(
    *,
    region_id: str,
    children=None,
    width_xs: int = 12,
    width_sm: int = 4,
    width_md: int = 4,
    width_lg: int = 4,
    width_xl: int = 4,
    class_name: str = 'd-flex',
) -> dbc.Col:
    children = children or []

    return dbc.Col(
        id=region_id,
        className=class_name,
        xs=width_xs,
        sm=width_sm,
        md=width_md,
        lg=width_lg,
        xl=width_xl,
        children=children,
    )
