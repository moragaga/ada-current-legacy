from __future__ import annotations

from typing import Any

from .definitions import LevelGaugeDefinition
from .models import (
    LevelGaugeDetailData,
    LevelGaugeGroupData,
)


def map_level_gauge_group(
    *,
    definitions: tuple[LevelGaugeDefinition, ...],
    kpis: dict[str, Any],
) -> LevelGaugeGroupData:
    return LevelGaugeGroupData.from_iterable(
        level_gauges=(
            map_level_gauge(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions
        ),
    )


def map_level_gauge(
    *,
    definition: LevelGaugeDefinition,
    kpis: dict[str, Any],
    override_state: str | None = None,
) -> LevelGaugeDetailData:
    return LevelGaugeDetailData(
        name=definition.name,
        variant=definition.variant,
        image_name=definition.image_name,
        percentage=kpis.get(definition.percentage_kpi_key),
        state=kpis.get(definition.state_kpi_key) if override_state is None else override_state,
        color=kpis.get(definition.color_kpi_key),
        unit=definition.unit,
    )
