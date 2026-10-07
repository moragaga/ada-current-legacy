from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..models.alarm_runtime import AlarmRefreshLock

LOCK_TIMEOUT_SECONDS = 120


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def utcnow_iso() -> str:
    return utcnow().isoformat()


def parse_iso_datetime(value: Any) -> datetime | None:
    if value is None:
        return None

    if not isinstance(value, str):
        value = str(value)

    value = value.strip()
    if not value:
        return None

    try:
        timestamp = datetime.fromisoformat(value)
    except Exception as e:
        print(f'[ERROR] wrong data format for lock_started_at {e}')
        return None

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return timestamp


def build_release_lock() -> AlarmRefreshLock:
    return {'is_running': False, 'started_at': None}


def build_acquire_lock() -> AlarmRefreshLock:
    return {'is_running': True, 'started_at': utcnow_iso()}


def is_lock_expired(lock_data: dict[str, Any] | None) -> bool:
    if not lock_data:
        return False

    if not lock_data.get('is_running', False):
        return False

    started_at = parse_iso_datetime(lock_data.get('started_at'))
    if started_at is None:
        return False

    age_seconds = (utcnow() - started_at).total_seconds()
    return age_seconds > LOCK_TIMEOUT_SECONDS
