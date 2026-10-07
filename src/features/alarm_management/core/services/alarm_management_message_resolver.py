from __future__ import annotations

from typing import Any

from ..models.alarm_management_message_option import AlarmManagementMessageOption


class AlarmManagementMessageResolver:
    @staticmethod
    def resolve_messages(
        *,
        message_configuration: dict[str, Any],
        message_group_key: str,
    ) -> tuple[AlarmManagementMessageOption, ...]:
        global_messages = message_configuration.get('global_messages') or []
        messages_by_group_key = message_configuration.get('messages_by_group_key') or {}

        group_key = str(message_group_key or '').strip()
        group_messages = messages_by_group_key.get(group_key) or []

        resolved_by_id: dict[str, AlarmManagementMessageOption] = {}

        AlarmManagementMessageResolver._append_messages(
            target=resolved_by_id,
            raw_messages=global_messages,
            source='global',
        )

        AlarmManagementMessageResolver._append_messages(
            target=resolved_by_id,
            raw_messages=group_messages,
            source='group',
        )

        return tuple(
            sorted(
                resolved_by_id.values(),
                key=lambda item: (
                    item.sort_order,
                    item.message,
                    item.message_id,
                ),
            )
        )

    @staticmethod
    def find_message_by_id(
        *,
        messages: tuple[AlarmManagementMessageOption, ...],
        message_id: str | None,
    ) -> AlarmManagementMessageOption | None:
        target_message_id = str(message_id or '').strip()

        if not target_message_id:
            return None

        for message in messages:
            if message.message_id == target_message_id:
                return message

        return None

    @staticmethod
    def _append_messages(
        *,
        target: dict[str, AlarmManagementMessageOption],
        raw_messages: Any,
        source: str,
    ) -> None:
        if not isinstance(raw_messages, list):
            return

        for raw_message in raw_messages:
            if not isinstance(raw_message, dict):
                continue

            message = AlarmManagementMessageOption.from_dict(
                data=raw_message,
                source=source,
            )

            if message is None:
                continue

            if not message.is_active:
                continue

            target[message.message_id] = message
