from __future__ import annotations

import pandas as pd
import plotly.graph_objs as go
from dash.development.base_component import Component

from .config import LEVEL_GAUGE_VARIANT_CONFIGS, GaugeVariant, LevelGaugeVariantConfig

BARS_COLORS: dict[str, str] = {'1': '#DC3545', '2': '#E0A800'}


def build_level_gauge_figure(
    *,
    variant: GaugeVariant,
    value: float | str | None | Component,
    assets_src: str | None,
    color: str | None | Component,
) -> go.Figure:
    numeric_value = _resolve_numeric_value(value=value)
    numeric_value = max(0.0, min(float(numeric_value), 100))
    value_frac = numeric_value / 100

    config: LevelGaugeVariantConfig = LEVEL_GAUGE_VARIANT_CONFIGS.get(variant)
    bar_range = config.y_max - config.y_min
    bar_fill = config.y_min + value_frac * bar_range

    x0 = config.x_center - config.bar_width / 2
    x1 = config.x_center + config.bar_width / 2

    fill_color = BARS_COLORS.get(color or '') or '#000000'

    fig = go.Figure()

    fig.add_shape(
        type='rect',
        x0=x0,
        x1=x1,
        y0=config.y_min,
        y1=bar_fill,
        fillcolor=fill_color,
        opacity=0.8,
        line_width=1,
        layer='above',
    )

    fig.add_shape(
        type='rect',
        x0=x0,
        x1=x1,
        y0=bar_fill,
        y1=config.y_max,
        fillcolor='#FFFFFF',
        opacity=0.8,
        line_width=1,
        layer='above',
    )

    fig.update_layout(
        paper_bgcolor='rgba(0, 0, 0, 0)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin={'l': 0, 'r': 0, 't': 0, 'b': 0},
        xaxis={'visible': False, 'range': [0, 1]},
        yaxis={'visible': False, 'range': [0, 1]},
    )

    if assets_src:
        fig.add_layout_image(
            source=assets_src,
            x=0,
            y=0,
            sizex=1,
            sizey=1,
            opacity=1,
            yanchor='bottom',
            sizing='stretch',
            layer='below',
        )

    return fig


def _resolve_numeric_value(*, value: float | str | None | Component):
    try:
        if not isinstance(value, Component):
            numeric_value = pd.to_numeric(value, errors='coerce')
            if pd.isna(numeric_value):
                numeric_value = 0.0
        else:
            numeric_value = 0.0

        return numeric_value
    except Exception as e:
        print(f'[ERROR] transform value {value}: {e}')
        return 0.0
