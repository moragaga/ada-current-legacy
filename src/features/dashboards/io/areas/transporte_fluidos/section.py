from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from .builders.slot_builder import (
    build_sta_container,
    build_stc_container,
    build_str_container,
    build_tranque_container,
    build_transporte_fluidos_ready_flag,
)

_CLASS_COMPONENT = 'background-secondary h-100 d-flex disabled'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_transporte_fluidos_section():
    return build_section_shell(
        title='TRANSPORTE DE FLUIDOS',
        content_id='transporte-fluidos-section',
        children=[
            build_display_io_card(
                uuid='str-main-card',
                name='STR',
                card_class_name=_CLASS_COMPONENT.replace('disabled', '').strip(),
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=False,
                status_backdrop_message='En construcción',
                status_backdrop_icon='bi bi-hammer',
                children=[build_str_container(), build_transporte_fluidos_ready_flag()],
            ),
            build_display_io_card(
                uuid='stc-main-card',
                name='STC',
                card_class_name=_CLASS_COMPONENT.replace('disabled', '').strip(),
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=False,
                status_backdrop_message='En construcción',
                status_backdrop_icon='bi bi-hammer',
                children=[
                    build_stc_container(),
                ],
            ),
            build_display_io_card(
                uuid='tranque-main-card',
                name='Tranque',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                status_backdrop_message='En construcción',
                status_backdrop_icon='bi bi-hammer',
                children=[
                    build_tranque_container(),
                ],
            ),
            build_display_io_card(
                uuid='sta-main-card',
                name='STA',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                status_backdrop_message='En construcción',
                status_backdrop_icon='bi bi-hammer',
                children=[
                    build_sta_container(),
                ],
            ),
        ],
    )
