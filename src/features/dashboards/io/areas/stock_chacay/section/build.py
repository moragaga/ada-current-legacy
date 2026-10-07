from __future__ import annotations

from src.shared.ui.app_dashboard_shell.section_shell import build_section_shell
from src.shared.ui.layout.io.display_io_card import build_display_io_card

from ..builders.builder import (
    build_stock_chacay_ready_flag,
    build_stockpile_chacay_container,
    build_tendencia_alimentado_container,
)

_CLASS_COMPONENT = 'background-secondary h-100 d-flex disabled'
_CLASS_WRAPPER = 'd-flex flex-fill p-0 m-0'


def build_stock_chacay_section():
    return build_section_shell(
        title='STOCKPILE CHACAY',
        content_id='stock-chacay-section',
        children=[
            build_display_io_card(
                uuid='stockpile-chacay-main-card',
                name='Stockpile Chacay',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                status_backdrop_message='En construcción',
                status_backdrop_icon='bi bi-hammer',
                children=[build_stockpile_chacay_container(), build_stock_chacay_ready_flag()],
            ),
            build_display_io_card(
                uuid='tendencia-alimentado-main-card',
                name='Tendencia Alimentado',
                card_class_name=_CLASS_COMPONENT,
                wrapper_class_name=_CLASS_WRAPPER,
                show_identifier=True,
                show_definition=False,
                enable_status_backdrop=True,
                status_backdrop_message='En construcción',
                status_backdrop_icon='bi bi-hammer',
                children=[build_tendencia_alimentado_container()],
            ),
        ],
    )
