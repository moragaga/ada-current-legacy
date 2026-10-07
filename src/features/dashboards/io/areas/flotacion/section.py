from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from src.features.dashboards.io.areas.flotacion.builders.slot_builder import (
    build_colectiva_container,
    build_flotacion_ready_flag,
    build_selectiva_container,
)

_CLASS_COMPONENT = 'background-secondary h-100 d-flex'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_flotacion_section():
    return build_section_shell(
        title='FLOTACIÓN',
        content_id='flotacion-section',
        children=[
            build_display_io_card(
                uuid='colectiva-main-card',
                name='Colectiva',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[build_colectiva_container(), build_flotacion_ready_flag()],
            ),
            build_display_io_card(
                uuid='selectiva-main-card',
                name='Selectiva',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                children=[
                    build_selectiva_container(),
                ],
            ),
        ],
    )
