from __future__ import annotations

from typing import Any

from .definition import VertimilDefinition
from .models import VertimilData, VertimilGroupData


def map_vertimil_group(
    *,
    definitions: tuple[VertimilDefinition, ...],
    kpis: dict[str, Any],
) -> VertimilGroupData:
    return VertimilGroupData.from_iterable(
        vertimils=(
            map_vertimil(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions
        )
    )


def map_vertimil(
    *,
    definition: VertimilDefinition,
    kpis: dict[str, Any],
) -> VertimilData:
    return VertimilData(
        label=definition.label,
        vertimil_state=kpis.get(definition.vertimil_state_key),
        vertimil_value=kpis.get(definition.vertimil_value_key),
        vertimil_unit=definition.vertimil_unit,
        vertimil_color=kpis.get(definition.vertimil_color_key),
    )
