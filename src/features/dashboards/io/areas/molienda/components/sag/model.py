from __future__ import annotations

from dataclasses import dataclass
from typing import TypeAlias

from dash.development.base_component import Component
from .build import build_sag_component

DisplayValue: TypeAlias = str | int | float | Component | None


@dataclass(frozen=True, slots=True)
class SagData:
    label: str
    sag_state: DisplayValue = None
    sag_power: DisplayValue = None
    sag_power_color: DisplayValue = None

    def to_component(self) -> Component:
        return build_sag_component(model=self)
