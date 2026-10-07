from __future__ import annotations

from typing import Any

from ..definitions.alarm_image_configuration_definition import (
    ALARM_IMAGE_CONFIGURATION_ADMIN_DEFINITION,
)
from .admin_rows_data_accessor import AdminRowsDataAccessor


class AlarmImageConfigurationRepository:
    def __init__(
        self,
        *,
        data_accessor: AdminRowsDataAccessor | None = None,
    ) -> None:
        self._data_accessor = data_accessor or AdminRowsDataAccessor()

    def load_rows(self) -> list[dict[str, Any]]:
        return self._data_accessor.load_rows(
            definition=ALARM_IMAGE_CONFIGURATION_ADMIN_DEFINITION,
        )

    def save_rows(self, rows: list[dict[str, Any]]) -> None:
        normalized_rows = self._normalize_rows(rows)

        self._data_accessor.save_rows(
            definition=ALARM_IMAGE_CONFIGURATION_ADMIN_DEFINITION,
            rows=normalized_rows,
        )

    @staticmethod
    def _normalize_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        normalized_rows = []

        for row in rows:
            message_group_key = str(row.get('message_group_key') or '').strip()
            image_key = str(row.get('image_key') or '').strip()

            if not message_group_key or not image_key:
                continue

            normalized_rows.append(
                {
                    'message_group_key': message_group_key,
                    'image_key': image_key,
                    'order': int(row.get('order') or 1),
                    'bundle_key': str(row.get('bundle_key') or 'bundle_001').strip(),
                    'bundle_hash': str(row.get('bundle_hash') or '').strip(),
                    'thumb_path': str(row.get('thumb_path') or '').strip(),
                    'full_path': str(row.get('full_path') or '').strip(),
                    'thumb_mime_type': str(row.get('thumb_mime_type') or 'image/webp').strip(),
                    'full_mime_type': str(row.get('full_mime_type') or '').strip(),
                    'content_hash': str(row.get('content_hash') or '').strip(),
                }
            )

        normalized_rows.sort(
            key=lambda item: (
                item['message_group_key'].lower(),
                item['order'],
                item['image_key'],
            )
        )

        return normalized_rows
