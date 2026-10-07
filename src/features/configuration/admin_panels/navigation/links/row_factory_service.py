from __future__ import annotations

from typing import Any
from uuid import uuid4


class NavigationLinkRowFactoryService:
    @staticmethod
    def build_new_row(
        *,
        current_rows: list[dict[str, Any]] | None,
    ) -> dict[str, Any]:
        rows = [row for row in current_rows or [] if isinstance(row, dict)]

        return {
            'link_id': str(uuid4()),
            'label': '',
            'path': '',
            'link_type': '',
            'parent_group_id': '',
            'icon_source': '',
            'icon': '',
            'order': NavigationLinkRowFactoryService._resolve_next_order(
                rows=rows,
            ),
            'new_tab': False,
            'visible_in_menu': True,
            'is_active': True,
            'force_reload': False,
            'allow_profiles': '',
        }

    @staticmethod
    def _resolve_next_order(
        *,
        rows: list[dict[str, Any]],
    ) -> int:
        orders: list[int] = []

        for row in rows:
            try:
                order = int(row.get('order') or 0)
            except Exception:
                continue

            if order > 0:
                orders.append(order)

        if not orders:
            return 10

        return max(orders) + 10
