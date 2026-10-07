from __future__ import annotations

import logging

from .alarm_image_runtime_bundle_sync_service import sync_alarm_image_bundles_now

logger = logging.getLogger(__name__)


def warmup_alarm_image_runtime() -> None:
    try:
        result = sync_alarm_image_bundles_now()

        logger.info(
            '[ALARM_IMAGE_RUNTIME] warmup executed=%s synced=%s skipped=%s failed=%s',
            result.executed,
            result.synced_bundle_keys,
            result.skipped_bundle_keys,
            result.failed_bundle_keys,
        )
    except Exception as exc:
        logger.exception(
            '[ALARM_IMAGE_RUNTIME] warmup failed, app will continue. Error: %s',
            exc,
        )
