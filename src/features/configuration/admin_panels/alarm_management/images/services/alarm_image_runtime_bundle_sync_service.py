from __future__ import annotations

import zipfile
from dataclasses import dataclass
from datetime import UTC, datetime
from io import BytesIO
from pathlib import Path

from ..models.alarm_image_bundle_manifest import AlarmImageBundleManifestRow
from ..models.alarm_image_runtime_state import (
    FAILED_STATUS,
    READY_STATUS,
    AlarmImageRuntimeBundleState,
)
from ..repositories.alarm_image_bundle_download_repository import AlarmImageBundleDownloadRepository
from ..repositories.alarm_image_bundle_manifest_repository import AlarmImageBundleManifestRepository
from ..repositories.alarm_image_public_asset_repository import AlarmImagePublicAssetRepository
from ..repositories.alarm_image_runtime_state_repository import AlarmImageRuntimeStateRepository
from .alarm_image_runtime_check_service import AlarmImageRuntimeCheckService
from .alarm_image_runtime_lock_service import AlarmImageRuntimeLockService


@dataclass(slots=True)
class AlarmImageRuntimeSyncResult:
    executed: bool
    in_progress: bool
    synced_bundle_keys: list[str]
    skipped_bundle_keys: list[str]
    failed_bundle_keys: list[str]

    @classmethod
    def not_due(cls) -> AlarmImageRuntimeSyncResult:
        return cls(
            executed=False,
            in_progress=False,
            synced_bundle_keys=[],
            skipped_bundle_keys=[],
            failed_bundle_keys=[],
        )

    @classmethod
    def already_running(cls) -> AlarmImageRuntimeSyncResult:
        return cls(
            executed=False,
            in_progress=True,
            synced_bundle_keys=[],
            skipped_bundle_keys=[],
            failed_bundle_keys=[],
        )


