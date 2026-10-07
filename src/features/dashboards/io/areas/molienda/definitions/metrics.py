from __future__ import annotations

from src.shared.ui.components.metrics import StandardMetricDefinition

def _build_sag_metrics_definition(*, sag_number: int) -> tuple[StandardMetricDefinition, ...]:
    return (
        StandardMetricDefinition(
            label='F80',
            kpi_key=f'f80_sag_{sag_number}_inst',
            unit='"',
            color_key=f'f80_sag_{sag_number}_color_inst',
            font_size_class_name='fs-io-bc-100',
        ),
        StandardMetricDefinition(
            label='P80',
            kpi_key=f'p80_sag_{sag_number}_inst',
            unit='µm',
            color_key=f'p80_sag_{sag_number}_color_inst',
            font_size_class_name='fs-io-bc-100',
        ),
        StandardMetricDefinition(
            label='Rend.',
            kpi_key=f'tph_sag_{sag_number}_inst',
            unit='t/h',
            color_key=f'tph_sag_{sag_number}_color_inst',
            font_size_class_name='fs-io-bc-100',
        ),
    )

SAG_1_METRICS: tuple[StandardMetricDefinition, ...] = _build_sag_metrics_definition(sag_number=1)
SAG_2_METRICS: tuple[StandardMetricDefinition, ...] = _build_sag_metrics_definition(sag_number=2)
SAG_3_METRICS: tuple[StandardMetricDefinition, ...] = _build_sag_metrics_definition(sag_number=3)
SAG_4_METRICS: tuple[StandardMetricDefinition, ...] = _build_sag_metrics_definition(sag_number=4)
