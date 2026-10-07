from __future__ import annotations

from typing import Any, Sequence

from dash.development.base_component import Component

from ..primitives import DisplayCardType, build_display_card


def build_display_generic_card(
    uuid: str,
    name: str,
    card_class_name: str,
    children: Sequence[Any] | None = None,
    wrapper_class_name: str | None = None,
    show_identifier: bool = False,
    show_definition: bool = False,
    enable_status_backdrop: bool = False,
    status_backdrop_message: str = 'Datos desactualizados',
) -> Component:
    return build_display_card(
        card_type=DisplayCardType.GENERIC,
        uuid=uuid,
        name=name,
        children=children,
        card_class_name=card_class_name,
        wrapper_class_name=wrapper_class_name,
        show_identifier=show_identifier,
        show_definition=show_definition,
        enable_status_backdrop=enable_status_backdrop,
        status_backdrop_message=status_backdrop_message,
    )
