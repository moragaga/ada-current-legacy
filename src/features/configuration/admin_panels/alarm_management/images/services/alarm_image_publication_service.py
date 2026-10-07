from __future__ import annotations

from collections.abc import Callable

from ..models.alarm_image_admin_view_model import AlarmImageAdminDraft
from ..models.alarm_image_publication import (
    CONTENT_MODE,
    ORDER_ONLY_MODE,
    AlarmImagePublicationResult,
)

PublishOrderChanges = Callable[[AlarmImageAdminDraft], AlarmImagePublicationResult]
PublishContentChanges = Callable[[AlarmImageAdminDraft], AlarmImagePublicationResult]


class AlarmImagePublicationService:
    def __init__(
        self,
        *,
        publish_order_changes: PublishOrderChanges,
        publish_content_changes: PublishContentChanges,
    ) -> None:
        self._publish_order_changes = publish_order_changes
        self._publish_content_changes = publish_content_changes

    def publish(self, draft: AlarmImageAdminDraft) -> AlarmImagePublicationResult:
        summary = draft.change_summary

        if not summary.has_changes:
            return AlarmImagePublicationResult.ok(
                mode=ORDER_ONLY_MODE,
                message='No existen cambios pendientes.',
            )

        if summary.only_order_changes:
            return self._safe_publish_order_changes(draft)

        return self._safe_publish_content_changes(draft)

    def _safe_publish_order_changes(
        self,
        draft: AlarmImageAdminDraft,
    ) -> AlarmImagePublicationResult:
        try:
            return self._publish_order_changes(draft)
        except Exception as exc:
            return AlarmImagePublicationResult.fail(
                mode=ORDER_ONLY_MODE,
                message=f'No se pudo guardar el orden de las imágenes. Detalle: {exc}',
            )

    def _safe_publish_content_changes(
        self,
        draft: AlarmImageAdminDraft,
    ) -> AlarmImagePublicationResult:
        try:
            return self._publish_content_changes(draft)
        except Exception as exc:
            return AlarmImagePublicationResult.fail(
                mode=CONTENT_MODE,
                message=f'No se pudieron publicar las imágenes. Detalle: {exc}',
            )


def build_empty_publish_order_changes() -> PublishOrderChanges:
    def _publish_order_changes(_: AlarmImageAdminDraft) -> AlarmImagePublicationResult:
        return AlarmImagePublicationResult.ok(
            mode=ORDER_ONLY_MODE,
            message='Cambios de orden guardados correctamente.',
        )

    return _publish_order_changes


def build_empty_publish_content_changes() -> PublishContentChanges:
    def _publish_content_changes(_: AlarmImageAdminDraft) -> AlarmImagePublicationResult:
        return AlarmImagePublicationResult.ok(
            mode=CONTENT_MODE,
            message='Cambios de imágenes publicados correctamente.',
        )

    return _publish_content_changes
