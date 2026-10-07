from __future__ import annotations

from typing import Any

from .definitions import FeederDefinition, FeedersDefinition
from .models import FeederData, FeedersData


def map_feeder(
    *,
    definition: FeederDefinition,
    kpis: dict[str, Any],
) -> FeederData:
    return FeederData(
        label=definition.label,
        value=kpis.get(definition.value_key),
        color=kpis.get(definition.color_key),
    )


def map_feeders(
    *,
    definition: FeedersDefinition,
    kpis: dict[str, Any],
) -> FeedersData:
    return FeedersData.from_iterable(
        items=(
            map_feeder(
                definition=feeder,
                kpis=kpis,
            )
            for feeder in definition.feeders
        ),
    )