class AlarmImageRuntimeBundleSyncService:
    def __init__(
        self,
        *,
        bundle_manifest_repository: AlarmImageBundleManifestRepository,
        bundle_download_repository: AlarmImageBundleDownloadRepository,
        runtime_state_repository: AlarmImageRuntimeStateRepository,
        public_asset_repository: AlarmImagePublicAssetRepository,
        lock_service: AlarmImageRuntimeLockService,
        check_service: AlarmImageRuntimeCheckService,
    ) -> None:
        self._bundle_manifest_repository = bundle_manifest_repository
        self._bundle_download_repository = bundle_download_repository
        self._runtime_state_repository = runtime_state_repository
        self._public_asset_repository = public_asset_repository
        self._lock_service = lock_service
        self._check_service = check_service

    def sync_if_due(self) -> AlarmImageRuntimeSyncResult:
        state = self._runtime_state_repository.load_state()

        if not self._check_service.should_check(state=state):
            return AlarmImageRuntimeSyncResult.not_due()

        return self.sync_now(force=False)

    def sync_now(
        self,
        *,
        force: bool = True,
    ) -> AlarmImageRuntimeSyncResult:
        state = self._runtime_state_repository.load_state()

        if not self._check_service.should_check(state=state, force=force):
            return AlarmImageRuntimeSyncResult.not_due()

        with self._lock_service.acquire() as lock:
            if lock is None:
                return AlarmImageRuntimeSyncResult.already_running()

            state = self._runtime_state_repository.load_state()

            synced_bundle_keys: list[str] = []
            skipped_bundle_keys: list[str] = []
            failed_bundle_keys: list[str] = []

            try:
                manifest_rows = self._bundle_manifest_repository.load_rows()
                manifest_bundle_keys = {row.bundle_key for row in manifest_rows}

                for manifest_row in manifest_rows:
                    if self._is_bundle_ready(manifest_row):
                        skipped_bundle_keys.append(manifest_row.bundle_key)
                        state.bundles[manifest_row.bundle_key] = AlarmImageRuntimeBundleState(
                            bundle_key=manifest_row.bundle_key,
                            bundle_hash=manifest_row.bundle_hash,
                            status=READY_STATUS,
                            synced_at=datetime.now(UTC).isoformat(),
                            bundle_relative_path=manifest_row.bundle_relative_path,
                        )
                        self._runtime_state_repository.save_state(state)
                        continue

                    try:
                        self._sync_bundle(manifest_row)
                    except Exception as exc:
                        failed_bundle_keys.append(manifest_row.bundle_key)
                        state.bundles[manifest_row.bundle_key] = AlarmImageRuntimeBundleState(
                            bundle_key=manifest_row.bundle_key,
                            bundle_hash=manifest_row.bundle_hash,
                            status=FAILED_STATUS,
                            synced_at=None,
                            last_error=str(exc),
                            bundle_relative_path=manifest_row.bundle_relative_path,
                        )
                        self._runtime_state_repository.save_state(state)
                        continue

                    synced_bundle_keys.append(manifest_row.bundle_key)
                    state.bundles[manifest_row.bundle_key] = AlarmImageRuntimeBundleState(
                        bundle_key=manifest_row.bundle_key,
                        bundle_hash=manifest_row.bundle_hash,
                        status=READY_STATUS,
                        synced_at=datetime.now(UTC).isoformat(),
                        bundle_relative_path=manifest_row.bundle_relative_path,
                    )
                    self._runtime_state_repository.save_state(state)

                state.bundles = {
                    bundle_key: bundle_state
                    for bundle_key, bundle_state in state.bundles.items()
                    if bundle_key in manifest_bundle_keys
                }

                if failed_bundle_keys:
                    state = self._check_service.schedule_failure(state)
                else:
                    state = self._check_service.schedule_success(state)

                self._runtime_state_repository.save_state(state)

                return AlarmImageRuntimeSyncResult(
                    executed=True,
                    in_progress=False,
                    synced_bundle_keys=synced_bundle_keys,
                    skipped_bundle_keys=skipped_bundle_keys,
                    failed_bundle_keys=failed_bundle_keys,
                )

            except Exception:
                state = self._check_service.schedule_failure(state)
                self._runtime_state_repository.save_state(state)
                raise

    def _is_bundle_ready(
        self,
        manifest_row: AlarmImageBundleManifestRow,
    ) -> bool:
        state = self._runtime_state_repository.load_state()
        bundle_state = state.bundles.get(manifest_row.bundle_key)

        if bundle_state is None:
            return False

        if bundle_state.status != READY_STATUS:
            return False

        if bundle_state.bundle_hash != manifest_row.bundle_hash:
            return False

        return self._public_asset_repository.has_public_bundle(
            bundle_key=manifest_row.bundle_key,
            bundle_hash=manifest_row.bundle_hash,
        )

    def _sync_bundle(
        self,
        manifest_row: AlarmImageBundleManifestRow,
    ) -> None:
        zip_content = self._bundle_download_repository.download_bundle(
            bundle_relative_path=manifest_row.bundle_relative_path,
        )

        staging_dir = self._public_asset_repository.prepare_staging_dir(
            bundle_key=manifest_row.bundle_key,
            trace_id=f'runtime_{manifest_row.bundle_hash}',
        )

        try:
            self._extract_zip_safely(
                zip_content=zip_content,
                target_dir=staging_dir,
            )

            extracted_hash = self._public_asset_repository.compute_directory_hash(staging_dir)

            if extracted_hash != manifest_row.bundle_hash:
                raise RuntimeError(
                    'Hash inválido para bundle '
                    f'{manifest_row.bundle_key}. '
                    f'Esperado={manifest_row.bundle_hash}, obtenido={extracted_hash}.'
                )

            self._public_asset_repository.commit_bundle(
                bundle_key=manifest_row.bundle_key,
                bundle_hash=manifest_row.bundle_hash,
                staging_dir=staging_dir,
            )

        finally:
            self._public_asset_repository.cleanup_staging_dir(staging_dir)

    @staticmethod
    def _extract_zip_safely(
        *,
        zip_content: bytes,
        target_dir: Path,
    ) -> None:
        target_root = target_dir.resolve()

        with zipfile.ZipFile(BytesIO(zip_content), mode='r') as zip_file:
            for member in zip_file.infolist():
                if member.is_dir():
                    continue

                member_path = Path(member.filename)

                if member_path.is_absolute() or '..' in member_path.parts:
                    raise RuntimeError(f'Ruta inválida dentro del ZIP: {member.filename}')

                target_path = (target_dir / member_path).resolve()

                if not str(target_path).startswith(str(target_root)):
                    raise RuntimeError(f'Ruta fuera del destino en ZIP: {member.filename}')

                target_path.parent.mkdir(parents=True, exist_ok=True)

                with zip_file.open(member, mode='r') as source:
                    target_path.write_bytes(source.read())


def build_alarm_image_runtime_bundle_sync_service() -> AlarmImageRuntimeBundleSyncService:
    runtime_state_repository = AlarmImageRuntimeStateRepository()

    return AlarmImageRuntimeBundleSyncService(
        bundle_manifest_repository=AlarmImageBundleManifestRepository(),
        bundle_download_repository=AlarmImageBundleDownloadRepository(),
        runtime_state_repository=runtime_state_repository,
        public_asset_repository=AlarmImagePublicAssetRepository(),
        lock_service=AlarmImageRuntimeLockService(
            lock_path=runtime_state_repository.runtime_root / 'sync.lock',
            ttl_seconds=600,
        ),
        check_service=AlarmImageRuntimeCheckService(
            success_interval_seconds=180,
            failure_interval_seconds=60,
            jitter_seconds=60,
        ),
    )


def sync_alarm_image_bundles_now() -> AlarmImageRuntimeSyncResult:
    return build_alarm_image_runtime_bundle_sync_service().sync_now(force=True)


def sync_alarm_image_bundles_if_due() -> AlarmImageRuntimeSyncResult:
    return build_alarm_image_runtime_bundle_sync_service().sync_if_due()
