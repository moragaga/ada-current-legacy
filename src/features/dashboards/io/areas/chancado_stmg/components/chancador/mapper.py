from __future__ import annotations

from typing import Any

from .definition import ChancadorDefinition
from .models import ChancadorData, ChancadorGroupData


def map_chancador_group(
    *,
    definitions: tuple[ChancadorDefinition, ...],
    kpis: dict[str, Any],
) -> ChancadorGroupData:
    return ChancadorGroupData.from_iterable(
        chancadores=(
            map_chancador(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions
        )
    )


def map_chancador(
    *,
    definition: ChancadorDefinition,
    kpis: dict[str, Any],
) -> ChancadorData:
    return ChancadorData(
        label=definition.label,
        chancado_state=kpis.get(definition.chancado_state_key),
        chancado_value=kpis.get(definition.chancado_value_key),
        chancado_color=kpis.get(definition.chancado_color_key),
        chancado_unit=definition.chancado_unit,
        atollo_state=kpis.get(definition.atollo_state_key),
        mirror=definition.mirror,
    )
