from __future__ import annotations

from typing import Any

from .definitions import StockpileMinaDefinition, StockpileMinaDetailDefinition
from .models import StockpileMinaData, StockpileMinaDetailData


def _map_pile(
    *,
    definition: StockpileMinaDetailDefinition,
    kpis: dict[str, Any],
) -> StockpileMinaDetailData:
    return StockpileMinaDetailData(
        percentage_value=kpis.get(definition.percentage_key),
        meters_value=kpis.get(definition.meters_key),
    )


def map_stockpile_mina(
    *,
    definition: StockpileMinaDefinition,
    kpis: dict[str, Any],
) -> StockpileMinaData:
    return StockpileMinaData(
        piles=(
            _map_pile(
                definition=pile,
                kpis=kpis,
            )
            for pile in definition.piles
        )
    )
