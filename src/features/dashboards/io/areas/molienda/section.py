from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from .builders.slot_builder import build_molienda_container, build_molienda_ready_flag

_CLASS_COMPONENT = 'background-secondary h-100 d-flex'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_molienda_section():
    return build_section_shell(
        title='MOLIENDA',
        content_id='molienda-section',
        children=[
            build_display_io_card(
                uuid='molienda-main-card',
                name='Molienda',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[build_molienda_container(), build_molienda_ready_flag()],
            ),
        ],
    )
