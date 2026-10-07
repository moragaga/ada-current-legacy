from __future__ import annotations

from typing import Any

from src.shared.ui.components.metrics import MetricRowsData, map_standard_metric_rows

from ..definitions.no_operativo_turno import NO_OPERATIVO_TURNO_DEFINITION


def build_no_operativo_turno_mapper(*, kpis: dict[str, Any]) -> MetricRowsData:
    return map_standard_metric_rows(
        definitions=NO_OPERATIVO_TURNO_DEFINITION,
        kpis=kpis,
    )
