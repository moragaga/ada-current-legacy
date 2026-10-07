from __future__ import annotations

from copy import deepcopy
from typing import Any

from src.features.admin_framework.services import AdminDataService
from src.features.configuration.admin_panels.alarm_configuration.definition import (
    ALARM_CONFIGURATION_ADMIN_DEFINITION,
)
from src.features.configuration.repositories import ConfigurationSharepointRepository
from src.features.configuration.services import ConfigManifestService

from ..constants import (
    GLOBAL_MESSAGES_BUCKET,
    MESSAGE_CONFIGURATION_SCHEMA_VERSION,
    MESSAGE_GROUP_BUCKET_PREFIX,
)
from ..definition import ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION
from .alarm_message_bucket_service import AlarmMessageBucketService
from .alarm_message_configuration_normalizer import AlarmMessageConfigurationNormalizer
from .alarm_message_row_validator import AlarmMessageRowValidator


class AlarmMessageAdminService:
    def __init__(
        self,
        *,
        admin_data_service: AdminDataService,
        configuration_repository: ConfigurationSharepointRepository,
        manifest_service: ConfigManifestService,
    ) -> None:
        self._admin_data_service = admin_data_service
        self._configuration_repository = configuration_repository
        self._manifest_service = manifest_service

    def build_snapshot(self) -> dict[str, Any]:
        alarm_rows = self._load_alarm_rows()

        message_configuration = self._load_or_build_empty_configuration(
            alarm_rows=alarm_rows,
        )

        bucket_options = AlarmMessageBucketService.build_bucket_options(
            alarm_rows=alarm_rows,
            message_configuration=message_configuration,
        )

        return {
            'alarm_rows_count': len(alarm_rows),
            'message_configuration': message_configuration,
            'bucket_options': bucket_options,
        }

    def save_bucket(
        self,
        *,
        selected_bucket: str,
        rows: list[dict[str, Any]],
        updated_by: str | None,
    ) -> tuple[bool, list[str], dict[str, Any]]:
        try:
            alarm_rows = self._load_alarm_rows()

            current_configuration = self._load_or_build_empty_configuration(
                alarm_rows=alarm_rows,
            )

            updated_configuration = self._replace_bucket_rows(
                message_configuration=current_configuration,
                selected_bucket=selected_bucket,
                rows=rows,
            )

            saved = self._save_message_configuration(
                message_configuration=updated_configuration,
            )

            if not saved:
                return (
                    False,
                    ['No se pudo guardar la configuración de mensajes.'],
                    current_configuration,
                )

            manifest_ok = self._manifest_service.register_update(
                definition=ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION,
                rows=updated_configuration,
                updated_by=updated_by,
            )

            if not manifest_ok:
                return (
                    False,
                    [
                        'Los mensajes fueron guardados, pero no se pudo actualizar el config manifest.'
                    ],
                    updated_configuration,
                )

            return True, [], updated_configuration

        except Exception as error:
            fallback_configuration = self._load_or_build_empty_configuration(
                alarm_rows=self._load_alarm_rows(),
            )

            return False, [str(error)], fallback_configuration

    def _load_alarm_rows(self) -> list[dict[str, Any]]:
        rows = self._admin_data_service.load(
            ALARM_CONFIGURATION_ADMIN_DEFINITION,
        )

        return [row for row in rows or [] if isinstance(row, dict)]

    def _load_or_build_empty_configuration(
        self,
        *,
        alarm_rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        raw_config = self._configuration_repository.load_document(
            filename=ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION.remote.sharepoint_filename,
            relative_path=ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION.remote.relative_path,
            default=None,
        )

        if raw_config is None:
            return self._build_empty_configuration(
                alarm_rows=alarm_rows,
            )

        if not isinstance(raw_config, dict):
            raise ValueError(
                'alarm_management_message_configuration.json.gz debe ser un objeto JSON.'
            )

        normalized = AlarmMessageConfigurationNormalizer.normalize(
            configuration=raw_config,
        )

        return self._ensure_alarm_groups_exist(
            message_configuration=normalized,
            alarm_rows=alarm_rows,
        )

    @staticmethod
    def _build_empty_configuration(
        *,
        alarm_rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        message_groups = AlarmMessageBucketService.resolve_message_groups_from_alarm_rows(
            alarm_rows=alarm_rows,
        )

        return {
            'schema_version': MESSAGE_CONFIGURATION_SCHEMA_VERSION,
            'global_messages': [],
            'messages_by_group_key': {
                message_group: [] for message_group in sorted(message_groups)
            },
        }

    def _save_message_configuration(
        self,
        *,
        message_configuration: dict[str, Any],
    ) -> bool:
        normalized = AlarmMessageConfigurationNormalizer.normalize(
            configuration=message_configuration,
        )

        return self._configuration_repository.save_document(
            filename=ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION.remote.sharepoint_filename,
            relative_path=ALARM_MANAGEMENT_MESSAGES_ADMIN_DEFINITION.remote.relative_path,
            document=normalized,
        )

    @staticmethod
    def _ensure_alarm_groups_exist(
        *,
        message_configuration: dict[str, Any],
        alarm_rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        config = AlarmMessageConfigurationNormalizer.normalize(
            configuration=deepcopy(message_configuration),
        )

        message_groups = AlarmMessageBucketService.resolve_message_groups_from_alarm_rows(
            alarm_rows=alarm_rows,
        )

        config.setdefault('messages_by_group_key', {})

        for message_group in sorted(message_groups):
            config['messages_by_group_key'].setdefault(message_group, [])

        return AlarmMessageConfigurationNormalizer.normalize(
            configuration=config,
        )

    @staticmethod
    def _replace_bucket_rows(
        *,
        message_configuration: dict[str, Any],
        selected_bucket: str,
        rows: list[dict[str, Any]],
    ) -> dict[str, Any]:
        normalized_rows = AlarmMessageRowValidator.normalize_and_validate_rows(
            rows=rows,
        )

        config = AlarmMessageConfigurationNormalizer.normalize(
            configuration=message_configuration,
        )

        if selected_bucket == GLOBAL_MESSAGES_BUCKET:
            config['global_messages'] = normalized_rows
            return config

        if selected_bucket.startswith(MESSAGE_GROUP_BUCKET_PREFIX):
            message_group = selected_bucket.removeprefix(MESSAGE_GROUP_BUCKET_PREFIX).strip()

            if not message_group:
                raise ValueError('El grupo de mensajes seleccionado no es válido.')

            config['messages_by_group_key'][message_group] = normalized_rows
            return config

        raise ValueError(f'Bucket de mensajes inválido: {selected_bucket}')
