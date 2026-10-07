from __future__ import annotations

from dataclasses import dataclass

from ..models.alarm_image_runtime_state import FAILED_STATUS
from ..repositories.alarm_image_bundle_manifest_repository import AlarmImageBundleManifestRepository
from ..repositories.alarm_image_public_asset_repository import AlarmImagePublicAssetRepository
from ..repositories.alarm_image_runtime_state_repository import AlarmImageRuntimeStateRepository


@dataclass(slots=True)
class AlarmImageAdminStatus:
    bundle_count: int
    ready_count: int
    failed_count: int
    pending_count: int
    total_size_bytes: int
    last_published_at: str | None
    last_published_by: str | None
    last_published_by_email: str | None
    last_runtime_check_at: str | None
    next_runtime_check_at: str | None
    last_runtime_success_at: str | None
    last_runtime_failure_at: str | None
    last_runtime_error: str | None


class AlarmImageAdminStatusService:
    def __init__(
        self,
        *,
        manifest_repository: AlarmImageBundleManifestRepository,
        runtime_state_repository: AlarmImageRuntimeStateRepository,
        public_asset_repository: AlarmImagePublicAssetRepository,
    ) -> None:
        self._manifest_repository = manifest_repository
        self._runtime_state_repository = runtime_state_repository
        self._public_asset_repository = public_asset_repository

    def get_status(self) -> AlarmImageAdminStatus:
        manifest_rows = self._manifest_repository.load_rows()
        runtime_state = self._runtime_state_repository.load_state()

        ready_count = 0
        failed_count = 0
        pending_count = 0

        for manifest_row in manifest_rows:
            bundle_state = runtime_state.bundles.get(manifest_row.bundle_key)

            is_local_ready = self._public_asset_repository.has_public_bundle(
                bundle_key=manifest_row.bundle_key,
                bundle_hash=manifest_row.bundle_hash,
            )

            if is_local_ready:
                ready_count += 1
                continue

            if (
                bundle_state is not None
                and bundle_state.status == FAILED_STATUS
                and bundle_state.bundle_hash == manifest_row.bundle_hash
            ):
                failed_count += 1
                continue

            pending_count += 1

        last_publication = self._get_last_publication(manifest_rows)

        return AlarmImageAdminStatus(
            bundle_count=len(manifest_rows),
            ready_count=ready_count,
            failed_count=failed_count,
            pending_count=pending_count,
            total_size_bytes=sum(row.size_bytes for row in manifest_rows),
            last_published_at=last_publication.published_at if last_publication else None,
            last_published_by=last_publication.published_by if last_publication else None,
            last_published_by_email=last_publication.published_by_email
            if last_publication
            else None,
            last_runtime_check_at=runtime_state.last_check_at,
            next_runtime_check_at=runtime_state.next_check_at,
            last_runtime_success_at=runtime_state.last_success_at,
            last_runtime_failure_at=runtime_state.last_failure_at,
            last_runtime_error=runtime_state.last_error,
        )

    @staticmethod
    def _get_last_publication(rows):
        if not rows:
            return None

        return max(
            rows,
            key=lambda row: row.published_at or row.updated_at or '',
        )


def build_alarm_image_admin_status_service() -> AlarmImageAdminStatusService:
    return AlarmImageAdminStatusService(
        manifest_repository=AlarmImageBundleManifestRepository(),
        runtime_state_repository=AlarmImageRuntimeStateRepository(),
        public_asset_repository=AlarmImagePublicAssetRepository(),
    )
