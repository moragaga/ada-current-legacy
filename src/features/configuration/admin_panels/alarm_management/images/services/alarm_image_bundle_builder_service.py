from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4

from ..repositories.alarm_image_public_asset_repository import (
    AlarmImageBundleZip,
    AlarmImagePublicAssetRepository,
)
from .alarm_image_asset_processing_service import AlarmImageAssetProcessingService


@dataclass(slots=True)
class AlarmImageBundleBuildResult:
    bundle_key: str
    bundle_hash: str
    zip_file: AlarmImageBundleZip
    rows: list[dict]


class AlarmImageBundleBuilderService:
    def __init__(
        self,
        *,
        asset_repository: AlarmImagePublicAssetRepository,
        processing_service: AlarmImageAssetProcessingService,
    ) -> None:
        self._asset_repository = asset_repository
        self._processing_service = processing_service

    def rebuild_bundle(
        self,
        *,
        bundle_key: str,
        rows: list[dict],
    ) -> AlarmImageBundleBuildResult:
        trace_id = uuid4().hex
        staging_dir = self._asset_repository.prepare_staging_dir(
            bundle_key=bundle_key,
            trace_id=trace_id,
        )

        try:
            processed_rows = []

            for row in rows:
                source_path = Path(str(row.get('_source_full_path') or ''))

                processed_asset = self._processing_service.process_to_staging(
                    source_path=source_path,
                    staging_bundle_dir=staging_dir,
                    message_group_key=str(row['message_group_key']),
                    image_key=str(row['image_key']),
                )

                processed_rows.append(
                    {
                        **self._drop_internal_fields(row),
                        '_processed_thumb_relative_path': processed_asset.thumb_relative_path,
                        '_processed_full_relative_path': processed_asset.full_relative_path,
                        'thumb_mime_type': processed_asset.thumb_mime_type,
                        'full_mime_type': processed_asset.full_mime_type,
                        'content_hash': processed_asset.content_hash,
                    }
                )

            bundle_hash = self._asset_repository.compute_directory_hash(staging_dir)
            final_dir = self._asset_repository.commit_bundle(
                bundle_key=bundle_key,
                bundle_hash=bundle_hash,
                staging_dir=staging_dir,
            )
            zip_file = self._asset_repository.create_bundle_zip(
                bundle_key=bundle_key,
                bundle_hash=bundle_hash,
                bundle_dir=final_dir,
            )

            final_rows = [
                self._build_final_row(
                    row=row,
                    bundle_key=bundle_key,
                    bundle_hash=bundle_hash,
                )
                for row in processed_rows
            ]

            return AlarmImageBundleBuildResult(
                bundle_key=bundle_key,
                bundle_hash=bundle_hash,
                zip_file=zip_file,
                rows=final_rows,
            )

        finally:
            self._asset_repository.cleanup_staging_dir(staging_dir)

    def _build_final_row(
        self,
        *,
        row: dict,
        bundle_key: str,
        bundle_hash: str,
    ) -> dict:
        thumb_relative_path = str(row.pop('_processed_thumb_relative_path'))
        full_relative_path = str(row.pop('_processed_full_relative_path'))

        return {
            **row,
            'bundle_key': bundle_key,
            'bundle_hash': bundle_hash,
            'thumb_path': self._asset_repository.build_public_path(
                bundle_key=bundle_key,
                bundle_hash=bundle_hash,
                relative_path=thumb_relative_path,
            ),
            'full_path': self._asset_repository.build_public_path(
                bundle_key=bundle_key,
                bundle_hash=bundle_hash,
                relative_path=full_relative_path,
            ),
        }

    @staticmethod
    def _drop_internal_fields(row: dict) -> dict:
        return {key: value for key, value in row.items() if not key.startswith('_')}
