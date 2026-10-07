from __future__ import annotations

from typing import Any

from ..models import AlarmFrontItem
from .distributed_alarm_front_context import DistributedAlarmFrontContext
from .distributed_alarm_group import DistributedAlarmGroup


class DistributedAlarmFrontContextBuilder:
    H2S_GROUP_KEY = 'h2s'
    H2S_GROUP_LABEL = 'H2S'
    H2S_OPERATOR_BUCKET = 'h2s'
    H2S_ICON_CLASS_NAME = 'bi bi-collection'

    @classmethod
    def build(
        cls,
        *,
        snapshot: dict[str, Any] | None,
    ) -> DistributedAlarmFrontContext:
        if not isinstance(snapshot, dict):
            return DistributedAlarmFrontContext(
                snapshot_timestamp='',
            )

        operator_view = cls._map_items(
            items=snapshot.get('operator_view'),
            source_view='operator_view',
        )
        operator_pool = cls._map_items(
            items=snapshot.get('operator_pool'),
            source_view='operator_pool',
        )

        h2s_items = cls._filter_bucket_items(
            items=(
                *operator_view,
                *operator_pool,
            ),
            operator_bucket=cls.H2S_OPERATOR_BUCKET,
        )

        h2s_group = cls._build_group(
            group_key=cls.H2S_GROUP_KEY,
            group_label=cls.H2S_GROUP_LABEL,
            operator_bucket=cls.H2S_OPERATOR_BUCKET,
            icon_class_name=cls.H2S_ICON_CLASS_NAME,
            items=h2s_items,
        )

        return DistributedAlarmFrontContext(
            snapshot_timestamp=cls._text(snapshot.get('snapshot_timestamp')),
            default_operator_view=cls._exclude_bucket_items(
                items=operator_view,
                operator_bucket=cls.H2S_OPERATOR_BUCKET,
            ),
            default_operator_pool=cls._exclude_bucket_items(
                items=operator_pool,
                operator_bucket=cls.H2S_OPERATOR_BUCKET,
            ),
            tracking_view=cls._map_items(
                items=snapshot.get('tracking_view'),
                source_view='tracking_view',
            ),
            distributed_groups=((h2s_group,) if h2s_group is not None else tuple()),
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

    @classmethod
    def _filter_bucket_items(
        cls,
        *,
        items: tuple[AlarmFrontItem, ...],
        operator_bucket: str,
    ) -> tuple[AlarmFrontItem, ...]:
        target_bucket = cls._text(operator_bucket)

        if not target_bucket:
            return tuple()

        return tuple(item for item in items if item.operator_bucket == target_bucket)

    @classmethod
    def _exclude_bucket_items(
        cls,
        *,
        items: tuple[AlarmFrontItem, ...],
        operator_bucket: str,
    ) -> tuple[AlarmFrontItem, ...]:
        target_bucket = cls._text(operator_bucket)

        if not target_bucket:
            return items

        return tuple(item for item in items if item.operator_bucket != target_bucket)

    @classmethod
    def _build_group(
        cls,
        *,
        group_key: str,
        group_label: str,
        operator_bucket: str,
        icon_class_name: str,
        items: tuple[AlarmFrontItem, ...],
    ) -> DistributedAlarmGroup | None:
        if not items:
            return None

        return DistributedAlarmGroup(
            group_key=group_key,
            group_label=group_label,
            operator_bucket=operator_bucket,
            items=items,
            icon_class_name=icon_class_name,
        )

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
