from __future__ import annotations

from typing import TYPE_CHECKING

from dash.development.base_component import Component
from ..custom_equipment import build_custom_equipment

if TYPE_CHECKING:
    from .model import SagData

def build_sag_component(*, model: SagData) -> Component:
    return build_custom_equipment(
        label=model.label,
        state=model.sag_state,
        power=model.sag_power,
        power_color=model.sag_power_color,
        equipment='sag',
    )