from __future__ import annotations

from typing import Any

from src.shared.ui.components.metrics import map_standard_metric_rows, StandardMetricDefinition
from ...definitions.sag import (
    SAG_1_DEFINITION,
    SAG_2_DEFINITION,
    SAG_3_DEFINITION,
    SAG_4_DEFINITION
)
from ...definitions.molino_bolas import (
    MB_SAG_1_DEFINITION,
    MB_SAG_2_DEFINITION,
    MB_SAG_3_DEFINITION,
    MB_SAG_4_DEFINITION
)
from ...definitions.metrics import (
    SAG_1_METRICS,
    SAG_2_METRICS,
    SAG_3_METRICS,
    SAG_4_METRICS
)

from ..sag.definition import SagDefinition
from ..sag.mapper import map_sag
from ..molino_bolas.definition import MolinoBolasDefinition
from ..molino_bolas.mapper import map_molino_bolas_group

# if TYPE_CHECKING:
from .model import LineaSagGroupData, LineaSagData


def build_linea_sag_mapper(
    *,
    linea_number: int,
    sag_definition: SagDefinition,
    molinos_bolas_definition: tuple[MolinoBolasDefinition, ...],
    metrics_definition: tuple[StandardMetricDefinition, ...],
    kpis: dict[str, Any],
) -> LineaSagData:
    return LineaSagData(
        linea_number=str(linea_number),
        sag=map_sag(
            definition=sag_definition,
            kpis=kpis,
        ),
        molinos_bolas=map_molino_bolas_group(
            definitions=molinos_bolas_definition,
            kpis=kpis,
        ),
        metrics=map_standard_metric_rows(
            definitions=metrics_definition,
            kpis=kpis,
        )
    )

def build_lineas_sag_mapper(
    *,
    kpis: dict[str, Any],
) -> LineaSagGroupData:
    grouped = [
        (SAG_1_DEFINITION, MB_SAG_1_DEFINITION, SAG_1_METRICS),
        (SAG_2_DEFINITION, MB_SAG_2_DEFINITION, SAG_2_METRICS),
        (SAG_3_DEFINITION, MB_SAG_3_DEFINITION, SAG_3_METRICS),
        (SAG_4_DEFINITION, MB_SAG_4_DEFINITION, SAG_4_METRICS),
    ]

    return LineaSagGroupData(
        lineas_sag=(
            build_linea_sag_mapper(
                linea_number=index,
                sag_definition=sag,
                molinos_bolas_definition=molinos_bolas,
                metrics_definition=metrics,
                kpis=kpis,
            )
            for index, (sag, molinos_bolas, metrics) in enumerate(grouped, start=1)
        )
    )