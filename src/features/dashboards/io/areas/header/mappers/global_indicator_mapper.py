from __future__ import annotations

from typing import Any

from src.shared.ui.components.global_indicator import (
    GlobalIndicatorDetailData,
    GlobalIndicatorGroupData,
)
from src.utils.colors import get_status_color

from ..definitions.global_indicator_definition import (
    GLOBAL_INDICATOR_DEFINITIONS,
    GlobalIndicatorDefinition,
)


def build_global_indicator_mapper(
    *,
    kpis: dict[str, Any],
) -> GlobalIndicatorGroupData:
    return GlobalIndicatorGroupData(
        indicators=tuple(
            _map_global_indicator(
                definition=definition,
                kpis=kpis,
            )
            for definition in GLOBAL_INDICATOR_DEFINITIONS
        )
    )


def _map_global_indicator(
    *,
    definition: GlobalIndicatorDefinition,
    kpis: dict[str, Any],
) -> GlobalIndicatorDetailData:
    key = definition.kpi_key

    return GlobalIndicatorDetailData(
        uuid=f'{key}_global_indicator_container',
        indicator=definition.label,
        unit=definition.unit,
        real_dia=kpis.get(f'{key}_dia_real_inst'),
        plan_dia=kpis.get(f'{key}_dia_plan_inst'),
        color_dia=get_status_color(kpis.get(f'{key}_dia_color_inst')),
        real_semana=kpis.get(f'{key}_semana_real_inst'),
        plan_semana=kpis.get(f'{key}_semana_plan_inst'),
        color_semana=get_status_color(kpis.get(f'{key}_semana_color_inst')),
        border_left=definition.border_left,
        border_right=definition.border_right,
    )