from __future__ import annotations

from typing import Any


class AlarmRuntimeSnapshotResolver:
    ACTIVE_COLLECTION_KEYS = (
        'operator_view',
        'operator_pool',
    )

    TRACKING_COLLECTION_KEYS = ('tracking_view',)

    ALL_COLLECTION_KEYS = (
        *ACTIVE_COLLECTION_KEYS,
        *TRACKING_COLLECTION_KEYS,
    )

    @classmethod
    def find_active_alarm(
        cls,
        *,
        snapshot: dict[str, Any],
        alarm_id: str,
    ) -> dict[str, Any] | None:
        return cls._find_alarm_in_collections(
            snapshot=snapshot,
            alarm_id=alarm_id,
            collection_keys=cls.ACTIVE_COLLECTION_KEYS,
        )

    @classmethod
    def find_any_alarm(
        cls,
        *,
        snapshot: dict[str, Any],
        alarm_id: str,
    ) -> dict[str, Any] | None:
        return cls._find_alarm_in_collections(
            snapshot=snapshot,
            alarm_id=alarm_id,
            collection_keys=cls.ALL_COLLECTION_KEYS,
        )

    @staticmethod
    def get_snapshot_timestamp(
        *,
        snapshot: dict[str, Any],
    ) -> str | None:
        value = snapshot.get('snapshot_timestamp')

        if value is None:
            return None

        normalized = str(value).strip()
        return normalized or None

    @classmethod
    def _find_alarm_in_collections(
        cls,
        *,
        snapshot: dict[str, Any],
        alarm_id: str,
        collection_keys: tuple[str, ...],
    ) -> dict[str, Any] | None:
        target_alarm_id = str(alarm_id or '').strip()

        if not target_alarm_id:
            return None

        for collection_key in collection_keys:
            collection = snapshot.get(collection_key) or []

            if not isinstance(collection, list):
                continue

            alarm = cls._find_alarm_in_collection(
                collection=collection,
                alarm_id=target_alarm_id,
            )

            if alarm is not None:
                return alarm

        return None

    @staticmethod
    def _find_alarm_in_collection(
        *,
        collection: list[Any],
        alarm_id: str,
    ) -> dict[str, Any] | None:
        for item in collection:
            if not isinstance(item, dict):
                continue

            current_alarm_id = str(item.get('alarm_id') or '').strip()

            if current_alarm_id == alarm_id:
                return item

        return None
