from __future__ import annotations

from src.shared.ui.app_header_shell.app_header_admin_shell import build_app_header_admin_shell


def build_admin_page_header(title: str):
    return build_app_header_admin_shell(
        title=title,
    )
