from __future__ import annotations

from typing import Any

from src.shared.ui.components.compact_table import CompactTableData, map_compact_table
from src.shared.ui.components.metrics import MetricRowsData, map_standard_metric_rows

from ..definitions.remanentes import REMANENTES_METRIC_DEFINITION, REMANENTES_SUMMARY_DEFINITION


def build_remanentes_summary_mapper(*, kpis: dict[str, Any]) -> CompactTableData:
    return map_compact_table(
        definition=REMANENTES_SUMMARY_DEFINITION,
        kpis=kpis,
    )


def build_remanentes_metrics_mapper(*, kpis: dict[str, Any]) -> MetricRowsData:
    return map_standard_metric_rows(
        definitions=REMANENTES_METRIC_DEFINITION,
        kpis=kpis,
    )
