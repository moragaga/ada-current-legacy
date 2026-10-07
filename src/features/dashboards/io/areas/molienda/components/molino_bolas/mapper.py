from __future__ import annotations

from typing import Any

from .definition import MolinoBolasDefinition
from .model import MolinoBolasData, MolinoBolasGroupData

def map_molino_bolas_group(
    *,
    definitions: tuple[MolinoBolasDefinition, ...],
    kpis: dict[str, Any],
) -> MolinoBolasGroupData:
    return MolinoBolasGroupData.from_iterable(
        molinos_bolas=(
            map_molino_bolas(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions
        )
    )

def map_molino_bolas(
    *,
    definition: MolinoBolasDefinition,
    kpis: dict[str, Any],
) -> MolinoBolasData:
    return MolinoBolasData(
        label=definition.label,
        mb_state=kpis.get(definition.mb_state_key),
        mb_power=kpis.get(definition.mb_power_key),
        mb_power_color=kpis.get(definition.mb_power_color_key),
    )