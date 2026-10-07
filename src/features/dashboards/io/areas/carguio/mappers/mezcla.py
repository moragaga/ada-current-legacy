from __future__ import annotations

import math
from typing import Any

from dash import html
from src.shared.ui.components.compact_table import CompactTableData, map_compact_table
from src.utils.colors import extract_status_code, get_status_color

from ..definitions.mezcla import MEZCLA_TABLE_DEFINITION


def _get_first(kpis: dict[str, Any], *keys: str) -> Any:
    """Retorna el primer valor no nulo encontrado para las claves especificadas."""
    for key in keys:
        if key in kpis and kpis[key] is not None:
            return kpis[key]
    return None


def _to_float(val: Any) -> float | None:
    if val is None:
        return None
    if isinstance(val, dict):
        parsed = val.get('parsed_value')
        if parsed is not None and str(parsed).lower() != 'nan':
            val = parsed
        else:
            val = val.get('value')
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return None if math.isnan(val) else float(val)
    val_str = str(val).strip()
    if val_str in ('', '-', '--', 'nan', 'NaN', 'None', 'null'):
        return None
    try:
        f = float(val_str.replace(',', '.'))
        return None if math.isnan(f) else f
    except (ValueError, TypeError):
        return None


def _fmt_int(val: float | None) -> str:
    if val is None:
        return '-'
    return f'{round(val)}'


def _fmt_rend(val: float | None, decimals: int = 3) -> str:
    if val is None:
        return '-'
    return f'{val:.{decimals}f}'


def _sum_vals(*vals: float | None) -> float | None:
    valid = [v for v in vals if v is not None]
    return sum(valid) if valid else None


def _safe_status_color(status: str | int, fallback_hex: str) -> str:
    try:
        c = get_status_color(status)
        if c:
            return c
    except Exception:
        pass
    return fallback_hex


def _resolve_status_color(code: Any) -> str | None:

    if code is None:
        return None

    if isinstance(code, str) and code.startswith('#'):
        return code

    if isinstance(code, dict):
        for k in ('status', 'status_code', 'code', 'alert', 'semaforo'):
            if k in code and code[k] is not None:
                code = code[k]
                break
        else:
            code = code.get('value')

    code_str = str(code).strip().lower()

    if code == 0 or code_str in ('0', '0.0', 'red', 'rojo', 'danger', 'critico', 'crítico'):
        return _safe_status_color(0, _safe_status_color('red', '#dc3545'))

    if code == 1 or code_str in ('1', '1.0', 'yellow', 'amarillo', 'warning', 'alerta'):
        return _safe_status_color(1, _safe_status_color('yellow', '#ffc107'))

    # Si no es 0 ni 1, no se pinta
    return None


def _get_kpi_color(kpis: dict[str, Any], *prefixes_or_keys: str) -> str | None:
    suffixes = (
        '_color_inst',
        '_color',
        '_inst_color',
        '_status_inst',
        '_status',
        '_alert_inst',
        '_alert',
        '_semaforo_inst',
        '_semaforo',
        '',
    )
    for prefix in prefixes_or_keys:
        for suffix in suffixes:
            key = f'{prefix}{suffix}'
            if key in kpis and kpis[key] is not None:
                val = kpis[key]
                code = extract_status_code(val)
                color = _resolve_status_color(code)
                if color is not None:
                    return color

                # Si es un sufijo explícito de estado/color o un diccionario con estado
                is_status_key = suffix != '' or any(
                    s in prefix for s in ('status', 'color', 'alert', 'semaforo')
                )
                if is_status_key or isinstance(val, dict):
                    color = _resolve_status_color(val)
                    if color is not None:
                        return color
    return None


def _resolve_op_req_color(
    op: float | None = None,
    req: float | None = None,
    kpi_color: str | None = None,
) -> str | None:
    """Aplica la regla de color para Op / Req:
    Respeta el color si el código es 0 (rojo) o 1 (amarillo).
    En cualquier otro caso, retorna None (no se pinta).
    """
    return _resolve_status_color(kpi_color) if kpi_color else None


def _fmt_pair(
    real_str: str,
    plan_str: str,
    is_total: bool = False,
    color: str | None = None,
) -> html.Span:
    real_color = color if color else '#4a4a4a'

    return html.Span(
        style={'whiteSpace': 'nowrap'},
        children=[
            html.Span(
                real_str,
                style={
                    'fontWeight': '700' if is_total else '600',
                    'color': real_color,
                },
            ),
            html.Span(
                f' / {plan_str}',
                style={
                    'fontWeight': '400',
                    'color': '#707070',  # Gris suave sin negrita
                },
            ),
        ],
    )


