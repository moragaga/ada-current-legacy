from __future__ import annotations

from typing import Any

from .definition import SagDefinition
from .model import SagData


def map_sag(
    *,
    definition: SagDefinition,
    kpis: dict[str, Any],
) -> SagData:
    return SagData(
        label=definition.label,
        sag_state=kpis.get(definition.sag_state_key),
        sag_power=kpis.get(definition.sag_power_key),
        sag_power_color=kpis.get(definition.sag_power_color_key),
    )
