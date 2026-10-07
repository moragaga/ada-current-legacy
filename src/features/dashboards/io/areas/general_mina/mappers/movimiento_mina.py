from __future__ import annotations

from typing import Any

from src.shared.ui.components.compact_table import CompactTableData, map_compact_table

from ..definitions.movimiento_mina import (
    MOVIMIENTO_MINA_SUMMARY_DEFINITION,
)


def build_movimiento_mina_summary_mapper(*, kpis: dict[str, Any]) -> CompactTableData:
    return map_compact_table(
        definition=MOVIMIENTO_MINA_SUMMARY_DEFINITION,
        kpis=kpis,
    )
