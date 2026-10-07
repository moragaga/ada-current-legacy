from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ..models.alarm_image_admin_view_model import (
    DELETED_STATUS,
    NEW_STATUS,
    REPLACED_STATUS,
    AlarmImageAdminDraft,
)
from ..repositories.alarm_image_public_asset_repository import AlarmImagePublicAssetRepository
from .alarm_image_bundle_builder_service import (
    AlarmImageBundleBuilderService,
    AlarmImageBundleBuildResult,
)
from .alarm_image_bundle_shard_planner import AlarmImageBundleShardPlanner


@dataclass(slots=True)
class AlarmImageContentPublicationResult:
    rows: list[dict]
    rebuilt_bundles: list[AlarmImageBundleBuildResult]


class AlarmImageContentPublicationService:
    def __init__(
        self,
        *,
        shard_planner: AlarmImageBundleShardPlanner,
        bundle_builder: AlarmImageBundleBuilderService,
        asset_repository: AlarmImagePublicAssetRepository,
    ) -> None:
        self._shard_planner = shard_planner
        self._bundle_builder = bundle_builder
        self._asset_repository = asset_repository

    def build_publication(
        self,
        *,
        current_rows: list[dict],
        draft: AlarmImageAdminDraft,
    ) -> AlarmImageContentPublicationResult:
        group_bundle_map = self._shard_planner.build_group_bundle_map(
            current_rows=current_rows,
            draft=draft,
        )
        affected_bundle_keys = self._shard_planner.get_affected_bundle_keys(
            current_rows=current_rows,
            draft=draft,
            group_bundle_map=group_bundle_map,
        )

        current_rows_by_key = {
            self._build_row_key(row): dict(row) for row in current_rows if self._build_row_key(row)
        }

        candidate_rows = self._build_candidate_rows(
            draft=draft,
            current_rows_by_key=current_rows_by_key,
            group_bundle_map=group_bundle_map,
        )

        if not affected_bundle_keys:
            return AlarmImageContentPublicationResult(
                rows=[self._drop_internal_fields(row) for row in candidate_rows],
                rebuilt_bundles=[],
            )

        final_rows: list[dict] = []
        rebuilt_bundles: list[AlarmImageBundleBuildResult] = []
        rows_by_bundle = self._group_rows_by_bundle(candidate_rows)

        for bundle_key, rows in rows_by_bundle.items():
            if bundle_key in affected_bundle_keys:
                build_result = self._bundle_builder.rebuild_bundle(
                    bundle_key=bundle_key,
                    rows=rows,
                )
                rebuilt_bundles.append(build_result)
                final_rows.extend(build_result.rows)
            else:
                final_rows.extend(self._drop_internal_fields(row) for row in rows)

        final_rows.sort(
            key=lambda row: (
                str(row.get('message_group_key') or '').lower(),
                int(row.get('order') or 1),
                str(row.get('image_key') or ''),
            )
        )

        return AlarmImageContentPublicationResult(
            rows=final_rows,
            rebuilt_bundles=rebuilt_bundles,
        )

    def _build_candidate_rows(
        self,
        *,
        draft: AlarmImageAdminDraft,
        current_rows_by_key: dict[str, dict],
        group_bundle_map: dict[str, str],
    ) -> list[dict]:
        candidate_rows: list[dict] = []

        for group in draft.groups:
            for image in group.images:
                if image.status == DELETED_STATUS:
                    continue

                row_key = self._build_key(
                    message_group_key=image.message_group_key,
                    image_key=image.image_key,
                )
                current_row = current_rows_by_key.get(row_key, {})
                bundle_key = (
                    group_bundle_map.get(image.message_group_key)
                    or current_row.get('bundle_key')
                    or 'bundle_001'
                )

                if image.status in {NEW_STATUS, REPLACED_STATUS}:
                    source_full_path = Path(str(image.draft_file_path or ''))
                else:
                    source_full_path = self._resolve_current_source_path(current_row)

                candidate_rows.append(
                    {
                        'message_group_key': image.message_group_key,
                        'image_key': image.image_key,
                        'order': image.order,
                        'bundle_key': bundle_key,
                        'bundle_hash': str(current_row.get('bundle_hash') or ''),
                        'thumb_path': str(current_row.get('thumb_path') or ''),
                        'full_path': str(current_row.get('full_path') or ''),
                        'thumb_mime_type': str(
                            current_row.get('thumb_mime_type')
                            or image.thumb_mime_type
                            or 'image/webp'
                        ),
                        'full_mime_type': str(
                            current_row.get('full_mime_type') or image.full_mime_type or ''
                        ),
                        'content_hash': str(
                            current_row.get('content_hash') or image.content_hash or ''
                        ),
                        '_source_full_path': str(source_full_path),
                    }
                )

        return candidate_rows

    def _resolve_current_source_path(self, current_row: dict) -> Path:
        full_path = str(current_row.get('full_path') or '').strip()
        thumb_path = str(current_row.get('thumb_path') or '').strip()

        if full_path:
            resolved_full_path = self._asset_repository.resolve_public_asset_path(full_path)
            if resolved_full_path.exists():
                return resolved_full_path

        if thumb_path:
            resolved_thumb_path = self._asset_repository.resolve_public_asset_path(thumb_path)
            if resolved_thumb_path.exists():
                return resolved_thumb_path

        raise FileNotFoundError('No se encontró archivo local publicado para una imagen existente.')

    @staticmethod
    def _group_rows_by_bundle(rows: list[dict]) -> dict[str, list[dict]]:
        result: dict[str, list[dict]] = {}

        for row in rows:
            bundle_key = str(row.get('bundle_key') or 'bundle_001')
            result.setdefault(bundle_key, []).append(row)

        return result

    def _build_row_key(self, row: dict) -> str:
        message_group_key = str(row.get('message_group_key') or '').strip()
        image_key = str(row.get('image_key') or '').strip()

        if not message_group_key or not image_key:
            return ''

        return self._build_key(
            message_group_key=message_group_key,
            image_key=image_key,
        )

    @staticmethod
    def _build_key(
        *,
        message_group_key: str,
        image_key: str,
    ) -> str:
        return f'{message_group_key}::{image_key}'

    @staticmethod
    def _drop_internal_fields(row: dict) -> dict:
        return {key: value for key, value in row.items() if not key.startswith('_')}
