from __future__ import annotations

from ..definitions.bundle_manifest_definition import (
    ALARM_IMAGE_BUNDLE_MANIFEST_ADMIN_DEFINITION,
)
from ..models.alarm_image_bundle_manifest import AlarmImageBundleManifestRow
from .admin_rows_data_accessor import AdminRowsDataAccessor


class AlarmImageBundleManifestRepository:
    def __init__(
        self,
        *,
        data_accessor: AdminRowsDataAccessor | None = None,
    ) -> None:
        self._data_accessor = data_accessor or AdminRowsDataAccessor()

    def load_rows(self) -> list[AlarmImageBundleManifestRow]:
        rows = self._data_accessor.load_rows(
            definition=ALARM_IMAGE_BUNDLE_MANIFEST_ADMIN_DEFINITION,
        )

        return [AlarmImageBundleManifestRow.from_dict(row) for row in rows if row.get('bundle_key')]

    def save_rows(self, rows: list[AlarmImageBundleManifestRow]) -> None:
        normalized_rows = sorted(
            rows,
            key=lambda row: row.bundle_key.lower(),
        )

        self._data_accessor.save_rows(
            definition=ALARM_IMAGE_BUNDLE_MANIFEST_ADMIN_DEFINITION,
            rows=[row.to_dict() for row in normalized_rows],
        )
