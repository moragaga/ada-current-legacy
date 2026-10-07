from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from .builders.slot_builder import (
    build_chancado_stmg_container,
    build_chancado_stmg_ready_flag,
)

_CLASS_COMPONENT = 'background-secondary h-100 d-flex'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_chancado_stmg_section():
    return build_section_shell(
        title='CHANCADO-STMG',
        content_id='chancado-stmg-section',
        children=[
            build_display_io_card(
                uuid='chancado-stmg-main-card',
                name='Chancado-STMG',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[build_chancado_stmg_container(), build_chancado_stmg_ready_flag()],
            ),
        ],
    )
