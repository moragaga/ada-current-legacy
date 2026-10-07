from __future__ import annotations

from src.shared.ui.charts.feeders import FeederDefinition, FeedersDefinition
from src.shared.ui.charts.stockpile_mina import (
    StockpileMinaDefinition,
    StockpileMinaDetailDefinition,
)
from src.shared.ui.components.compact_table import (
    CompactTableCellDefinition,
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableRowDefinition,
)

from ...components.chancador import ChancadorDefinition


def _build_chancador_summary_row(
    *,
    chancador_number: str,
) -> CompactTableRowDefinition:
    return CompactTableRowDefinition.data(
        key=f'ch{chancador_number}',
        cells={
            'item': CompactTableCellDefinition.static(
                value=f'CH{chancador_number}',
                align='start',
            ),
            'tph': CompactTableCellDefinition.from_key(
                key=(f'alimentacion_chancador_{chancador_number}_real_hora_movil_inst'),
                align='end',
            ),
            'min_atollo': CompactTableCellDefinition.from_key(
                key=(f'duracion_total_real_atollos_chancador_{chancador_number}_current_inst'),
                align='end',
            ),
            'mm_poste': CompactTableCellDefinition.from_key(
                key=f'altura_poste_chancador_{chancador_number}_inst',
                align='end',
            ),
        },
    )


def _chancadores_summary_rows() -> tuple[CompactTableRowDefinition, ...]:
    return tuple(
        _build_chancador_summary_row(chancador_number=chancador_number)
        for chancador_number in ('1', '2')
    )


CHANCADORES_DEFINITION: tuple[ChancadorDefinition, ...] = (
    ChancadorDefinition(
        label='CH1',
        chancado_state_key='estado_chancador_1_inst',
        chancado_value_key='alimentacion_real_chancador_1_inst',
        chancado_color_key='',
        chancado_unit='t/h',
        atollo_state_key='atollo_en_curso_chancador_1_inst',
    ),
    ChancadorDefinition(
        label='CH2',
        chancado_state_key='estado_chancador_2_inst',
        chancado_value_key='alimentacion_real_chancador_2_inst',
        chancado_color_key='',
        chancado_unit='t/h',
        atollo_state_key='atollo_en_curso_chancador_2_inst',
        mirror=True
    ),
)

CHANCADORES_SUMMARY_DEFINITION: CompactTableDefinition = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='item',
            label='',
            align='start',
            width='16%',
            is_row_header=True,
        ),
        CompactTableColumnDefinition(
            key='tph',
            label='RENDIMIENTO',
            align='end',
            width='28%',
        ),
        CompactTableColumnDefinition(
            key='min_atollo',
            label='MIN. ATOLLO',
            align='end',
            width='28%',
        ),
        CompactTableColumnDefinition(
            key='mm_poste',
            label='MM. POSTE',
            align='end',
            width='28%',
        ),
    ),
    rows=_chancadores_summary_rows(),
)

STOCKPILE_MINA_DEFINITION: StockpileMinaDefinition = StockpileMinaDefinition(
    piles=(
        StockpileMinaDetailDefinition(
            percentage_key='altura_pila_stockpile_mina_1_p_inst',
            meters_key='altura_pila_stockpile_mina_1_m_inst',
        ),
        StockpileMinaDetailDefinition(
            percentage_key='altura_pila_stockpile_mina_2_p_inst',
            meters_key='altura_pila_stockpile_mina_2_m_inst',
        ),
    )
)

FEEDERS_DEFINITION: FeedersDefinition = FeedersDefinition(
    feeders=(
        FeederDefinition(
            label='5',
            value_key='velocidad_feeder_005_inst',
            color_key='',
        ),
        FeederDefinition(
            label='6',
            value_key='velocidad_feeder_006_inst',
            color_key='',
        ),
        FeederDefinition(
            label='7',
            value_key='velocidad_feeder_007_inst',
            color_key='',
        ),
        FeederDefinition(
            label='8',
            value_key='velocidad_feeder_008_inst',
            color_key='',
        ),
    )
)
