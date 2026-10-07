from __future__ import annotations

from typing import Any
from uuid import uuid4


class AlarmMessageRowFactoryService:
    @staticmethod
    def build_new_row(
        *,
        current_rows: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        rows = [row for row in current_rows or [] if isinstance(row, dict)]

        return {
            'message_id': str(uuid4()),
            'message': '',
            'silence_policy_code': 'inherit',
            'allow_silence_edit': True,
            'is_active': True,
            'sort_order': AlarmMessageRowFactoryService._resolve_next_sort_order(
                rows=rows,
            ),
        }

    @staticmethod
    def _resolve_next_sort_order(
        *,
        rows: list[dict[str, Any]],
    ) -> int:
        sort_orders: list[int] = []

        for row in rows:
            try:
                sort_order = int(row.get('sort_order') or 0)
            except Exception:
                continue

            if sort_order > 0:
                sort_orders.append(sort_order)

        if not sort_orders:
            return 10

        return max(sort_orders) + 10
