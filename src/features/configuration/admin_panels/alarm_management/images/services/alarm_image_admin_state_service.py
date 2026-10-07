from __future__ import annotations

from ..models.alarm_image_admin_view_model import (
    DELETED_STATUS,
    NEW_STATUS,
    PUBLISHED_STATUS,
    REORDERED_STATUS,
    REPLACED_STATUS,
    AlarmImageAdminDraft,
    AlarmImageAdminGroup,
    AlarmImageAdminImage,
    AlarmImageChangeSummary,
)


class AlarmImageAdminStateService:
    def build_initial_draft(
        self,
        *,
        message_groups: list[dict],
        published_images: list[dict],
        page_size: int = 8,
    ) -> AlarmImageAdminDraft:
        images_by_group = self._group_images_by_message_group_key(published_images)

        groups = [
            AlarmImageAdminGroup(
                message_group_key=str(group['message_group_key']),
                label=str(group.get('label') or group['message_group_key']),
                alarm_count=int(group.get('alarm_count') or 0),
                images=images_by_group.get(str(group['message_group_key']), []),
            )
            for group in message_groups
            if group.get('message_group_key')
        ]

        groups.sort(key=lambda group: group.label.lower())

        selected_message_group_key = groups[0].message_group_key if groups else None

        draft = AlarmImageAdminDraft(
            groups=groups,
            selected_message_group_key=selected_message_group_key,
            page_size=page_size,
            ui_state='idle',
        )

        draft.change_summary = self.summarize_changes(draft)
        return draft

    @staticmethod
    def update_search(
        *,
        draft: AlarmImageAdminDraft,
        search_text: str,
    ) -> AlarmImageAdminDraft:
        draft.search_text = search_text or ''
        draft.current_page = 1
        return draft

    @staticmethod
    def go_previous_page(draft: AlarmImageAdminDraft) -> AlarmImageAdminDraft:
        draft.current_page = max(1, draft.current_page - 1)
        return draft

    def go_next_page(self, draft: AlarmImageAdminDraft) -> AlarmImageAdminDraft:
        total_pages = self.get_total_pages(draft)
        draft.current_page = min(total_pages, draft.current_page + 1)
        return draft

    @staticmethod
    def select_group(
        *,
        draft: AlarmImageAdminDraft,
        message_group_key: str,
    ) -> AlarmImageAdminDraft:
        if any(group.message_group_key == message_group_key for group in draft.groups):
            draft.selected_message_group_key = message_group_key
        return draft

    def add_image(
        self,
        *,
        draft: AlarmImageAdminDraft,
        message_group_key: str,
        image_key: str,
        thumb_url: str,
        full_url: str,
        mime_type: str,
        content_hash: str,
        source_filename: str,
        draft_file_path: str,
    ) -> AlarmImageAdminDraft:
        group = self._find_group(draft, message_group_key)
        if group is None:
            return draft

        next_order = len(group.active_images) + 1

        group.images.append(
            AlarmImageAdminImage(
                message_group_key=message_group_key,
                image_key=image_key,
                order=next_order,
                thumb_url=thumb_url,
                full_url=full_url,
                thumb_mime_type=mime_type,
                full_mime_type=mime_type,
                content_hash=content_hash,
                status=NEW_STATUS,
                published_order=None,
                source_filename=source_filename,
                draft_file_path=draft_file_path,
            )
        )

        self._normalize_orders(group)
        draft.ui_state = 'dirty'
        draft.change_summary = self.summarize_changes(draft)
        return draft

    def replace_image(
        self,
        *,
        draft: AlarmImageAdminDraft,
        message_group_key: str,
        image_key: str,
        thumb_url: str,
        full_url: str,
        mime_type: str,
        content_hash: str,
        source_filename: str,
        draft_file_path: str,
    ) -> AlarmImageAdminDraft:
        group = self._find_group(draft, message_group_key)
        if group is None:
            return draft

        image = self._find_image(group, image_key)
        if image is None or image.status == DELETED_STATUS:
            return draft

        image.thumb_url = thumb_url
        image.full_url = full_url
        image.thumb_mime_type = mime_type
        image.full_mime_type = mime_type
        image.content_hash = content_hash
        image.source_filename = source_filename
        image.draft_file_path = draft_file_path

        if image.status != NEW_STATUS:
            image.status = REPLACED_STATUS

        self._normalize_orders(group)
        draft.ui_state = 'dirty'
        draft.change_summary = self.summarize_changes(draft)
        return draft

    def move_image_up(
        self,
        *,
        draft: AlarmImageAdminDraft,
        message_group_key: str,
        image_key: str,
    ) -> AlarmImageAdminDraft:
        group = self._find_group(draft, message_group_key)
        if group is None:
            return draft

        images = group.active_images
        index = self._find_image_index(images, image_key)
        if index is None or index <= 0:
            return draft

        images[index - 1], images[index] = images[index], images[index - 1]

        self._apply_active_order(group, images)
        self._refresh_order_statuses(group)

        draft.change_summary = self.summarize_changes(draft)
        draft.ui_state = 'dirty' if draft.change_summary.has_changes else 'idle'
        return draft

    def move_image_down(
        self,
        *,
        draft: AlarmImageAdminDraft,
        message_group_key: str,
        image_key: str,
    ) -> AlarmImageAdminDraft:
        group = self._find_group(draft, message_group_key)
        if group is None:
            return draft

        images = group.active_images
        index = self._find_image_index(images, image_key)
        if index is None or index >= len(images) - 1:
            return draft

        images[index], images[index + 1] = images[index + 1], images[index]

        self._apply_active_order(group, images)
        self._refresh_order_statuses(group)

        draft.change_summary = self.summarize_changes(draft)
        draft.ui_state = 'dirty' if draft.change_summary.has_changes else 'idle'
        return draft

    def delete_image(
        self,
        *,
        draft: AlarmImageAdminDraft,
        message_group_key: str,
        image_key: str,
    ) -> AlarmImageAdminDraft:
        group = self._find_group(draft, message_group_key)
        if group is None:
            return draft

        image = self._find_image(group, image_key)
        if image is None:
            return draft

        if image.status == NEW_STATUS:
            group.images = [
                existing_image
                for existing_image in group.images
                if existing_image.image_key != image_key
            ]
        else:
            image.status = DELETED_STATUS

        self._normalize_orders(group)
        draft.ui_state = 'dirty' if self.summarize_changes(draft).has_changes else 'idle'
        draft.change_summary = self.summarize_changes(draft)
        return draft

    @staticmethod
    def get_filtered_groups(draft: AlarmImageAdminDraft) -> list[AlarmImageAdminGroup]:
        search_text = draft.search_text.strip().lower()

        if not search_text:
            return draft.groups

        return [
            group
            for group in draft.groups
            if search_text in group.label.lower() or search_text in group.message_group_key.lower()
        ]

    def get_page_groups(self, draft: AlarmImageAdminDraft) -> list[AlarmImageAdminGroup]:
        filtered_groups = self.get_filtered_groups(draft)
        total_pages = self.get_total_pages(draft)

        draft.current_page = min(max(1, draft.current_page), total_pages)

        start = (draft.current_page - 1) * draft.page_size
        end = start + draft.page_size
        return filtered_groups[start:end]

    def get_total_pages(self, draft: AlarmImageAdminDraft) -> int:
        filtered_count = len(self.get_filtered_groups(draft))
        if filtered_count == 0:
            return 1

        return max(1, (filtered_count + draft.page_size - 1) // draft.page_size)

    @staticmethod
    def summarize_changes(draft: AlarmImageAdminDraft) -> AlarmImageChangeSummary:
        changed_group_keys: set[str] = set()
        reordered_count = 0
        deleted_count = 0
        new_count = 0
        replaced_count = 0

        for group in draft.groups:
            for image in group.images:
                if image.status == REORDERED_STATUS:
                    reordered_count += 1
                    changed_group_keys.add(group.message_group_key)
                elif image.status == DELETED_STATUS:
                    deleted_count += 1
                    changed_group_keys.add(group.message_group_key)
                elif image.status == NEW_STATUS:
                    new_count += 1
                    changed_group_keys.add(group.message_group_key)
                elif image.status == REPLACED_STATUS:
                    replaced_count += 1
                    changed_group_keys.add(group.message_group_key)

        has_content_changes = any(
            [
                deleted_count,
                new_count,
                replaced_count,
            ]
        )

        has_order_changes = reordered_count > 0
        has_changes = has_content_changes or has_order_changes

        return AlarmImageChangeSummary(
            has_changes=has_changes,
            only_order_changes=has_order_changes and not has_content_changes,
            has_content_changes=has_content_changes,
            changed_group_count=len(changed_group_keys),
            reordered_count=reordered_count,
            deleted_count=deleted_count,
            new_count=new_count,
            replaced_count=replaced_count,
        )

    @staticmethod
    def _group_images_by_message_group_key(
        published_images: list[dict],
    ) -> dict[str, list[AlarmImageAdminImage]]:
        result: dict[str, list[AlarmImageAdminImage]] = {}

        for item in published_images:
            message_group_key = str(item.get('message_group_key') or '')
            if not message_group_key:
                continue

            order = int(item.get('order') or 1)

            image = AlarmImageAdminImage(
                message_group_key=message_group_key,
                image_key=str(item['image_key']),
                order=order,
                thumb_url=str(item.get('thumb_url') or ''),
                full_url=item.get('full_url'),
                thumb_mime_type=item.get('thumb_mime_type'),
                full_mime_type=item.get('full_mime_type'),
                content_hash=item.get('content_hash'),
                status=PUBLISHED_STATUS,
                published_order=order,
            )

            result.setdefault(message_group_key, []).append(image)

        for images in result.values():
            images.sort(key=lambda image: image.order)
            for index, image in enumerate(images, start=1):
                image.order = index
                image.published_order = index

        return result

    @staticmethod
    def _find_group(
        draft: AlarmImageAdminDraft,
        message_group_key: str,
    ) -> AlarmImageAdminGroup | None:
        for group in draft.groups:
            if group.message_group_key == message_group_key:
                return group
        return None

    @staticmethod
    def _find_image(
        group: AlarmImageAdminGroup,
        image_key: str,
    ) -> AlarmImageAdminImage | None:
        for image in group.images:
            if image.image_key == image_key:
                return image
        return None

    @staticmethod
    def _find_image_index(
        images: list[AlarmImageAdminImage],
        image_key: str,
    ) -> int | None:
        for index, image in enumerate(images):
            if image.image_key == image_key:
                return index
        return None

    @staticmethod
    def _apply_active_order(
        group: AlarmImageAdminGroup,
        active_images: list[AlarmImageAdminImage],
    ) -> None:
        for index, image in enumerate(active_images, start=1):
            image.order = index

        deleted_images = [image for image in group.images if image.status == DELETED_STATUS]

        group.images = active_images + deleted_images

    @staticmethod
    def _normalize_orders(group: AlarmImageAdminGroup) -> None:
        active_images = group.active_images

        for index, image in enumerate(active_images, start=1):
            image.order = index

        deleted_images = [image for image in group.images if image.status == DELETED_STATUS]

        group.images = active_images + deleted_images

    @staticmethod
    def _refresh_order_statuses(group: AlarmImageAdminGroup) -> None:
        for image in group.active_images:
            if image.status not in {PUBLISHED_STATUS, REORDERED_STATUS}:
                continue

            if image.published_order is not None and image.order != image.published_order:
                image.status = REORDERED_STATUS
            else:
                image.status = PUBLISHED_STATUS
