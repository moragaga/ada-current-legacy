from __future__ import annotations

from typing import Any

from src.app.dependencies import get_cosmos_service

from ..constants import (
    COSMOS_CONTAINER_NAME,
    DOCUMENT_ID,
    PARTITION_KEY,
)
from ..models.managed_alarm_counts import (
    ManagedAlarmAnalyticsCounts,
)


class ManagedAlarmAnalyticsRepository:
    def get_counts(self) -> ManagedAlarmAnalyticsCounts:
        payload = self._read_counts_payload()

        return ManagedAlarmAnalyticsCounts.from_payload(
            payload=payload,
        )

    @staticmethod
    def get_snapshot() -> dict[str, Any]:
        try:
            item = get_cosmos_service().read_item(
                container_name=COSMOS_CONTAINER_NAME,
                item_id=DOCUMENT_ID,
                partition_key_value=PARTITION_KEY,
            )

            if isinstance(item, dict):
                return item

            return {}

        except Exception:
            return {}

    @staticmethod
    def _read_counts_payload() -> dict[str, Any]:
        try:
            results = get_cosmos_service().query_items(
                container_name=COSMOS_CONTAINER_NAME,
                query=(
                    'SELECT VALUE c.artifacts.managed_alarm_counts FROM c WHERE c.id = @document_id'
                ),
                parameters=[
                    {
                        'name': '@document_id',
                        'value': DOCUMENT_ID,
                    },
                ],
            )

            items = list(results or [])

            if not items:
                return {}

            payload = items[0]

            if isinstance(payload, dict):
                return payload

            return {}

        except Exception:
            return {}
