from __future__ import annotations

AdminComponentId = dict[str, str]


def build_admin_component_ids(admin_key: str) -> dict[str, AdminComponentId]:
    return {
        'container': {'type': 'admin-container', 'admin': admin_key},
        'init': {'type': 'admin-init', 'admin': admin_key},
        'grid': {'type': 'admin-grid', 'admin': admin_key},
        'toast_host': {'type': 'admin-toast-host', 'admin': admin_key},
        'modal_host': {'type': 'admin-modal-host', 'admin': admin_key},
        'refresh_button': {'type': 'admin-refresh-button', 'admin': admin_key},
        'add_button': {'type': 'admin-add-button', 'admin': admin_key},
        'delete_button': {'type': 'admin-delete-button', 'admin': admin_key},
        'save_button': {'type': 'admin-save-button', 'admin': admin_key},
        'loading': {'type': 'admin-loading', 'admin': admin_key},
    }
