from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from dash.development.base_component import Component

from src.shared.ui.charts.feeders import FeedersData
from src.shared.ui.charts.stockpile_mina import StockpileMinaData
from src.shared.ui.components.compact_table import CompactTableData

from ..chancador.models import ChancadorGroupData
from ..correa_stmg.models import CorreaStmgGroupData
from .build import build_chancado_stmg_component


@dataclass(frozen=True, slots=True)
class ProduccionGlobalMetricRow:
    label: str
    real: Any = '-'
    plan: Any = '-'
    proyeccion: Any = '-'
    objetivo_dia: Any = '-'
    requerido: Any = '-'


@dataclass(frozen=True, slots=True)
class ProduccionGlobalData:
    rows: list[ProduccionGlobalMetricRow]


@dataclass(frozen=True, slots=True)
class ChancadoStmgData:
    produccion_global_summary: ProduccionGlobalData
    chancadores: ChancadorGroupData
    chancadores_summary: CompactTableData
    stockpile_mina: StockpileMinaData
    feeders: FeedersData
    correas_stmg: CorreaStmgGroupData
    leyes_summary: CompactTableData

    def to_component(self) -> Component:
        return build_chancado_stmg_component(model=self)