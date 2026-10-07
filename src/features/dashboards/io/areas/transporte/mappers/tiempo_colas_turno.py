from __future__ import annotations

from typing import Any

from src.shared.ui.components.metrics import MetricRowsData, map_dual_metric_rows

from ..definitions.tiempos_colas_turno import TIEMPOS_COLAS_TURNO_DEFINITION


def build_no_operativo_turno_mapper(*, kpis: dict[str, Any]) -> MetricRowsData:
    return map_dual_metric_rows(
        definitions=TIEMPOS_COLAS_TURNO_DEFINITION,
        kpis=kpis,
    )
