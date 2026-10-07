from __future__ import annotations

from typing import Any

from ..models import AlarmFrontItem
from .generic_alarm_front_context import GenericAlarmFrontContext


class GenericAlarmFrontContextBuilder:
    @classmethod
    def build(
        cls,
        *,
        snapshot: dict[str, Any] | None,
    ) -> GenericAlarmFrontContext:
        if not isinstance(snapshot, dict):
            return GenericAlarmFrontContext(
                snapshot_timestamp='',
            )

        return GenericAlarmFrontContext(
            snapshot_timestamp=cls._text(snapshot.get('snapshot_timestamp')),
            operator_view=cls._map_items(
                items=snapshot.get('operator_view'),
                source_view='operator_view',
            ),
            operator_pool=cls._map_items(
                items=snapshot.get('operator_pool'),
                source_view='operator_pool',
            ),
            tracking_view=cls._map_items(
                items=snapshot.get('tracking_view'),
                source_view='tracking_view',
            ),
            inactive_reactivation_view=cls._map_items(
                items=snapshot.get('inactive_reactivation_view'),
                source_view='inactive_reactivation_view',
            ),
            meta=cls._dict(snapshot.get('meta')),
        )

    @classmethod
    def _map_items(
        cls,
        *,
        items: Any,
        source_view: str,
    ) -> tuple[AlarmFrontItem, ...]:
        if not isinstance(items, list):
            return tuple()

        mapped = [
            AlarmFrontItem.from_dict(
                data=item,
                source_view=source_view,
            )
            for item in items
            if isinstance(item, dict)
        ]

        mapped.sort(
            key=lambda item: (
                item.ranking,
                item.priority_order,
                item.start_timestamp,
                item.alarm_key,
            )
        )

        return tuple(mapped)

    @staticmethod
    def _text(value: Any) -> str:
        if value is None:
            return ''

        return str(value).strip()

    @staticmethod
    def _dict(value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return value

        return {}
