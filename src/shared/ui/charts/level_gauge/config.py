from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

GaugeVariant = Literal['tk', 'st']


@dataclass(frozen=True, slots=True)
class LevelGaugeVariantConfig:
    y_min: float
    y_max: float
    bar_width: float
    x_center: float


LEVEL_GAUGE_VARIANT_CONFIGS: dict[GaugeVariant, LevelGaugeVariantConfig] = {
    'tk': LevelGaugeVariantConfig(
        y_min=0.05,
        y_max=0.65,
        bar_width=0.08,
        x_center=0.55,
    ),
    'st': LevelGaugeVariantConfig(
        y_min=0.05,
        y_max=0.75,
        bar_width=0.08,
        x_center=0.55,
    ),
}
