from __future__ import annotations

from ..mappers.alarm_image_published_mapper import AlarmImagePublishedMapper
from ..models.alarm_image_admin_view_model import AlarmImageAdminDraft
from ..models.alarm_image_publication import (
    CONTENT_MODE,
    ORDER_ONLY_MODE,
    AlarmImagePublicationResult,
)
from ..repositories.admin_rows_data_accessor import AdminRowsDataAccessor
from ..repositories.alarm_configuration_rows_repository import AlarmConfigurationRowsRepository
from ..repositories.alarm_image_bundle_manifest_repository import AlarmImageBundleManifestRepository
from ..repositories.alarm_image_bundle_sharepoint_repository import (
    AlarmImageBundleSharePointRepository,
)
from ..repositories.alarm_image_configuration_repository import AlarmImageConfigurationRepository
from ..repositories.alarm_image_public_asset_repository import AlarmImagePublicAssetRepository
from .alarm_image_asset_processing_service import AlarmImageAssetProcessingService
from .alarm_image_bundle_builder_service import AlarmImageBundleBuilderService
from .alarm_image_bundle_manifest_service import AlarmImageBundleManifestService
from .alarm_image_bundle_shard_planner import AlarmImageBundleShardPlanner
from .alarm_image_content_publication_service import AlarmImageContentPublicationService
from .alarm_image_group_source_service import AlarmImageGroupSourceService
from .alarm_image_publication_actor_service import AlarmImagePublicationActorService
from .alarm_image_url_service import AlarmImageUrlService


class AlarmImageAdminApplicationService:
    def __init__(
        self,
        *,
        group_source_service: AlarmImageGroupSourceService,
        image_repository: AlarmImageConfigurationRepository,
        bundle_manifest_repository: AlarmImageBundleManifestRepository,
        bundle_sharepoint_repository: AlarmImageBundleSharePointRepository,
        published_mapper: AlarmImagePublishedMapper,
        content_publication_service: AlarmImageContentPublicationService,
        bundle_manifest_service: AlarmImageBundleManifestService,
        actor_service: AlarmImagePublicationActorService,
    ) -> None:
        self._group_source_service = group_source_service
        self._image_repository = image_repository
        self._bundle_manifest_repository = bundle_manifest_repository
        self._bundle_sharepoint_repository = bundle_sharepoint_repository
        self._published_mapper = published_mapper
        self._content_publication_service = content_publication_service
        self._bundle_manifest_service = bundle_manifest_service
        self._actor_service = actor_service

    def load_message_groups(self) -> list[dict]:
        return self._group_source_service.load_message_groups()

    def load_published_images(self) -> list[dict]:
        rows = self._image_repository.load_rows()
        return self._published_mapper.to_admin_rows(rows)

    def publish_order_changes(
        self,
        draft: AlarmImageAdminDraft,
    ) -> AlarmImagePublicationResult:
        current_rows = self._image_repository.load_rows()
        updated_rows = self._apply_order_changes(
            current_rows=current_rows,
            draft=draft,
        )

        self._image_repository.save_rows(updated_rows)

        return AlarmImagePublicationResult.ok(
            mode=ORDER_ONLY_MODE,
            message='Cambios de orden guardados correctamente.',
        )

    def publish_content_changes(
        self,
        draft: AlarmImageAdminDraft,
    ) -> AlarmImagePublicationResult:
        current_rows = self._image_repository.load_rows()

        publication = self._content_publication_service.build_publication(
            current_rows=current_rows,
            draft=draft,
        )

        uploaded_relative_paths = {}

        for rebuilt_bundle in publication.rebuilt_bundles:
            uploaded_relative_paths[rebuilt_bundle.bundle_key] = (
                self._bundle_sharepoint_repository.upload_bundle_zip(
                    zip_path=rebuilt_bundle.zip_file.path,
                    bundle_filename=rebuilt_bundle.zip_file.filename,
                )
            )

        actor = self._actor_service.get_current_actor()
        current_manifest_rows = self._bundle_manifest_repository.load_rows()

        updated_manifest_rows = self._bundle_manifest_service.merge_rebuilt_bundles(
            current_manifest_rows=current_manifest_rows,
            image_rows=publication.rows,
            rebuilt_bundles=publication.rebuilt_bundles,
            uploaded_relative_paths=uploaded_relative_paths,
            actor=actor,
        )

        self._image_repository.save_rows(publication.rows)
        self._bundle_manifest_repository.save_rows(updated_manifest_rows)

        return AlarmImagePublicationResult.ok(
            mode=CONTENT_MODE,
            message='Cambios de imágenes publicados correctamente.',
        )

    def _apply_order_changes(
        self,
        *,
        current_rows: list[dict],
        draft: AlarmImageAdminDraft,
    ) -> list[dict]:
        rows_by_key = {
            self._build_row_key(row): dict(row) for row in current_rows if self._build_row_key(row)
        }

        for group in draft.groups:
            for image in group.active_images:
                row_key = self._build_key(
                    message_group_key=image.message_group_key,
                    image_key=image.image_key,
                )

                if row_key not in rows_by_key:
                    continue

                rows_by_key[row_key]['order'] = image.order

        return list(rows_by_key.values())

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


def build_alarm_image_admin_application_service() -> AlarmImageAdminApplicationService:
    data_accessor = AdminRowsDataAccessor()

    alarm_configuration_rows_repository = AlarmConfigurationRowsRepository(
        data_accessor=data_accessor,
    )

    group_source_service = AlarmImageGroupSourceService(
        load_alarm_configuration_rows=alarm_configuration_rows_repository.load_rows,
    )

    image_repository = AlarmImageConfigurationRepository(
        data_accessor=data_accessor,
    )

    bundle_manifest_repository = AlarmImageBundleManifestRepository(
        data_accessor=data_accessor,
    )

    bundle_sharepoint_repository = AlarmImageBundleSharePointRepository()

    url_service = AlarmImageUrlService()

    published_mapper = AlarmImagePublishedMapper(
        url_service=url_service,
    )

    asset_repository = AlarmImagePublicAssetRepository()

    processing_service = AlarmImageAssetProcessingService()

    bundle_builder = AlarmImageBundleBuilderService(
        asset_repository=asset_repository,
        processing_service=processing_service,
    )

    shard_planner = AlarmImageBundleShardPlanner(
        max_groups_per_bundle=15,
    )

    content_publication_service = AlarmImageContentPublicationService(
        shard_planner=shard_planner,
        bundle_builder=bundle_builder,
        asset_repository=asset_repository,
    )

    bundle_manifest_service = AlarmImageBundleManifestService()

    return AlarmImageAdminApplicationService(
        group_source_service=group_source_service,
        image_repository=image_repository,
        bundle_manifest_repository=bundle_manifest_repository,
        bundle_sharepoint_repository=bundle_sharepoint_repository,
        published_mapper=published_mapper,
        content_publication_service=content_publication_service,
        bundle_manifest_service=bundle_manifest_service,
        actor_service=AlarmImagePublicationActorService(),
    )
