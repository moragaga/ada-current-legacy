from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

READY_STATUS = 'ready'
FAILED_STATUS = 'failed'


@dataclass(slots=True)
class AlarmImageRuntimeBundleState:
    bundle_key: str
    bundle_hash: str
    status: str
    synced_at: str | None = None
    last_error: str | None = None
    bundle_relative_path: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AlarmImageRuntimeBundleState:
        return cls(
            bundle_key=str(data.get('bundle_key') or '').strip(),
            bundle_hash=str(data.get('bundle_hash') or '').strip(),
            status=str(data.get('status') or '').strip(),
            synced_at=data.get('synced_at'),
            last_error=data.get('last_error'),
            bundle_relative_path=data.get('bundle_relative_path'),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'bundle_key': self.bundle_key,
            'bundle_hash': self.bundle_hash,
            'status': self.status,
            'synced_at': self.synced_at,
            'last_error': self.last_error,
            'bundle_relative_path': self.bundle_relative_path,
        }


@dataclass(slots=True)
class AlarmImageRuntimeState:
    bundles: dict[str, AlarmImageRuntimeBundleState] = field(default_factory=dict)
    last_check_at: str | None = None
    next_check_at: str | None = None
    last_success_at: str | None = None
    last_failure_at: str | None = None
    last_error: str | None = None

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AlarmImageRuntimeState:
        bundles_data = data.get('bundles') or {}

        return cls(
            bundles={
                str(bundle_key): AlarmImageRuntimeBundleState.from_dict(bundle_data)
                for bundle_key, bundle_data in bundles_data.items()
                if isinstance(bundle_data, dict)
            },
            last_check_at=data.get('last_check_at'),
            next_check_at=data.get('next_check_at'),
            last_success_at=data.get('last_success_at'),
            last_failure_at=data.get('last_failure_at'),
            last_error=data.get('last_error'),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            'bundles': {
                bundle_key: bundle_state.to_dict()
                for bundle_key, bundle_state in self.bundles.items()
            },
            'last_check_at': self.last_check_at,
            'next_check_at': self.next_check_at,
            'last_success_at': self.last_success_at,
            'last_failure_at': self.last_failure_at,
            'last_error': self.last_error,
        }
