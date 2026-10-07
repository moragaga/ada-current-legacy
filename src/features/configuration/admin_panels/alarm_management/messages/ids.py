from __future__ import annotations

from .constants import ALARM_MANAGEMENT_MESSAGES_ADMIN_KEY


def build_alarm_management_message_admin_ids() -> dict[str, str]:
    base = ALARM_MANAGEMENT_MESSAGES_ADMIN_KEY

    return {
        'container': f'{base}-container',
        'init': f'{base}-init-store',
        'snapshot': f'{base}-snapshot-store',
        'bucket_selector': f'{base}-bucket-selector',
        'grid': f'{base}-grid',
        'reload_button': f'{base}-reload-button',
        'add_row_button': f'{base}-add-row-button',
        'delete_rows_button': f'{base}-delete-rows-button',
        'save_button': f'{base}-save-button',
        'toast_host': f'{base}-toast-host',
        'loading': f'{base}-loading',
    }
