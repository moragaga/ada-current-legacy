from __future__ import annotations

from dataclasses import dataclass



@dataclass(frozen=True, slots=True)
class GlobalIndicatorDefinition:
    kpi_key: str
    label: str
    unit: str
    border_left: bool = False
    border_right: bool = True


GLOBAL_INDICATOR_DEFINITIONS: tuple[GlobalIndicatorDefinition, ...] = (
    GlobalIndicatorDefinition(
        kpi_key='movimiento_mina',
        label='Movimiento Mina',
        unit='ktms',
        border_left=True,
        border_right=True,
    ),
    GlobalIndicatorDefinition(
        kpi_key='transportado',
        label='Transportado',
        unit='ktms',
    ),
    GlobalIndicatorDefinition(
        kpi_key='ley_cu',
        label='Ley Cu',
        unit='%',
    ),
    GlobalIndicatorDefinition(
        kpi_key='tratamiento',
        label='Tratamiento',
        unit='ktms',
    ),
    GlobalIndicatorDefinition(
        kpi_key='recuperacion_cu',
        label='Recuperación Cu',
        unit='%',
    ),
    GlobalIndicatorDefinition(
        kpi_key='cu_fino_producido',
        label='Cu Fino Producido',
        unit='tmf',
    ),
    GlobalIndicatorDefinition(
        kpi_key='mo_fino_producido',
        label='Mo Fino Producido',
        unit='tmf',
    ),
    GlobalIndicatorDefinition(
        kpi_key='mo_fino_envasado',
        label='Mo Fino Envasado',
        unit='tmf',
    ),
)
