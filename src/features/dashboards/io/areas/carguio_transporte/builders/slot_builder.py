from __future__ import annotations

from src.shared.ui.display.slot_container import (
    build_slot_container,
    build_slot_ready_flag_container,
)

from ..ids import CarguioTransporteIds


def build_gestion_carguio_container():
    return build_slot_container(component_id=CarguioTransporteIds.GESTION_CARGUIO, class_name='')


def build_carguio_transporte_ready_flag():
    return build_slot_ready_flag_container(id_flag=CarguioTransporteIds.READY_FLAG)
