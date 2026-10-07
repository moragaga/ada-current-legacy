from __future__ import annotations

from typing import Any

from ..constants import (
    GLOBAL_MESSAGES_BUCKET,
    MESSAGE_GROUP_BUCKET_PREFIX,
)


class AlarmMessageBucketService:
    @staticmethod
    def resolve_message_groups_from_alarm_rows(
        *,
        alarm_rows: list[dict[str, Any]],
    ) -> set[str]:
        return {
            str(row.get('message_group_key') or '').strip()
            for row in alarm_rows
            if str(row.get('message_group_key') or '').strip()
        }

    @staticmethod
    def build_bucket_options(
        *,
        alarm_rows: list[dict[str, Any]],
        message_configuration: dict[str, Any],
    ) -> list[dict[str, str]]:
        groups_from_alarms = AlarmMessageBucketService.resolve_message_groups_from_alarm_rows(
            alarm_rows=alarm_rows,
        )

        configured_groups = {
            str(group_key or '').strip()
            for group_key in (message_configuration.get('messages_by_group_key') or {}).keys()
            if str(group_key or '').strip()
        }

        all_groups = sorted(groups_from_alarms | configured_groups)

        options = [
            {
                'label': 'Globales',
                'value': GLOBAL_MESSAGES_BUCKET,
            }
        ]

        for group in all_groups:
            label = group

            if group not in groups_from_alarms:
                label = f'{group} (sin alarmas vinculadas)'

            options.append(
                {
                    'label': label,
                    'value': f'{MESSAGE_GROUP_BUCKET_PREFIX}{group}',
                }
            )

        return options

    @staticmethod
    def get_rows_for_bucket(
        *,
        selected_bucket: str | None,
        message_configuration: dict[str, Any],
    ) -> list[dict[str, Any]]:
        if not selected_bucket:
            return []

        if selected_bucket == GLOBAL_MESSAGES_BUCKET:
            rows = list(message_configuration.get('global_messages') or [])
            return AlarmMessageBucketService._sort_rows(rows=rows)

        if selected_bucket.startswith(MESSAGE_GROUP_BUCKET_PREFIX):
            message_group = selected_bucket.removeprefix(MESSAGE_GROUP_BUCKET_PREFIX)
            messages_by_key = message_configuration.get('messages_by_group_key') or {}
            rows = list(messages_by_key.get(message_group) or [])
            return AlarmMessageBucketService._sort_rows(rows=rows)

        return []

    @staticmethod
    def _sort_rows(
        *,
        rows: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        return sorted(
            [row for row in rows if isinstance(row, dict)],
            key=lambda row: (
                int(row.get('sort_order') or 0),
                str(row.get('message') or ''),
            ),
        )
