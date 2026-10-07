from __future__ import annotations

from datetime import UTC, datetime

from ..models.alarm_image_bundle_manifest import AlarmImageBundleManifestRow
from .alarm_image_bundle_builder_service import AlarmImageBundleBuildResult
from .alarm_image_publication_actor_service import AlarmImagePublicationActor


class AlarmImageBundleManifestService:
    def merge_rebuilt_bundles(
        self,
        *,
        current_manifest_rows: list[AlarmImageBundleManifestRow],
        image_rows: list[dict],
        rebuilt_bundles: list[AlarmImageBundleBuildResult],
        uploaded_relative_paths: dict[str, str],
        actor: AlarmImagePublicationActor,
    ) -> list[AlarmImageBundleManifestRow]:
        rows_by_bundle_key = {row.bundle_key: row for row in current_manifest_rows}

        group_keys_by_bundle = self._build_group_keys_by_bundle(image_rows)
        now = datetime.now(UTC).isoformat()

        for rebuilt_bundle in rebuilt_bundles:
            bundle_key = rebuilt_bundle.bundle_key
            zip_file = rebuilt_bundle.zip_file

            rows_by_bundle_key[bundle_key] = AlarmImageBundleManifestRow(
                bundle_key=bundle_key,
                bundle_hash=rebuilt_bundle.bundle_hash,
                bundle_filename=zip_file.filename,
                bundle_relative_path=uploaded_relative_paths[bundle_key],
                size_bytes=zip_file.size_bytes,
                message_group_keys=group_keys_by_bundle.get(bundle_key, []),
                updated_at=now,
                published_at=now,
                published_by=actor.display_name,
                published_by_email=actor.email,
            )

        return [
            row for row in rows_by_bundle_key.values() if group_keys_by_bundle.get(row.bundle_key)
        ]

    @staticmethod
    def _build_group_keys_by_bundle(
        image_rows: list[dict],
    ) -> dict[str, list[str]]:
        result: dict[str, set[str]] = {}

        for row in image_rows:
            bundle_key = str(row.get('bundle_key') or '').strip()
            message_group_key = str(row.get('message_group_key') or '').strip()

            if not bundle_key or not message_group_key:
                continue

            result.setdefault(bundle_key, set()).add(message_group_key)

        return {bundle_key: sorted(group_keys) for bundle_key, group_keys in result.items()}
