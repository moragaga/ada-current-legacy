from __future__ import annotations

from typing import Any

from src.shared.ui.components.metrics import map_standard_metric_rows

from .definition import CorreaStmgDefinition, CorreaStmgGroupDefinition
from .models import CorreaStmgData, CorreaStmgGroupData


def map_correa_stmg_group(
    *,
    definitions: CorreaStmgGroupDefinition,
    kpis: dict[str, Any],
) -> CorreaStmgGroupData:
    return CorreaStmgGroupData.from_iterable(
        correas=(
            map_correa_stmg(
                definition=definition,
                kpis=kpis,
            )
            for definition in definitions.correas
        ),
        metrics=(
            map_standard_metric_rows(
                definitions=definitions.metrics,
                kpis=kpis,
            )
            if definitions.metrics
            else None
        ),
    )


def map_correa_stmg(
    *,
    definition: CorreaStmgDefinition,
    kpis: dict[str, Any],
) -> CorreaStmgData:
    return CorreaStmgData(
        label=definition.label,
        correa_state=kpis.get(definition.correa_state_key),
    )
