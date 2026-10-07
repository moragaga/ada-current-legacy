from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.shared.infrastructure.cosmos.service import CosmosService

from ...core.models import AlarmManagementRuntimeInputs
from ..services import TwoTurnShiftEndProvider
from ..settings import AlarmManagementRuntimeSettings


class CosmosAlarmManagementRuntimeInputProvider:
    def __init__(
        self,
        *,
        cosmos_service: CosmosService,
        settings: AlarmManagementRuntimeSettings,
        shift_end_provider: TwoTurnShiftEndProvider,
    ) -> None:
        self._cosmos_service = cosmos_service
        self._settings = settings
        self._shift_end_provider = shift_end_provider

    def load_inputs(self) -> AlarmManagementRuntimeInputs:
        now_utc = datetime.now(timezone.utc)

        runtime_snapshot = self._load_runtime_snapshot()
        alarm_configuration_rows = self._load_alarm_configuration_rows()
        message_configuration = self._load_message_configuration()
        managed_alarm_ids = self._load_managed_alarm_ids(
            runtime_snapshot=runtime_snapshot,
        )

        shift_end_utc = self._shift_end_provider.get_shift_end_utc(
            now_utc=now_utc,
        )

        return AlarmManagementRuntimeInputs(
            runtime_snapshot=runtime_snapshot,
            alarm_configuration_rows=alarm_configuration_rows,
            message_configuration=message_configuration,
            managed_alarm_ids=managed_alarm_ids,
            now_utc=now_utc,
            shift_end_utc=shift_end_utc,
        )

    def _load_runtime_snapshot(self) -> dict[str, Any]:
        document = self._cosmos_service.read_item(
            container_name=self._settings.runtime_snapshot_container_name,
            item_id=self._settings.runtime_snapshot_document_id,
            partition_key_value=self._settings.runtime_snapshot_partition_key_value,
        )

        if not isinstance(document, dict):
            return {}

        return document

    def _load_alarm_configuration_rows(self) -> list[dict[str, Any]]:
        document = self._cosmos_service.read_item(
            container_name=self._settings.alarm_configuration_container_name,
            item_id=self._settings.alarm_configuration_document_id,
            partition_key_value=self._settings.alarm_configuration_partition_key_value,
        )

        if not isinstance(document, dict):
            return []

        data = document.get('data')

        if not isinstance(data, list):
            return []

        return [row for row in data if isinstance(row, dict)]

    def _load_message_configuration(self) -> dict[str, Any]:
        default_configuration = {
            'schema_version': 1,
            'global_messages': [],
            'messages_by_group_key': {},
        }

        document = self._cosmos_service.read_item(
            container_name=self._settings.message_configuration_container_name,
            item_id=self._settings.message_configuration_document_id,
            partition_key_value=self._settings.message_configuration_partition_key_value,
        )

        if not isinstance(document, dict):
            return default_configuration

        data = document.get('data')

        if not isinstance(data, dict):
            return default_configuration

        global_messages = data.get('global_messages')
        messages_by_group_key = data.get('messages_by_group_key')

        if not isinstance(global_messages, list):
            data['global_messages'] = []

        if not isinstance(messages_by_group_key, dict):
            data['messages_by_group_key'] = {}

        return data

    def _load_managed_alarm_ids(
        self,
        *,
        runtime_snapshot: dict[str, Any],
    ) -> set[str]:
        managed_alarm_ids = set()

        managed_alarm_ids.update(self._load_pending_action_alarm_ids())
        managed_alarm_ids.update(
            self._load_tracking_managed_alarm_ids(
                runtime_snapshot=runtime_snapshot,
            )
        )

        return managed_alarm_ids

    def _load_pending_action_alarm_ids(self) -> set[str]:
        query = """
        SELECT c.alarm_id
        FROM c
        WHERE c.status = @status
        """

        items = self._cosmos_service.query_items(
            container_name=self._settings.action_container_name,
            query=query,
            parameters=[
                {
                    'name': '@status',
                    'value': 'pending',
                }
            ],
        )

        alarm_ids: set[str] = set()

        for item in items:
            if not isinstance(item, dict):
                continue

            alarm_id = str(item.get('alarm_id') or '').strip()

            if alarm_id:
                alarm_ids.add(alarm_id)

        return alarm_ids

    @staticmethod
    def _load_tracking_managed_alarm_ids(
        *,
        runtime_snapshot: dict[str, Any],
    ) -> set[str]:
        tracking_view = runtime_snapshot.get('tracking_view') or []

        if not isinstance(tracking_view, list):
            return set()

        alarm_ids: set[str] = set()

        for item in tracking_view:
            if not isinstance(item, dict):
                continue

            status = str(item.get('status') or '').strip().upper()

            if status not in {'MANAGED', 'INACTIVE'}:
                continue

            alarm_id = str(item.get('alarm_id') or '').strip()

            if alarm_id:
                alarm_ids.add(alarm_id)

        return alarm_ids
