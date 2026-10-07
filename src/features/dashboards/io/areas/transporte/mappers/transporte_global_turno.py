from __future__ import annotations

from typing import Any

from src.features.dashboards.io.areas.transporte.definitions.transporte_global_turno import (
    TRANSPORTE_GLOBAL_TURNO_DEFINITION,
)
from src.shared.ui.components.metrics import (
    DualMetricDefinition,
    MetricRowsData,
    StandardMetricDefinition,
)
from src.shared.ui.components.metrics.mappers import (
    map_dual_metric,
    map_standard_metric,
)


def build_transporte_global_turno_mapper(*, kpis: dict[str, Any]) -> MetricRowsData:
    rows = []
    for definition in TRANSPORTE_GLOBAL_TURNO_DEFINITION:
        if isinstance(definition, DualMetricDefinition):
            rows.append(map_dual_metric(definition=definition, kpis=kpis))
        elif isinstance(definition, StandardMetricDefinition):
            rows.append(map_standard_metric(definition=definition, kpis=kpis))

    return MetricRowsData.from_iterable(items=rows)