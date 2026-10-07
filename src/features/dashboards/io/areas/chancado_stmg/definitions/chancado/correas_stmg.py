from __future__ import annotations

from src.shared.ui.components.metrics import StandardMetricDefinition

from ...components.correa_stmg import CorreaStmgDefinition, CorreaStmgGroupDefinition

CORREAS_STMG_DEFINITION: CorreaStmgGroupDefinition = CorreaStmgGroupDefinition(
    correas=(
        CorreaStmgDefinition(label='CV005', correa_state_key='estado_correa_005_inst'),
        CorreaStmgDefinition(label='CV006', correa_state_key='estado_correa_006_inst'),
        CorreaStmgDefinition(label='CV007', correa_state_key='estado_correa_007_inst'),
    ),
    metrics=(
        StandardMetricDefinition(
            label='Transp. STMG',
            kpi_key='transportado_stmg_inst',
            color_key='',
            unit='TPH',
            font_size_class_name='fs-io-200',
            container_class_name='app-border-bottom pt-1 w-100',
        ),
    ),
)
