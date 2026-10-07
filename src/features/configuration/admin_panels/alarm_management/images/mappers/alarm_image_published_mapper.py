from __future__ import annotations

from typing import Any

from ..services.alarm_image_url_service import AlarmImageUrlService


class AlarmImagePublishedMapper:
    def __init__(
        self,
        *,
        url_service: AlarmImageUrlService,
    ) -> None:
        self._url_service = url_service

    def to_admin_rows(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        result = []

        for row in rows:
            message_group_key = str(row.get('message_group_key') or '').strip()
            image_key = str(row.get('image_key') or '').strip()

            if not message_group_key or not image_key:
                continue

            thumb_path = str(row.get('thumb_path') or '').strip()
            full_path = str(row.get('full_path') or '').strip()

            result.append(
                {
                    'message_group_key': message_group_key,
                    'image_key': image_key,
                    'order': int(row.get('order') or 1),
                    'bundle_key': str(row.get('bundle_key') or '').strip(),
                    'bundle_hash': str(row.get('bundle_hash') or '').strip(),
                    'thumb_url': self._url_service.build_public_url(thumb_path),
                    'full_url': self._url_service.build_public_url(full_path),
                    'thumb_mime_type': str(row.get('thumb_mime_type') or 'image/webp').strip(),
                    'full_mime_type': str(row.get('full_mime_type') or '').strip(),
                    'content_hash': str(row.get('content_hash') or '').strip(),
                }
            )

        result.sort(
            key=lambda item: (
                item['message_group_key'].lower(),
                item['order'],
                item['image_key'],
            )
        )

        return result
