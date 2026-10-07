from __future__ import annotations

from src.shared.ui.components.compact_table import (
    CompactTableCellDefinition,
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableRowDefinition,
)

_FLOTAS = [
    {'key': 'pa', 'label': 'PA'},
    {'key': 'bh', 'label': 'BH'},
    {'key': 'total', 'label': 'TOTAL'},
]


def _build_rows() -> tuple[CompactTableRowDefinition, ...]:
    rows = []
    for f in _FLOTAS:
        k = f['key']
        is_total = k == 'total'
        rows.append(
            CompactTableRowDefinition.data(
                key=k,
                cells={
                    'flota': CompactTableCellDefinition.static(
                        value=f['label'],
                        align='start',
                        emphasized=True,
                    ),
                    'op_req': CompactTableCellDefinition.from_key(
                        key=f'mezcla_{k}_op_req',
                        align='center',
                        emphasized=is_total,
                    ),
                    'disp': CompactTableCellDefinition.from_key(
                        key=f'mezcla_{k}_disp',
                        align='center',
                        emphasized=is_total,
                    ),
                    'uebd': CompactTableCellDefinition.from_key(
                        key=f'mezcla_{k}_uebd',
                        align='center',
                        emphasized=is_total,
                    ),
                    'rend': CompactTableCellDefinition.from_key(
                        key=f'mezcla_{k}_rend',
                        align='center',
                        emphasized=is_total,
                    ),
                },
            )
        )
    return tuple(rows)


MEZCLA_TABLE_DEFINITION = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='flota',
            label='FLOTA',
            align='start',
            width='16%', 
            is_row_header=True,
        ),
        CompactTableColumnDefinition(
            key='op_req',
            label='OP / REQ',
            align='center',
            width='16%',  
        ),
        CompactTableColumnDefinition(
            key='disp',
            label='DISP. (%)',
            align='center',
            width='18%',
        ),
        CompactTableColumnDefinition(
            key='uebd',
            label='UEBD (%)',
            align='center',
            width='18%',
        ),
        CompactTableColumnDefinition(
            key='rend',
            label='REND. (kt/h)',
            align='center',
            width='25%', 
        ),
    ),
    rows=_build_rows(),
)