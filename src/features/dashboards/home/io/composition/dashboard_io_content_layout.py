from __future__ import annotations

from src.features.alarm_monitor.layout.alarm_panel_layout import build_alarm_panel_layout
from src.features.dashboards.io.areas import (
    build_carguio_section,
    build_carguio_transporte_section,
    build_chancado_stmg_section,
    build_flotacion_section,
    build_general_mina_section,
    build_molienda_section,
    build_puerto_section,
    build_stock_chacay_section,
    build_transporte_fluidos_section,
    build_transporte_section,
    build_header_section
)


def build_dashboard_io_content_layout() -> dict:
    return {
        'header_region': [build_header_section()],
        'alarm_region': [build_alarm_panel_layout()],
        'first_region': [build_general_mina_section()],
        'second_region': [build_carguio_section()],
        'second_third_middle_region': [build_carguio_transporte_section()],
        'third_region': [build_transporte_section()],
        'fourth_region': [build_chancado_stmg_section()],
        'fifth_region': [build_stock_chacay_section()],
        'sixth_region': [build_molienda_section()],
        'seventh_region': [build_flotacion_section()],
        'eighth_region': [build_transporte_fluidos_section()],
        'ninth_region': [build_puerto_section()],
    }


