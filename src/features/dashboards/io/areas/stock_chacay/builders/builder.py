from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import StockChacayIds


def build_stockpile_chacay_container():
    return build_slot_container(component_id=StockChacayIds.STOCKPILE_CHACAY, class_name='')


def build_tendencia_alimentado_container():
    return build_slot_container(component_id=StockChacayIds.TENDENCIA_ALIMENTADO, class_name='')


def build_stock_chacay_ready_flag():
    return build_slot_ready_flag_container(id_flag=StockChacayIds.READY_FLAG)
