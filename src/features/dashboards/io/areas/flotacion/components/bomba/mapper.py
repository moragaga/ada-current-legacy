from __future__ import annotations

from typing import Any

from .definition import BombasGroupDefinition, BombaDefinition
from .models import BombaData, BombaGroupData


def map_bomba_group(
    *,
    definitions: BombasGroupDefinition,
    kpis: dict[str, Any],
) -> BombaGroupData:
    list_content = []
    for definition in definitions.bombas_group:
        content = []
        for position, components in definition.items():
            for component in components:
                content.append(map_bomba(definition=component, kpis=kpis))
            list_content.append({
                position: content.copy(),
            })


    return BombaGroupData.from_iterable(
        bombas=tuple(list_content),
    )

def map_bomba(
    *,
    definition: BombaDefinition,
    kpis: dict[str, Any],
) -> BombaData:
    return BombaData(
        label=definition.label,
        bomba_state=kpis.get(definition.bomba_state_key),
    )
