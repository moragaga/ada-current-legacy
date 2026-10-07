from __future__ import annotations

import math
from typing import Any

from dash import html
from src.shared.ui.components.compact_table import CompactTableData, map_compact_table

from ..definitions.equipos_servicio import EQUIPOS_SERVICIO_TABLE_DEFINITION

_EQUIPOS = (
    'bulldozer',
    'wheeldozer',
    'motoniveladora',
    'excavadora',
    'aljibe',
    'cargador_frontal',
)


def _to_int(val: Any) -> int | None:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return None if math.isnan(val) else int(round(val))
    val_str = str(val).strip()
    if val_str in ('', '-', '--', 'nan', 'NaN', 'None', 'null'):
        return None
    try:
        f = float(val_str.replace(',', '.'))
        return None if math.isnan(f) else int(round(f))
    except (ValueError, TypeError):
        return None


def _fmt_int(val: int | None) -> str:
    if val is None:
        return '-'
    return str(val)


def _fmt_pair(real: int | None, plan: int | None, is_total: bool = False) -> html.Span:
    """Renderiza el valor real en gris grafito y quita la negrita al '/' y al plan/guion."""
    real_str = _fmt_int(real)
    plan_str = _fmt_int(plan)

    return html.Span(
        style={'whiteSpace': 'nowrap'},
        children=[
            html.Span(
                real_str,
                style={
                    'fontWeight': '700' if is_total else '600',
                    'color': '#4a4a4a',  # Gris grafito idéntico
                },
            ),
            html.Span(
                f' / {plan_str}',
                style={
                    'fontWeight': '400',  # Sin negrita
                    'color': '#707070',   # Gris suave
                },
            ),
        ],
    )


def _sum_vals(*vals: int | None) -> int | None:
    valid = [v for v in vals if v is not None]
    return sum(valid) if valid else None


def map_equipos_servicio_table(*, kpis: dict[str, Any]) -> CompactTableData:
    kpis_copy = dict(kpis)

    op_r_list: list[int | None] = []
    op_p_list: list[int | None] = []
    disp_r_list: list[int | None] = []
    disp_p_list: list[int | None] = []
    fs_r_list: list[int | None] = []
    fs_p_list: list[int | None] = []

    for key in _EQUIPOS:
        op_r = _to_int(
            kpis.get(f'equipos_servicio_{key}_operando_inst', kpis.get(f'equipos_servicio_{key}_operando'))
        )
        op_p = _to_int(
            kpis.get(f'equipos_servicio_{key}_operando_plan_inst', kpis.get(f'equipos_servicio_{key}_operando_plan'))
        )
        disp_r = _to_int(
            kpis.get(f'equipos_servicio_{key}_disponible_inst', kpis.get(f'equipos_servicio_{key}_disponible'))
        )
        disp_p = _to_int(
            kpis.get(f'equipos_servicio_{key}_disponible_plan_inst', kpis.get(f'equipos_servicio_{key}_disponible_plan'))
        )
        fs_r = _to_int(
            kpis.get(f'equipos_servicio_{key}_fuera_servicio_inst', kpis.get(f'equipos_servicio_{key}_fuera_servicio'))
        )
        fs_p = _to_int(
            kpis.get(f'equipos_servicio_{key}_fuera_servicio_plan_inst', kpis.get(f'equipos_servicio_{key}_fuera_servicio_plan'))
        )

        op_r_list.append(op_r)
        op_p_list.append(op_p)
        disp_r_list.append(disp_r)
        disp_p_list.append(disp_p)
        fs_r_list.append(fs_r)
        fs_p_list.append(fs_p)

        # Celdas por equipo (PA, BH, Bulldozer, etc.)
        kpis_copy[f'eq_serv_{key}_op'] = _fmt_pair(op_r, op_p, is_total=False)
        kpis_copy[f'eq_serv_{key}_disp'] = _fmt_pair(disp_r, disp_p, is_total=False)
        kpis_copy[f'eq_serv_{key}_fs'] = _fmt_pair(fs_r, fs_p, is_total=False)

    # Fila TOTAL: suma de valores válidos manteniendo el plan/guion sin negrita
    tot_op_r = _sum_vals(*op_r_list)
    tot_op_p = _sum_vals(*op_p_list)
    tot_disp_r = _sum_vals(*disp_r_list)
    tot_disp_p = _sum_vals(*disp_p_list)
    tot_fs_r = _sum_vals(*fs_r_list)
    tot_fs_p = _sum_vals(*fs_p_list)

    kpis_copy['eq_serv_total_op'] = _fmt_pair(tot_op_r, tot_op_p, is_total=True)
    kpis_copy['eq_serv_total_disp'] = _fmt_pair(tot_disp_r, tot_disp_p, is_total=True)
    kpis_copy['eq_serv_total_fs'] = _fmt_pair(tot_fs_r, tot_fs_p, is_total=True)

    return map_compact_table(
        definition=EQUIPOS_SERVICIO_TABLE_DEFINITION,
        kpis=kpis_copy,
    )