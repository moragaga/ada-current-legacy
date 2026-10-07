from __future__ import annotations

from ..mappers.alarm_image_published_mapper import AlarmImagePublishedMapper
from ..models.alarm_image_runtime_view_model import (
    AlarmImageRuntimeGroup,
    AlarmImageRuntimeItem,
)
from ..repositories.alarm_image_configuration_repository import AlarmImageConfigurationRepository
from ..repositories.alarm_image_public_asset_repository import AlarmImagePublicAssetRepository
from .alarm_image_runtime_bundle_sync_service import (
    AlarmImageRuntimeBundleSyncService,
    build_alarm_image_runtime_bundle_sync_service,
)
from .alarm_image_url_service import AlarmImageUrlService


class AlarmImageRuntimeQueryService:
    def __init__(
        self,
        *,
        image_repository: AlarmImageConfigurationRepository,
        published_mapper: AlarmImagePublishedMapper,
        public_asset_repository: AlarmImagePublicAssetRepository,
        runtime_sync_service: AlarmImageRuntimeBundleSyncService,
    ) -> None:
        self._image_repository = image_repository
        self._published_mapper = published_mapper
        self._public_asset_repository = public_asset_repository
        self._runtime_sync_service = runtime_sync_service

    def get_images_for_message_group(
        self,
        *,
        message_group_key: str,
        sync_if_due: bool = True,
    ) -> AlarmImageRuntimeGroup:
        normalized_group_key = str(message_group_key or '').strip()

        if not normalized_group_key:
            return AlarmImageRuntimeGroup(
                message_group_key='',
                images=[],
                has_images=False,
                has_missing_assets=False,
            )

        if sync_if_due:
            self._runtime_sync_service.sync_if_due()

        rows = self._image_repository.load_rows()

        group_rows = [
            row
            for row in rows
            if str(row.get('message_group_key') or '').strip() == normalized_group_key
        ]

        mapped_rows = self._published_mapper.to_admin_rows(group_rows)
        runtime_items = self._build_runtime_items(mapped_rows)

        if runtime_items and any(
            not item.thumb_available or not item.full_available for item in runtime_items
        ):
            self._runtime_sync_service.sync_now(force=True)

            rows = self._image_repository.load_rows()
            group_rows = [
                row
                for row in rows
                if str(row.get('message_group_key') or '').strip() == normalized_group_key
            ]
            mapped_rows = self._published_mapper.to_admin_rows(group_rows)
            runtime_items = self._build_runtime_items(mapped_rows)

        return AlarmImageRuntimeGroup(
            message_group_key=normalized_group_key,
            images=runtime_items,
            has_images=bool(runtime_items),
            has_missing_assets=any(
                not item.thumb_available or not item.full_available for item in runtime_items
            ),
        )

    def get_images_for_many_message_groups(
        self,
        *,
        message_group_keys: list[str],
        sync_if_due: bool = True,
    ) -> dict[str, AlarmImageRuntimeGroup]:
        normalized_keys = [
            str(value or '').strip() for value in message_group_keys if str(value or '').strip()
        ]

        if not normalized_keys:
            return {}

        if sync_if_due:
            self._runtime_sync_service.sync_if_due()

        rows = self._image_repository.load_rows()
        key_set = set(normalized_keys)

        rows_by_group: dict[str, list[dict]] = {key: [] for key in normalized_keys}

        for row in rows:
            row_group_key = str(row.get('message_group_key') or '').strip()

            if row_group_key in key_set:
                rows_by_group.setdefault(row_group_key, []).append(row)

        result: dict[str, AlarmImageRuntimeGroup] = {}

        for group_key, group_rows in rows_by_group.items():
            mapped_rows = self._published_mapper.to_admin_rows(group_rows)
            runtime_items = self._build_runtime_items(mapped_rows)

            result[group_key] = AlarmImageRuntimeGroup(
                message_group_key=group_key,
                images=runtime_items,
                has_images=bool(runtime_items),
                has_missing_assets=any(
                    not item.thumb_available or not item.full_available for item in runtime_items
                ),
            )

        return result

    def _build_runtime_items(
        self,
        mapped_rows: list[dict],
    ) -> list[AlarmImageRuntimeItem]:
        sorted_rows = sorted(
            mapped_rows,
            key=lambda row: (
                int(row.get('order') or 1),
                str(row.get('image_key') or ''),
            ),
        )

        result: list[AlarmImageRuntimeItem] = []

        for index, row in enumerate(sorted_rows, start=1):
            thumb_url = str(row.get('thumb_url') or '').strip()
            full_url = str(row.get('full_url') or '').strip()

            result.append(
                AlarmImageRuntimeItem(
                    message_group_key=str(row.get('message_group_key') or '').strip(),
                    image_key=str(row.get('image_key') or '').strip(),
                    order=index,
                    label=f'Imagen {index}',
                    thumb_url=thumb_url,
                    full_url=full_url,
                    thumb_mime_type=str(row.get('thumb_mime_type') or '').strip(),
                    full_mime_type=str(row.get('full_mime_type') or '').strip(),
                    thumb_available=self._asset_exists(thumb_url),
                    full_available=self._asset_exists(full_url),
                    bundle_key=str(row.get('bundle_key') or '').strip(),
                    bundle_hash=str(row.get('bundle_hash') or '').strip(),
                    content_hash=row.get('content_hash'),
                )
            )

        return result

    def _asset_exists(self, url_or_path: str) -> bool:
        if not url_or_path:
            return False

        return self._public_asset_repository.resolve_public_asset_path(url_or_path).exists()


def build_alarm_image_runtime_query_service() -> AlarmImageRuntimeQueryService:
    url_service = AlarmImageUrlService()

    return AlarmImageRuntimeQueryService(
        image_repository=AlarmImageConfigurationRepository(),
        published_mapper=AlarmImagePublishedMapper(
            url_service=url_service,
        ),
        public_asset_repository=AlarmImagePublicAssetRepository(),
        runtime_sync_service=build_alarm_image_runtime_bundle_sync_service(),
    )


def get_alarm_images_for_message_group(
    message_group_key: str,
    *,
    sync_if_due: bool = True,
) -> dict:
    return (
        build_alarm_image_runtime_query_service()
        .get_images_for_message_group(
            message_group_key=message_group_key,
            sync_if_due=sync_if_due,
        )
        .to_dict()
    )
