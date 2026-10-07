from __future__ import annotations

from src.shared.ui.components.compact_table import (
    CompactTableCellDefinition,
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableRowDefinition,
)


def _leyes_summary_rows() -> tuple[CompactTableRowDefinition, ...]:
    parameters = [
        {'key': 'ley_cu', 'label': 'Ley CuT %', 'tag': 'ley_cu_{0}'},
        {'key': 'ley_mo', 'label': 'Ley Mo ppm', 'tag': 'ley_mo_{0}'},
        {'key': 'ley_conc', 'label': 'Ley Conc %', 'tag': 'ley_conc_{0}'},
        {'key': 'dureza', 'label': 'Dureza %', 'tag': 'dureza_{0}'},
        {'key': 'recuperacion', 'label': 'Recuperación', 'tag': 'recuperacion_{0}'},
        {'key': 'axb', 'label': 'AxB Alim', 'tag': 'axb_{0}'},
        {'key': 'arsenico', 'label': 'Arsénico ppm', 'tag': 'arsenico_{0}'},
    ]

    return tuple(
        [
            CompactTableRowDefinition.data(
                key=parameter.get('key'),
                cells={
                    'item': CompactTableCellDefinition.static(
                        value=parameter.get('label'), align='start'
                    ),
                    'hora': CompactTableCellDefinition.from_key(
                        key=parameter.get('tag', '').format('hora'), align='end'
                    ),
                    'turno': CompactTableCellDefinition.from_key(
                        key=parameter.get('tag', '').format('turno'), align='end'
                    ),
                    'dia': CompactTableCellDefinition.from_key(
                        key=parameter.get('tag', '').format('dia'), align='end'
                    ),
                    'plan': CompactTableCellDefinition.from_key(
                        key=parameter.get('tag', '').format('plan'), align='end'
                    ),
                },
            )
            for parameter in parameters
        ]
    )


LEYES_SUMMARY_DEFINITION: CompactTableDefinition = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='item',
            label='',
            align='start',
            width='35%',
            is_row_header=True,
        ),
        CompactTableColumnDefinition(
            key='hora',
            label='HORA',
            align='end',
            width='16.25%',
        ),
        CompactTableColumnDefinition(
            key='turno',
            label='TURNO',
            align='end',
            width='16.25%',
        ),
        CompactTableColumnDefinition(
            key='dia',
            label='DÍA',
            align='end',
            width='16.25%',
        ),
        CompactTableColumnDefinition(
            key='plan',
            label='PLAN',
            align='end',
            width='16.25%',
        ),
    ),
    rows=_leyes_summary_rows(),
)
