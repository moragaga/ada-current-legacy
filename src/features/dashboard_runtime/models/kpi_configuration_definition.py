from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

DashboardVisualization = Literal['text', 'json']
Components = Literal[
    'left_region', 'right_region', 'center_region', 'indicadores_globales', 'general'
]


@dataclass(frozen=True)
class KpiConfigurationInformationDefinition:
    kpi_name: str
    visualization: DashboardVisualization
    component: Components
    source: str
    load_instant: bool = True
    include_in_series_artifact: bool = False


@dataclass(frozen=True)
class KpiConfigurationDefinition:
    kpi_configuration: list[KpiConfigurationInformationDefinition]
