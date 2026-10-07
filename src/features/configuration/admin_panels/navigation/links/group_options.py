from __future__ import annotations

from typing import Any

from src.features.configuration.models import FieldOption


def build_navigation_group_options(
    group_rows: list[dict[str, Any]] | None,
) -> tuple[FieldOption, ...]:
    rows = [row for row in group_rows or [] if isinstance(row, dict)]

    valid_rows = [
        row
        for row in rows
        if str(row.get('group_id') or '').strip() and str(row.get('label') or '').strip()
    ]

    valid_rows.sort(
        key=lambda row: (
            _to_int(row.get('order')),
            str(row.get('label') or ''),
            str(row.get('group_id') or ''),
        )
    )

    options: list[FieldOption] = [
        FieldOption(
            label='Sin grupo',
            value='',
        )
    ]

    for row in valid_rows:
        options.append(
            FieldOption(
                label=str(row.get('label') or '').strip(),
                value=str(row.get('group_id') or '').strip(),
            )
        )

    return tuple(options)


def _to_int(value) -> int:
    try:
        return int(value or 0)
    except Exception:
        return 0
