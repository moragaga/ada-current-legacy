from __future__ import annotations

from collections import defaultdict

from ..models.alarm_image_admin_view_model import (
    DELETED_STATUS,
    AlarmImageAdminDraft,
)


class AlarmImageBundleShardPlanner:
    def __init__(
        self,
        *,
        max_groups_per_bundle: int = 10,
    ) -> None:
        self._max_groups_per_bundle = max_groups_per_bundle

    def build_group_bundle_map(
        self,
        *,
        current_rows: list[dict],
        draft: AlarmImageAdminDraft,
    ) -> dict[str, str]:
        group_bundle_map = self._load_existing_group_bundle_map(current_rows)
        bundle_groups = self._build_bundle_groups(group_bundle_map)

        for group in draft.groups:
            if group.message_group_key in group_bundle_map:
                continue

            if not group.active_images:
                continue

            bundle_key = self._find_bundle_with_space(bundle_groups)

            if bundle_key is None:
                bundle_key = self._build_next_bundle_key(bundle_groups)

            group_bundle_map[group.message_group_key] = bundle_key
            bundle_groups[bundle_key].add(group.message_group_key)

        return group_bundle_map

    def get_affected_bundle_keys(
        self,
        *,
        current_rows: list[dict],
        draft: AlarmImageAdminDraft,
        group_bundle_map: dict[str, str],
    ) -> set[str]:
        current_group_bundle_map = self._load_existing_group_bundle_map(current_rows)
        affected_bundle_keys: set[str] = set()

        for group in draft.groups:
            has_content_change = any(
                image.status in {'new', 'replaced', DELETED_STATUS} for image in group.images
            )

            if not has_content_change:
                continue

            bundle_key = group_bundle_map.get(
                group.message_group_key
            ) or current_group_bundle_map.get(group.message_group_key)

            if bundle_key:
                affected_bundle_keys.add(bundle_key)

        return affected_bundle_keys

    @staticmethod
    def _load_existing_group_bundle_map(
        rows: list[dict],
    ) -> dict[str, str]:
        result: dict[str, str] = {}

        for row in rows:
            message_group_key = str(row.get('message_group_key') or '').strip()
            bundle_key = str(row.get('bundle_key') or '').strip()

            if not message_group_key:
                continue

            result[message_group_key] = bundle_key or 'bundle_001'

        return result

    @staticmethod
    def _build_bundle_groups(
        group_bundle_map: dict[str, str],
    ) -> dict[str, set[str]]:
        bundle_groups: dict[str, set[str]] = defaultdict(set)

        for message_group_key, bundle_key in group_bundle_map.items():
            bundle_groups[bundle_key].add(message_group_key)

        if not bundle_groups:
            bundle_groups['bundle_001'] = set()

        return bundle_groups

    def _find_bundle_with_space(
        self,
        bundle_groups: dict[str, set[str]],
    ) -> str | None:
        for bundle_key in sorted(bundle_groups):
            if len(bundle_groups[bundle_key]) < self._max_groups_per_bundle:
                return bundle_key

        return None

    @staticmethod
    def _build_next_bundle_key(
        bundle_groups: dict[str, set[str]],
    ) -> str:
        max_number = 0

        for bundle_key in bundle_groups:
            if not bundle_key.startswith('bundle_'):
                continue

            try:
                max_number = max(max_number, int(bundle_key.replace('bundle_', '', 1)))
            except ValueError:
                continue

        return f'bundle_{max_number + 1:03d}'