def map_mezcla_table(*, kpis: dict[str, Any]) -> CompactTableData:
    kpis_copy = dict(kpis)
    vals: dict[str, dict[str, float | None]] = {}

    for flota in ('pa', 'bh'):
        op = _to_float(_get_first(kpis, f'mezcla_{flota}_op_inst', f'mezcla_{flota}_op'))
        req = _to_float(
            _get_first(
                kpis,
                f'mezcla_{flota}_req_plan',
                f'mezcla_{flota}_req_inst',
                f'mezcla_{flota}_req',
            )
        )
        disp = _to_float(_get_first(kpis, f'mezcla_{flota}_disp_inst', f'mezcla_{flota}_disp'))
        disp_p = _to_float(_get_first(kpis, f'mezcla_{flota}_disp_plan', f'mezcla_{flota}_disp_p'))
        uebd = _to_float(_get_first(kpis, f'mezcla_{flota}_uebd_inst', f'mezcla_{flota}_uebd'))
        uebd_p = _to_float(_get_first(kpis, f'mezcla_{flota}_uebd_plan', f'mezcla_{flota}_uebd_p'))
        rend = _to_float(_get_first(kpis, f'mezcla_{flota}_rend_inst', f'mezcla_{flota}_rend'))
        rend_p = _to_float(_get_first(kpis, f'mezcla_{flota}_rend_plan', f'mezcla_{flota}_rend_p'))

        backend_color_op = _get_kpi_color(
            kpis,
            f'mezcla_{flota}_req',
            f'mezcla_{flota}_op_req',
            f'mezcla_{flota}_op',
            f'mezcla_{flota}_req_plan',
        )
        color_op = _resolve_op_req_color(op=op, req=req, kpi_color=backend_color_op)

        color_disp = _get_kpi_color(kpis, f'mezcla_{flota}_disp')
        color_uebd = _get_kpi_color(kpis, f'mezcla_{flota}_uebd')
        color_rend = _get_kpi_color(kpis, f'mezcla_{flota}_rend')

        # Filas individuales (PA y BH)
        kpis_copy[f'mezcla_{flota}_op_req'] = _fmt_pair(_fmt_int(op), _fmt_int(req), color=color_op)
        kpis_copy[f'mezcla_{flota}_disp'] = _fmt_pair(_fmt_int(disp), _fmt_int(disp_p), color=color_disp)
        kpis_copy[f'mezcla_{flota}_uebd'] = _fmt_pair(_fmt_int(uebd), _fmt_int(uebd_p), color=color_uebd)
        kpis_copy[f'mezcla_{flota}_rend'] = _fmt_pair(_fmt_rend(rend), _fmt_rend(rend_p), color=color_rend)

        vals[flota] = {
            'op': op,
            'req': req,
            'disp': disp,
            'disp_p': disp_p,
            'uebd': uebd,
            'uebd_p': uebd_p,
            'rend': rend,
            'rend_p': rend_p,
        }

    pa, bh = vals['pa'], vals['bh']

    # Suma directa de las flotas para la fila TOTAL
    tot_op = _sum_vals(pa['op'], bh['op'])
    tot_req = _to_float(
        _get_first(kpis, 'mezcla_total_req_plan', 'mezcla_total_req_inst', 'mezcla_total_req')
    ) or _sum_vals(pa['req'], bh['req'])
    tot_disp = _sum_vals(pa['disp'], bh['disp'])
    tot_disp_p = _sum_vals(pa['disp_p'], bh['disp_p'])
    tot_uebd = _sum_vals(pa['uebd'], bh['uebd'])
    tot_uebd_p = _sum_vals(pa['uebd_p'], bh['uebd_p'])
    tot_rend = _sum_vals(pa['rend'], bh['rend'])
    tot_rend_p = _sum_vals(pa['rend_p'], bh['rend_p'])

    # Resolución de color para la fila TOTAL
    backend_tot_color_op = _get_kpi_color(
        kpis,
        'mezcla_total_req',
        'mezcla_total_op_req',
        'mezcla_total_op',
        'mezcla_total_req_plan',
    )
    tot_color_op = _resolve_op_req_color(op=tot_op, req=tot_req, kpi_color=backend_tot_color_op)

    tot_color_disp = _get_kpi_color(kpis, 'mezcla_total_disp')
    tot_color_uebd = _get_kpi_color(kpis, 'mezcla_total_uebd')
    tot_color_rend = _get_kpi_color(kpis, 'mezcla_total_rend')

    # Fila TOTAL
    kpis_copy['mezcla_total_op_req'] = _fmt_pair(
        _fmt_int(tot_op), _fmt_int(tot_req), is_total=True, color=tot_color_op
    )
    kpis_copy['mezcla_total_disp'] = _fmt_pair(
        _fmt_int(tot_disp), _fmt_int(tot_disp_p), is_total=True, color=tot_color_disp
    )
    kpis_copy['mezcla_total_uebd'] = _fmt_pair(
        _fmt_int(tot_uebd), _fmt_int(tot_uebd_p), is_total=True, color=tot_color_uebd
    )
    kpis_copy['mezcla_total_rend'] = _fmt_pair(
        _fmt_rend(tot_rend), _fmt_rend(tot_rend_p), is_total=True, color=tot_color_rend
    )

    return map_compact_table(
        definition=MEZCLA_TABLE_DEFINITION,
        kpis=kpis_copy,
    )


def build_mezcla_summary_mapper(*args, **kwargs) -> Any:
    return None


def build_mezcla_metrics_mapper(*args, **kwargs) -> Any:
    return None