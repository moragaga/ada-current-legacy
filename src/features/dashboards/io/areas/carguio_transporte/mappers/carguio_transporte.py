from __future__ import annotations

from typing import Any

from src.shared.ui.components.compact_table import CompactTableData, map_compact_table

from ..definitions.carguio_transporte import GESTION_CARGUIO_TURNO_DEFINITION


def build_gestion_carguio_turno_mapper(*, kpis: dict[str, Any]) -> CompactTableData:
    return map_compact_table(
        definition=GESTION_CARGUIO_TURNO_DEFINITION,
        kpis=kpis,
    )
