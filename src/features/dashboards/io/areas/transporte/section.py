from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from .builders.slot_builder import (
    build_no_operativo_container,
    build_tiempos_colas_container,
    build_transporte_global_container,
    build_transporte_ready_flag,
)

_CLASS_COMPONENT = 'background-secondary h-100 d-flex'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_transporte_section():
    return build_section_shell(
        title='TRANSPORTE',
        content_id='transporte-section',
        children=[
            build_display_io_card(
                uuid='transporte-global-main-card',
                name='Transporte Global • Turno',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_transporte_global_container(),
                    build_transporte_ready_flag(),
                ],
            ),
            build_display_io_card(
                uuid='no-operativo-main-card',
                name='N° Operativo • Turno',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_no_operativo_container(),
                ],
            ),
            build_display_io_card(
                uuid='tiempos-colas-main-card',
                name='Tiempos y Colas • Turno',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_tiempos_colas_container(),
                ],
            ),
        ],
    )
