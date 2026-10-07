from __future__ import annotations

from typing import Any

from src.features.dashboards.io.components.compact_card import (
    map_to_compact_card_rows,
)

from ..definitions.perforacion import (
    PERFORACION_F9_CARD_DEFINITION,
    PERFORACION_F11_CARD_DEFINITION,
    PERFORACION_F12_CARD_DEFINITION,
    PERFORACION_SUMMARY_DEFINITION
)


def build_perforacion_mapper(*, kpis: dict[str, Any]):
    for perforacion in (
        PERFORACION_F9_CARD_DEFINITION,
        PERFORACION_F11_CARD_DEFINITION,
        PERFORACION_F12_CARD_DEFINITION,
        PERFORACION_SUMMARY_DEFINITION
    ):
        yield map_to_compact_card_rows(
            definition=perforacion,
            kpis=kpis,
        )
