from __future__ import annotations

import os


class AlarmImageUrlService:
    def __init__(
        self,
        *,
        public_asset_url_prefix: str | None = None,
    ) -> None:
        self._public_asset_url_prefix = (
            public_asset_url_prefix
            or os.getenv(
                'MANAGED_ALARM_IMAGE_PUBLIC_ASSET_URL_PREFIX',
                '/assets/data/managed_alarm_images/public',
            )
        ).rstrip('/')

    def build_public_url(self, path: str) -> str:
        normalized_path = str(path or '').strip().strip('/')

        if not normalized_path:
            return ''

        if normalized_path.startswith('/assets/'):
            return normalized_path

        return f'{self._public_asset_url_prefix}/{normalized_path}'
