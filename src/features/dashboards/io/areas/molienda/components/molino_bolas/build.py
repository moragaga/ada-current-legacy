from __future__ import annotations

from typing import TYPE_CHECKING

from dash import html

from dash.development.base_component import Component
from ..custom_equipment import build_custom_equipment

if TYPE_CHECKING:
    from .model import MolinoBolasData, MolinoBolasGroupData

def build_molino_bolas_component(*, model: MolinoBolasData, full_space: bool = True) -> Component:
    return build_custom_equipment(
        label=model.label,
        state=model.mb_state,
        power=model.mb_power,
        power_color=model.mb_power_color,
        equipment='molino_bolas',
        full_space=full_space
    )

def build_molinos_bolas_component(*, models: MolinoBolasGroupData) -> Component:
    return html.Div(
        className='d-flex gap-1 w-100',
        children=[
            build_molino_bolas_component(model=model, full_space=len(models) == 2) for model in models
        ]
    )