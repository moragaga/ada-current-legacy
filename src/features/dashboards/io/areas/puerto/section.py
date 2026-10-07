from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from .builders.slot_builder import (
    build_desaladora_container,
    build_puerto_container,
    build_puerto_ready_flag,
)

_CLASS_COMPONENT = 'background-secondary h-100 d-flex disabled'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_puerto_section():
    return build_section_shell(
        title='PUERTO',
        content_id='puerto-section',
        children=[
            build_display_io_card(
                uuid='puerto-main-card',
                name='Puerto',
                card_class_name=_CLASS_COMPONENT.replace('disabled', '').strip(),
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=False,
                status_backdrop_message='En construcción',
                status_backdrop_icon='bi bi-hammer',
                children=[build_puerto_container()],
            ),
            build_display_io_card(
                uuid='desaladora-main-card',
                name='Desaladora',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                status_backdrop_message='En construcción',
                status_backdrop_icon='bi bi-hammer',
                children=[build_desaladora_container(), build_puerto_ready_flag()],
            ),
        ],
    )
