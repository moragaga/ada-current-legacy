from __future__ import annotations

from src.shared.ui.components.compact_table import (
    CompactTableCellDefinition,
    CompactTableColumnDefinition,
    CompactTableDefinition,
    CompactTableRowDefinition,
)

_EQUIPOS = [
    {'key': 'bulldozer', 'label': 'Bulldozer'},
    {'key': 'wheeldozer', 'label': 'Wheeldozer'},
    {'key': 'motoniveladora', 'label': 'Motoniveladora'},
    {'key': 'excavadora', 'label': 'Excavadora'},
    {'key': 'aljibe', 'label': 'Aljibe'},
    {'key': 'cargador_frontal', 'label': 'Cargador Frontal'},
    {'key': 'total', 'label': 'TOTAL'},
]


def _build_rows() -> tuple[CompactTableRowDefinition, ...]:
    rows = []
    for eq in _EQUIPOS:
        is_total = eq['key'] == 'total'
        rows.append(
            CompactTableRowDefinition.data(
                key=eq['key'],
                cells={
                    'equipo': CompactTableCellDefinition.static(
                        value=eq['label'],
                        align='start',
                        emphasized=is_total,
                    ),
                    'op': CompactTableCellDefinition.from_key(
                        key=f"eq_serv_{eq['key']}_op",
                        align='center',
                        emphasized=is_total,
                    ),
                    'disp': CompactTableCellDefinition.from_key(
                        key=f"eq_serv_{eq['key']}_disp",
                        align='center',
                        emphasized=is_total,
                    ),
                    'fs': CompactTableCellDefinition.from_key(
                        key=f"eq_serv_{eq['key']}_fs",
                        align='center',
                        emphasized=is_total,
                    ),
                },
            )
        )
    return tuple(rows)


EQUIPOS_SERVICIO_TABLE_DEFINITION = CompactTableDefinition(
    columns=(
        CompactTableColumnDefinition(
            key='equipo',
            label='Equipo',
            align='start',
            width='34%',
            is_row_header=True,
        ),
        CompactTableColumnDefinition(
            key='op',
            label='Operando',
            align='center',
            width='22%',
        ),
        CompactTableColumnDefinition(
            key='disp',
            label='Disponibles',
            align='center',
            width='22%',
        ),
        CompactTableColumnDefinition(
            key='fs',
            label='F.S',
            align='center',
            width='22%',
        ),
    ),
    rows=_build_rows(),
)