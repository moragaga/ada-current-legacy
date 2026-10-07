from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import TransporteIds


def build_transporte_global_container():
    return build_slot_container(component_id=TransporteIds.TRANSPORTE_GLOBAL, class_name='')


def build_no_operativo_container():
    return build_slot_container(component_id=TransporteIds.NO_OPERATIVO, class_name='')


def build_tiempos_colas_container():
    return build_slot_container(component_id=TransporteIds.TIEMPOS_COLAS, class_name='')


def build_transporte_ready_flag():
    return build_slot_ready_flag_container(id_flag=TransporteIds.READY_FLAG)
