from __future__ import annotations

import json
import math
from typing import Any
from dash import html

_ALERT_COLORS = {
    'red': '#d93829',      # Rojo
    'yellow': '#d4ac0d',   # Amarillo ámbar
}


def _parse_to_float(val: Any) -> float | None:
    """Parsea a float respetando NaN y None sin forzar cero por defecto."""
    if val is None:
        return None
    if isinstance(val, (int, float)):
        return None if math.isnan(val) else float(val)
    try:
        s = str(val).strip().lower()
        if s in ('none', 'null', 'nan', '', '-'):
            return None
        if '/' in s:
            s = s.split('/')[0].strip()
        s = s.replace('.', '').replace(',', '.')
        num = float(s)
        return None if math.isnan(num) else num
    except Exception:
        return None


def _format_integer(val: Any) -> str:
    """Formatea valores exclusivamente a enteros con punto de miles. Retorna '-' si es NaN o None."""
    num = _parse_to_float(val)
    if num is None:
        return '-'
    return f'{int(round(num)):,}'.replace(',', '.')


def _extract_reporte(data: Any) -> dict:
    if not data:
        return {}

    if isinstance(data, str):
        try:
            parsed = json.loads(data)
            return _extract_reporte(parsed)
        except Exception:
            return {}

    if isinstance(data, dict):
        if 'fases' in data and isinstance(data['fases'], list):
            return data

        for ck in ('metros_perforados_reporte_inst', 'metros_perforados_reporte', 'perforacion_summary_inst'):
            for k, v in data.items():
                if str(k).strip().lower() == ck:
                    found = _extract_reporte(v)
                    if found and found.get('fases'):
                        return found

        for field in ('value', 'parsed_value', 'data', 'kpis', 'records'):
            if field in data:
                found = _extract_reporte(data[field])
                if found and found.get('fases'):
                    return found

        for v in data.values():
            if isinstance(v, (dict, list, str)):
                found = _extract_reporte(v)
                if found and found.get('fases'):
                    return found

    elif isinstance(data, list):
        for item in data:
            found = _extract_reporte(item)
            if found and found.get('fases'):
                return found

    return {}


def build_perforacion_content(kpis: dict | None = None):
    kpis = kpis or {}
    reporte = _extract_reporte(kpis)
    raw_fases = reporte.get('fases', [])

    # Lógica original: únicamente perforadoras con acum_semana > 0
    fases_data = []
    for grupo in raw_fases:
        fase_nombre = grupo.get('fase', '')
        items = grupo.get('items', [])
        valid_items = [
            it for it in items
            if (_parse_to_float(it.get('acum_semana')) or 0.0) > 0
        ]
        if valid_items:
            fases_data.append({
                'fase': fase_nombre,
                'items': valid_items,
            })

    real_num = _parse_to_float(reporte.get('total_acumulado_semanal'))
    if (real_num is None or real_num <= 0) and fases_data:
        item_vals = [
            _parse_to_float(item.get('acum_semana'))
            for f in fases_data
            for item in f.get('items', [])
        ]
        valid_vals = [v for v in item_vals if v is not None]
        real_num = sum(valid_vals) if valid_vals else None

    acum_plan_raw = reporte.get('acumulado_semanal_plan')
    acumulado_plan = _format_integer(acum_plan_raw)

    plan_sem_raw = reporte.get('plan_semanal_total')
    plan_semanal = _format_integer(plan_sem_raw)
    plan_num = _parse_to_float(plan_sem_raw)

    porcentaje_avance = (
        min(100.0, max(0.0, round((real_num / plan_num) * 100, 1)))
        if plan_num and plan_num > 0 and real_num and real_num > 0
        else 0.0
    )

    acumulado_real = _format_integer(real_num)

    # Color dinámico para la barra y la cifra acumulada real
    color_acum_global = reporte.get('color_acum')
    color_alerta_header = (
        _ALERT_COLORS.get(str(color_acum_global).strip().lower())
        if color_acum_global
        else None
    )

    bar_color = color_alerta_header if color_alerta_header else '#535e69'
    real_text_color = color_alerta_header if color_alerta_header else '#111111'

    return html.Div(
        className='w-100',
        style={'padding': '2px 4px', 'boxSizing': 'border-box'},
        children=[
            # --- SECCIÓN SUPERIOR: AVANCE SEMANAL ---
            html.Div(
                children=[
                    html.Div(
                        'Avance Semanal (m)',
                        style={
                            'fontSize': 'clamp(6.8px, 0.8vw, 7.5px)',
                            'fontWeight': '700',
                            'color': '#333333',
                            'letterSpacing': '0.2px',
                            'marginBottom': '2px',
                        },
                    ),
                    html.Div(
                        style={
                            'width': '100%',
                            'height': '6px',
                            'backgroundColor': '#e2e5e9',
                            'borderRadius': '3px',
                            'overflow': 'hidden',
                            'marginBottom': '4px',
                        },
                        children=[
                            html.Div(
                                style={
                                    'width': f'{porcentaje_avance}%',
                                    'height': '100%',
                                    'backgroundColor': bar_color,
                                    'borderRadius': '3px',
                                }
                            )
                        ],
                    ),
                    html.Div(
                        style={
                            'display': 'flex',
                            'justifyContent': 'space-between',
                            'alignItems': 'center',
                            'fontSize': 'clamp(5.8px, 0.7vw, 6.6px)',
                            'paddingBottom': '4px',
                            'marginBottom': '2px',
                        },
                        children=[
                            html.Div(
                                [
                                    html.Span('Acum. semanal  ', style={'color': '#707070'}),
                                    html.Span(
                                        f'{acumulado_real} ',
                                        style={'fontWeight': '700', 'color': real_text_color},
                                    ),
                                    html.Span(f'/{acumulado_plan}', style={'color': '#707070'}),
                                ]
                            ),
                            html.Div(
                                [
                                    html.Span('PS  ', style={'color': '#707070'}),
                                    html.Span(
                                        f'{plan_semanal}',
                                        style={'fontWeight': '700', 'color': '#111111'},
                                    ),
                                ]
                            ),
                        ],
                    ),
                ]
            ),
            # --- TABLA DE PERFORADORAS ---
            html.Div(
                _build_perforacion_table(fases_data),
                style={
                    'maxHeight': '320px',
                    'overflowY': 'auto',
                    'overflowX': 'hidden',
                    'width': '100%',
                },
            ),
        ],
    )


