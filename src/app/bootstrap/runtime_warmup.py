from __future__ import annotations

import logging
import os
import threading

from flask import Flask

logger = logging.getLogger(__name__)


def start_runtime_warmup_tasks(app: Flask) -> None:
    if not _should_start_warmup():
        logger.info('[RUNTIME_WARMUP] Warmup disabled.')
        return

    thread = threading.Thread(
        target=_run_warmup_safely,
        args=(app,),
        name='runtime-warmup',
        daemon=True,
    )
    thread.start()


def _run_warmup_safely(app: Flask) -> None:
    try:
        with app.app_context():
            from src.features.configuration.admin_panels.alarm_management.images.services.alarm_image_runtime_warmup_service import (
                warmup_alarm_image_runtime,
            )

            print('[INFO] [RUNTIME_WARMUP] Warming up alarm image runtime')
            warmup_alarm_image_runtime()

    except Exception as exc:
        logger.exception(
            '[RUNTIME_WARMUP] Warmup failed. App will continue. Error: %s',
            exc,
        )


def _should_start_warmup() -> bool:
    enabled = os.getenv('ENABLE_RUNTIME_WARMUP', 'true').strip().lower()

    if enabled not in {'1', 'true', 'yes', 'y'}:
        return False

    flask_env = os.getenv('FLASK_ENV', '').strip().lower()
    werkzeug_run_main = os.getenv('WERKZEUG_RUN_MAIN')

    if flask_env == 'LOCAL' and werkzeug_run_main != 'true':
        return False

    return True
