from __future__ import annotations

from copy import deepcopy
from typing import Any

from ..constants import MESSAGE_CONFIGURATION_SCHEMA_VERSION


class AlarmMessageConfigurationNormalizer:
    @staticmethod
    def normalize(
        *,
        configuration: dict[str, Any] | None,
    ) -> dict[str, Any]:
        normalized = deepcopy(configuration or {})

        normalized['schema_version'] = int(
            normalized.get('schema_version') or MESSAGE_CONFIGURATION_SCHEMA_VERSION
        )

        if not isinstance(normalized.get('global_messages'), list):
            normalized['global_messages'] = []

        if not isinstance(normalized.get('messages_by_group_key'), dict):
            normalized['messages_by_group_key'] = {}

        messages_by_group_key: dict[str, list[dict[str, Any]]] = {}

        for raw_key, raw_messages in normalized['messages_by_group_key'].items():
            message_group_key = str(raw_key or '').strip()

            if not message_group_key:
                continue

            if not isinstance(raw_messages, list):
                messages_by_group_key[message_group_key] = []
                continue

            messages_by_group_key[message_group_key] = [
                item for item in raw_messages if isinstance(item, dict)
            ]

        normalized['messages_by_group_key'] = messages_by_group_key

        return normalized
