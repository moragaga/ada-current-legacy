from __future__ import annotations

import logging

from .alarm_image_runtime_bundle_sync_service import sync_alarm_image_bundles_if_due

logger = logging.getLogger(__name__)


class AlarmImageAdminRefreshService:
    @staticmethod
    def refresh_runtime_if_due() -> None:
        try:
            result = sync_alarm_image_bundles_if_due()

            logger.info(
                '[ALARM_IMAGE_ADMIN] runtime refresh executed=%s in_progress=%s synced=%s skipped=%s failed=%s',
                result.executed,
                result.in_progress,
                result.synced_bundle_keys,
                result.skipped_bundle_keys,
                result.failed_bundle_keys,
            )

        except Exception as exc:
            logger.exception(
                '[ALARM_IMAGE_ADMIN] runtime refresh failed: %s',
                exc,
            )


def build_alarm_image_admin_refresh_service() -> AlarmImageAdminRefreshService:
    return AlarmImageAdminRefreshService()
