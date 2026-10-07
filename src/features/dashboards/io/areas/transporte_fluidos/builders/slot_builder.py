from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import TransporteFluidosIds


def build_str_container():
    return build_slot_container(component_id=TransporteFluidosIds.STR, class_name='')


def build_stc_container():
    return build_slot_container(component_id=TransporteFluidosIds.STC, class_name='')


def build_tranque_container():
    return build_slot_container(component_id=TransporteFluidosIds.TRANQUE, class_name='')


def build_sta_container():
    return build_slot_container(component_id=TransporteFluidosIds.STA, class_name='')


def build_transporte_fluidos_ready_flag():
    return build_slot_ready_flag_container(id_flag=TransporteFluidosIds.READY_FLAG)
