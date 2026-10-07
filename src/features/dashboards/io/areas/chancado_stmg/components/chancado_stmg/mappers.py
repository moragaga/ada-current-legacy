from __future__ import annotations

from typing import Any

from src.shared.ui.charts.feeders import map_feeders
from src.shared.ui.charts.stockpile_mina import map_stockpile_mina
from src.shared.ui.components.compact_table import map_compact_table

from ...definitions.chancado.correas_stmg import CORREAS_STMG_DEFINITION
from ...definitions.chancado.equipos_ch import (
    CHANCADORES_DEFINITION,
    CHANCADORES_SUMMARY_DEFINITION,
    FEEDERS_DEFINITION,
    STOCKPILE_MINA_DEFINITION,
)
from ...definitions.chancado.leyes import LEYES_SUMMARY_DEFINITION
from ..chancador import map_chancador_group
from ..correa_stmg import map_correa_stmg_group
from .models import ChancadoStmgData, ProduccionGlobalData, ProduccionGlobalMetricRow


def _extract_from_kpis(kpis: dict[str, Any], keys: list[str], fallback: str = '-') -> str:
    for key in keys:
        if key in kpis:
            res = _clean_kpi_value(kpis[key])
            if res != '-':
                return res
    return _clean_kpi_value(fallback)

def _clean_kpi_value(val: Any) -> str:
    if val is None:
        return '-'

    if isinstance(val, dict):
        parsed = val.get('parsed_value')
        raw = val.get('value')
        candidate = parsed if parsed is not None and str(parsed).lower() != 'nan' else raw
    else:
        candidate = val

    if candidate is None:
        return '-'

    cand_str = str(candidate).strip()

    if (
        cand_str.lower() in ('nan', 'none', 'null', '')
        or 'invalid-value-icon' in cand_str
        or 'img' in cand_str.lower()
    ):
        return '-'

    # Normalizar coma decimal a punto antes de convertir a float
    cand_num_str = cand_str.replace(',', '.')

    try:
        f_val = float(cand_num_str)
        if f_val.is_integer():
            return str(int(f_val))
        return f'{f_val:.1f}'
    except (ValueError, TypeError):
        return cand_str


def map_produccion_global(*, kpis: dict[str, Any]) -> ProduccionGlobalData:
    summary = kpis.get('produccion_global_summary_inst', {})

    # 1. Extraer datos preexistentes de summary como respaldo
    data = {}
    if summary.get('is_ok'):
        for item in summary.get('payload', []):
            item_copy = item.copy()
            _key = item_copy.pop('key', None)
            item_copy.pop('label', None)
            if _key:
                data[_key] = item_copy

    data_alim = data.get('alimentacion', {})
    data_transp = data.get('transporte') or data.get('transportado') or {}

    # Print de diagnóstico rápido en consola
    print("\n>>> [MAPPER DEBUG] Claves de alimentación en kpis:", [k for k in kpis if 'alimentacion' in k])

    # 2. ALIMENTACIÓN
    # AVANCE: Real
    alim_real = _extract_from_kpis(
        kpis,
        ['alimentacion_chancado_real_inst', 'alimentacion_chancado_real'],
        fallback=data_alim.get('real', '-'),
    )
    alim_plan_acum = _extract_from_kpis(
        kpis,
        [
            'alimentacion_chancado_plan_semana_inst',
            'alimentacion_chancado_plan_acum_inst',
            'alimentacion_chancado_plan_semanal_inst',
            'alimentacion_plan_semana_inst',
        ],
        fallback=data_alim.get('plan', '-'),
    )
    alim_plan_dia = _extract_from_kpis(
        kpis,
        ['alimentacion_chancado_plan_inst', 'alimentacion_chancado_plan_obj_inst', 'alimentacion_chancado_plan'],
        fallback=data_alim.get('objetivo_dia', '-'),
    )
    # CIERRE: Proy.
    alim_proy = _extract_from_kpis(
        kpis,
        ['alimentacion_chancado_proy_inst', 'alimentacion_chancado_simulado', 'alimentacion_chancado_proyeccion_inst'],
        fallback=data_alim.get('proyeccion', '-'),
    )
    # RITMO: Req./h
    alim_req = _extract_from_kpis(
        kpis,
        ['alimentacion_chancado_requerido_plan_inst', 'alimentacion_chancado_requerido_plan'],
        fallback=data_alim.get('requerido', '-'),
    )

    # 3. TRANSPORTADO
    # AVANCE: Real
    transp_real = _extract_from_kpis(
        kpis,
        ['transportado_stmg_real_inst', 'transporte_stmg_real'],
        fallback=data_transp.get('real', '-'),
    )
    # AVANCE: Plan acum.
    transp_plan_acum = _extract_from_kpis(
        kpis,
        [
            'transportado_stmg_plan_semana_inst',
            'transportado_stmg_plan_acum_inst',
            'transportado_stmg_plan_semanal_inst',
        ],
        fallback=data_transp.get('plan', '-'),
    )
    # CIERRE: Plan día
    transp_plan_dia = _extract_from_kpis(
        kpis,
        ['transportado_stmg_plan_inst', 'transportado_stmg_plan_obj_inst', 'transporte_stmg_plan_obj', 'transporte_stmg_plan'],
        fallback=data_transp.get('objetivo_dia', '-'),
    )
    # CIERRE: Proy.
    transp_proy = _extract_from_kpis(
        kpis,
        ['transportado_stmg_proy_inst', 'transporte_stmg_proyectado', 'transporte_stmg_simulado', 'transportado_stmg_proyeccion_inst'],
        fallback=data_transp.get('proyeccion', '-'),
    )
    # RITMO: Req./h
    transp_req = _extract_from_kpis(
        kpis,
        ['transportado_stmg_requerido_plan_inst', 'transporte_stmg_requerido_plan'],
        fallback=data_transp.get('requerido', '-'),
    )

    print(f">>> [MAPPER DEBUG] Resultado Alimentación Plan Acumulado: {alim_plan_acum}")

    # 4. Construcción de filas
    rows = [
        ProduccionGlobalMetricRow(
            label='Alimentación',
            real=alim_real,
            plan=alim_plan_acum,
            proyeccion=alim_proy,
            objetivo_dia=alim_plan_dia,
            requerido=alim_req,
        ),
        ProduccionGlobalMetricRow(
            label='Transportado',
            real=transp_real,
            plan=transp_plan_acum,
            proyeccion=transp_proy,
            objetivo_dia=transp_plan_dia,
            requerido=transp_req,
        ),
    ]

    return ProduccionGlobalData(rows=rows)

def build_chancado_stmg_mapper(
    *,
    kpis: dict[str, Any],
) -> ChancadoStmgData:
    return ChancadoStmgData(
        produccion_global_summary=map_produccion_global(kpis=kpis),
        chancadores=map_chancador_group(
            definitions=CHANCADORES_DEFINITION,
            kpis=kpis,
        ),
        chancadores_summary=map_compact_table(
            definition=CHANCADORES_SUMMARY_DEFINITION,
            kpis=kpis,
        ),
        stockpile_mina=map_stockpile_mina(
            definition=STOCKPILE_MINA_DEFINITION,
            kpis=kpis,
        ),
        feeders=map_feeders(
            definition=FEEDERS_DEFINITION,
            kpis=kpis,
        ),
        correas_stmg=map_correa_stmg_group(
            definitions=CORREAS_STMG_DEFINITION,
            kpis=kpis,
        ),
        leyes_summary=map_compact_table(
            definition=LEYES_SUMMARY_DEFINITION,
            kpis=kpis,
        ),
    )