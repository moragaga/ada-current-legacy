from __future__ import annotations

from src.shared.ui.components.compact_table import (
    CompactTableCellDefinition,
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableRowDefinition,
)


def _global_production_summary_rows() -> tuple[CompactTableRowDefinition, ...]:
    parameters = [
        {'key': 'alim', 'label': 'Alim.', 'tag': 'alim_{0}'},
        {'key': 'transp', 'label': 'Transp.', 'tag': 'transp_{0}'},
    ]

    return tuple(
        [
            CompactTableRowDefinition.data(
                key=parameter.get('key'),
                cells={
                    'item': CompactTableCellDefinition.static(
                        value=parameter.get('label'), align='start'
                    ),
                    'real': CompactTableCellDefinition.from_key(
                        key=parameter.get('tag', '').format('hora'), align='end'
                    ),
                    'plan': CompactTableCellDefinition.from_key(
                        key=parameter.get('tag', '').format('turno'), align='end'
                    ),
                    'proy': CompactTableCellDefinition.from_key(
                        key=parameter.get('tag', '').format('dia'), align='end'
                    ),
                },
            )
            for parameter in parameters
        ]
    )


GLOBAL_PRODUCTION_SUMMARY_DEFINITION: CompactTableDefinition = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='item',
            label='',
            align='start',
            width='28%',
            is_row_header=True,
        ),
        CompactTableColumnDefinition(
            key='real',
            label='REAL',
            align='end',
            width='24%',
        ),
        CompactTableColumnDefinition(
            key='plan',
            label='PLAN',
            align='end',
            width='24%',
        ),
        CompactTableColumnDefinition(
            key='proy',
            label='PROY',
            align='end',
            width='24%',
        ),
    ),
    rows=_global_production_summary_rows(),
)
