from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from .builders.slot_builder import (
    build_general_mina_ready_flag,
    build_movimiento_mina_container,
    build_mp10_container,
    build_perforacion_container,
    build_remanentes_container,
)

_CLASS_COMPONENT = 'background-secondary h-100 d-flex'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_general_mina_section():
    return build_section_shell(
        title='GENERAL MINA',
        content_id='general-mina-section',
        children=[
            build_display_io_card(
                uuid='movimiento-mina-main-card',
                name='Movimiento Mina',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_movimiento_mina_container(),
                    build_general_mina_ready_flag(),
                ],
            ),
            build_display_io_card(
                uuid='remanentes-main-card',
                name='Remanentes',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_remanentes_container(),
                ],
            ),
            build_display_io_card(
                uuid='perforacion-main-card',
                name='Perforación',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_perforacion_container(),
                ],
            ),
            build_display_io_card(
                uuid='mp10-main-card',
                name='MP10',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_mp10_container(),
                ],
            ),
        ],
    )
