from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

_LOCK_TTL_SECONDS = 90
_EXPIRED_AFTER_SECONDS = 300


def build_dashboard_refresh_signal() -> dict[str, Any]:
    return {
        'token': str(uuid4()),
        'created_at_utc': _utc_now_iso(),
    }


def build_acquired_dashboard_refresh_lock(*, signal: dict[str, Any]) -> dict[str, Any]:
    return {
        'is_running': True,
        'active_token': signal.get('token'),
        'started_at_utc': _utc_now_iso(),
    }


def build_released_dashboard_refresh_lock() -> dict[str, Any]:
    return {
        'is_running': False,
        'active_token': None,
        'started_at_utc': None,
        'released_at_utc': _utc_now_iso(),
    }


def is_dashboard_refresh_lock_expired(*, lock_data: dict[str, Any] | None) -> bool:
    if not lock_data:
        return False

    started_at_utc = _parse_datetime(lock_data.get('started_at_utc'))
    if started_at_utc is None:
        return True

    elapsed = (datetime.now(tz=UTC) - started_at_utc).total_seconds()
    return elapsed > _LOCK_TTL_SECONDS


def evaluate_dashboard_runtime_result(
    *,
    current_last_update: Any,
    previous_last_update_pi_utc: Any,
    previous_last_update_dispatch_utc: Any
) -> tuple[dict[str, Any], dict[str, Any], bool]:
    last_update_pi_inst = current_last_update.get('ultima_actualizacion_pi_inst')
    last_update_dispatch_inst = current_last_update.get('ultima_actualizacion_dispatch_inst')
    last_update_pi_iso = _to_iso(last_update_pi_inst)
    last_update_dispatch_iso = _to_iso(last_update_dispatch_inst)
    previous_iso_pi = _to_iso(previous_last_update_pi_utc)
    previous_iso_dispatch = _to_iso(previous_last_update_dispatch_utc)
    refreshed_at_utc = _utc_now_iso()

    changed = last_update_pi_iso is None or last_update_pi_iso != previous_iso_pi
    expired = _is_expired(last_update_pi_iso)

    runtime_store = {
        'changed': changed,
        'expired': expired,
        'last_update_pi_utc': last_update_pi_iso,
        'refreshed_at_utc': refreshed_at_utc,
    }

    information_status_store = {
        'changed': changed,
        'expired': expired,
        'last_update_pi_utc': last_update_pi_iso,
        'last_update_dispatch_utc': last_update_dispatch_iso,
        'previous_last_update_pi_utc': previous_iso_pi,
        'previous_last_update_dispatch_utc': previous_iso_dispatch,
        'refreshed_at_utc': refreshed_at_utc,
    }

    return runtime_store, information_status_store, changed


def _is_expired(value: str | None) -> bool:
    parsed = _parse_datetime(value)
    if parsed is None:
        return True

    elapsed = (datetime.now(tz=UTC) - parsed).total_seconds()
    return elapsed > _EXPIRED_AFTER_SECONDS


def _to_iso(value: Any) -> str | None:
    if value is None:
        return None

    if isinstance(value, datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=UTC)
        return value.astimezone(UTC).isoformat()

    if isinstance(value, str):
        parsed = _parse_datetime(value)
        if parsed is None:
            return value
        return parsed.astimezone(UTC).isoformat()

    return str(value)


def _parse_datetime(value: Any) -> datetime | None:
    if isinstance(value, datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)

    if not isinstance(value, str) or not value:
        return None

    try:
        normalized = value.replace('Z', '+00:00')
        parsed = datetime.fromisoformat(normalized)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=UTC)
        return parsed.astimezone(UTC)
    except ValueError:
        return None


def _utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat()
