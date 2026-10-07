from __future__ import annotations

from src.shared.ui.components.metrics import (
    DualMetricDefinition,
    StandardMetricDefinition,
)

_FS_COLUMN = 'fs-io-200'

# Clases utilitarias: peso normal y color gris claro (según tu framework CSS)
_SECOND_VAL_CLASS = 'text-muted fw-normal'   # o 'app-text-muted font-weight-normal'
_FIRST_VAL_CLASS = 'fw-bold'                 # asegura que el valor real conserve la negrita

TRANSPORTE_GLOBAL_TURNO_DEFINITION: tuple[
    DualMetricDefinition | StandardMetricDefinition, ...
] = (
    DualMetricDefinition(
        label='Rendimiento (t/h)',
        first_kpi_key='ig_mina_rendcaex_turno_real',
        second_kpi_key='ig_mina_rendcaex_turno_plan',
        first_color_key='ig_mina_rendcaex_turno_real_color',
        first_value_class_name=_FIRST_VAL_CLASS,
        second_value_class_name=_SECOND_VAL_CLASS,
        first_unit='',
        second_unit='',
        divider_value=' / ',
        font_size_class_name=_FS_COLUMN,
    ),
    DualMetricDefinition(
        label='UEBD (%)',
        first_kpi_key='ig_mina_uebdcaex_turno_real',
        second_kpi_key='ig_mina_uebdcaex_turno_plan',
        first_color_key='ig_mina_uebdcaex_turno_real_color',
        first_value_class_name=_FIRST_VAL_CLASS,
        second_value_class_name=_SECOND_VAL_CLASS,
        first_unit='',
        second_unit='',
        divider_value=' / ',
        font_size_class_name=_FS_COLUMN,
    ),
    DualMetricDefinition(
        label='Ciclo (min)',
        first_kpi_key='ciclo_transporte_real_inst',
        second_kpi_key='ig_mina_tiempo_ciclo_caex_turno_plan',
        first_color_key='ig_mina_ciclo_transporte_turno_real_color',
        first_value_class_name=_FIRST_VAL_CLASS,
        second_value_class_name=_SECOND_VAL_CLASS,
        first_unit='',
        second_unit='',
        divider_value=' / ',
        font_size_class_name=_FS_COLUMN,
    ),
    DualMetricDefinition(
        label='Velocidad Media (km/h)',
        first_kpi_key='velocidad_media_inst',
        second_kpi_key='ig_mina_velocidad_caex_turno_plan',
        first_color_key='ig_mina_velocidad_media_real_color',
        first_value_class_name=_FIRST_VAL_CLASS,
        second_value_class_name=_SECOND_VAL_CLASS,
        first_unit='',
        second_unit='',
        divider_value=' / ',
        font_size_class_name=_FS_COLUMN,
    ),
    DualMetricDefinition(
        label='Distancia Media (km)',
        first_kpi_key='distancia_media_inst',
        second_kpi_key='ig_mina_distancia_media_caex_turno_plan',
        first_color_key='ig_mina_distancia_media_caex_turno_real_color',
        first_value_class_name=_FIRST_VAL_CLASS,
        second_value_class_name=_SECOND_VAL_CLASS,
        first_unit='',
        second_unit='',
        divider_value=' / ',
        font_size_class_name=_FS_COLUMN,
    ),
)