from __future__ import annotations

from src.shared.ui.feedback.notifications.toast import build_toast


class AdminFeedbackService:
    @staticmethod
    def build_success(message: str):
        return build_toast(
            header='Guardado exitoso',
            message=message,
            icon='success',
        )

    @staticmethod
    def build_error(message: str | list[str]):
        return build_toast(
            header='Error',
            message=message,
            icon='danger',
        )

    @staticmethod
    def build_warning(message: str | list[str]):
        return build_toast(
            header='Advertencia',
            message=message,
            icon='warning',
        )
