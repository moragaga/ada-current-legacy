from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from .builders.slot_builder import (
    build_carguio_ready_flag,
    build_equipos_servicio_container,
    build_mezcla_container,
)

_CLASS_COMPONENT = 'background-secondary h-100 d-flex'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_carguio_section():
    return build_section_shell(
        title='CARGUÍO',
        content_id='carguio-section',
        children=[
            build_display_io_card(
                uuid='equipos-servicio-main-card',
                name='Carguio Global - Turno',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[build_equipos_servicio_container(), build_carguio_ready_flag()],
            ),
            build_display_io_card(
                uuid='mezcla-main-card',
                name='Equipos de Servicio',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_mezcla_container(),
                ],
            ),
        ],
    )