def _render_value_cell(
    real_val: Any,
    plan_val: Any,
    td_style: dict,
    color: str | None = None,
) -> html.Td:
    """Renderiza 'real / plan' en entero, coloreando el valor real según su estado de alerta."""
    real_str = _format_integer(real_val)
    plan_str = _format_integer(plan_val)

    real_color = _ALERT_COLORS.get(str(color).strip().lower(), '#212529') if color else '#212529'

    return html.Td(
        [
            html.Span(real_str, style={'fontWeight': '600', 'color': real_color}),
            html.Span(f' / {plan_str}', style={'color': '#757575', 'fontWeight': '400'}),
        ],
        style=td_style,
    )


def _build_perforacion_table(fases_data: list[dict]):
    border_horizontal = '1px solid #d2d6dc'

    th_style = {
        'fontSize': 'clamp(5.5px, 0.66vw, 6.4px)',
        'fontWeight': '700',
        'color': '#495057',
        'backgroundColor': '#e8e8e8',
        'padding': '3px 2px',
        'textAlign': 'center',
        'border': 'none',
        'whiteSpace': 'nowrap',
        'lineHeight': '1.1',
        'position': 'sticky',
        'top': 0,
        'zIndex': 1,
    }

    td_style = {
        'fontSize': 'clamp(5.8px, 0.7vw, 6.6px)',
        'padding': '2.5px 2px',
        'textAlign': 'center',
        'border': 'none',
        'borderBottom': border_horizontal,
        'whiteSpace': 'nowrap',
        'lineHeight': '1.15',
        'backgroundColor': 'transparent',
    }

    table_rows = []
    for grupo in fases_data:
        fase_nombre = grupo.get('fase', '')
        items = grupo.get('items', [])
        num_items = len(items)

        for idx, item in enumerate(items):
            row_cells = []

            # Agrupador de Fase
            if idx == 0:
                row_cells.append(
                    html.Td(
                        fase_nombre,
                        rowSpan=num_items,
                        style={
                            **td_style,
                            'fontWeight': '700',
                            'verticalAlign': 'middle',
                            'color': '#212529',
                            'backgroundColor': 'transparent',
                        },
                    )
                )

            # Nombre de la Perforadora (con mapeo de PFAR a PF123)
            raw_perfo = str(item.get('perforadora') or item.get('pala') or '-').strip()
            perfo_name = 'PF123' if raw_perfo.upper() == 'PFAR' else raw_perfo

            row_cells.append(
                html.Td(
                    perfo_name,
                    style={
                        **td_style,
                        'fontWeight': '600',
                        'color': '#212529',
                        'backgroundColor': 'transparent',
                    },
                )
            )

            # Día Anterior (Real / Plan) con color condicional
            val_dia = item.get('dia_anterior')
            plan_dia = item.get('plan_diario') if 'plan_diario' in item else item.get('plan_dia_anterior')
            color_dia = item.get('color')
            row_cells.append(
                _render_value_cell(val_dia, plan_dia, td_style, color=color_dia)
            )

            # Acumulado Semana (Real / Plan) con color condicional
            val_acum = item.get('acum_semana')
            plan_acum = (
                item.get('acum_semana_plan')
                if 'acum_semana_plan' in item
                else item.get('plan_acum_semana')
            )
            color_acum = item.get('color_acum')
            row_cells.append(
                _render_value_cell(val_acum, plan_acum, td_style, color=color_acum)
            )

            table_rows.append(html.Tr(children=row_cells))

    return html.Table(
        style={
            'width': '100%',
            'borderCollapse': 'collapse',
            'border': 'none',
            'tableLayout': 'fixed',
        },
        children=[
            html.Thead(
                style={'border': 'none'},
                children=[
                    html.Tr(
                        style={'border': 'none'},
                        children=[
                            html.Th('Fase', style={**th_style, 'width': '15%'}),
                            html.Th('Perfo. (m)', style={**th_style, 'width': '19%'}),
                            html.Th('Dia. Anterior (m)', style={**th_style, 'width': '33%'}),
                            html.Th('Acum. Semana (m)', style={**th_style, 'width': '33%'}),
                        ],
                    )
                ],
            ),
            html.Tbody(children=table_rows),
        ],
    )