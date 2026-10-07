from __future__ import annotations

from enum import StrEnum
from typing import Sequence

import dash_bootstrap_components as dbc
from dash import html
from dash.development.base_component import Component


class DisplayCardType(StrEnum):
    GENERIC = 'generic'
    IO = 'io'


def build_display_card(
    *,
    card_type: DisplayCardType = DisplayCardType.GENERIC,
    uuid: str | None = None,
    name: str | None = None,
    children: Sequence[Component] | None = None,
    card_class_name: str | None = None,
    wrapper_class_name: str | None = None,
    show_identifier: bool = False,
    show_definition: bool = False,
    enable_status_backdrop: bool = False,
    status_backdrop_message: str = 'Datos desactualizados',
    status_backdrop_icon: str = 'bi bi-cloud-slash'
) -> Component:
    card_content = [
        html.Div(
            className='d-flex flex-column',
            children=children or [],
        ),
        _build_footer_component(
            card_type=card_type,
            uuid=uuid,
            name=name,
            show_identifier=show_identifier,
            show_definition=show_definition,
        ),
    ]

    status_backdrop = None

    if enable_status_backdrop:
        status_backdrop = _build_status_backdrop(
            uuid=uuid,
            message=status_backdrop_message,
            icon=status_backdrop_icon
        )

    return dbc.Row(
        className=_build_wrapper_class_name(
            class_name=wrapper_class_name,
        ),
        children=[
            dbc.Col(
                class_name='p-0',
                **dict.fromkeys(
                    ['xs', 'sm', 'md', 'lg', 'xl', 'xxl'],
                    12,
                ),
                children=[
                    _build_card_component(
                        card_type=card_type,
                        card_class_name=card_class_name,
                        content=card_content,
                        status_backdrop=status_backdrop,
                    )
                ],
            )
        ],
    )


def _build_card_component(
    *,
    card_type: DisplayCardType = DisplayCardType.GENERIC,
    card_class_name: str | None = None,
    content: Sequence[Component] | None = None,
    status_backdrop: Component | None = None,
) -> Component:
    card_children: list[Component] = [
        dbc.CardBody(
            className=(
                'd-flex flex-column '
                'justify-content-between h-100'
            ),
            children=content,
        )
    ]

    if status_backdrop is not None:
        card_children.append(status_backdrop)

    return dbc.Card(
        className=_build_card_class_name(
            card_type=card_type,
            class_name=card_class_name,
        ),
        children=card_children,
    )


def _build_status_backdrop(
    *,
    uuid: str | None,
    message: str,
    icon: str = 'bi bi-cloud-slash'
) -> Component:
    if not uuid:
        raise ValueError(
            '[ERROR] A display card with a status backdrop requires a uuid.'
        )
    _id = {
        'type': 'display-card-status-backdrop',
        'index': uuid,
    }
    _class_name = 'display-card-backdrop'
    if message == 'En construcción':
        _id = {}
        _class_name = 'display-card-backdrop display-card-backdrop--visible'

    return html.Div(
        id=_id,
        className=_class_name,
        children=[
            html.Div(
                className='display-card-backdrop__content',
                children=[
                    html.I(
                        className=(
                            f'{icon} '
                            'display-card-backdrop__icon'
                        ),
                    ),
                    html.P(
                        className='display-card-backdrop__message',
                        children=message,
                    ),
                ],
            ),
        ],
    )


def _build_card_class_name(
    *,
    card_type: DisplayCardType = DisplayCardType.GENERIC,
    class_name: str | None = None,
) -> str:
    classes = {
        DisplayCardType.GENERIC: 'display-card-content-wrapper',
        DisplayCardType.IO: 'display-io-card-content-wrapper',
    }

    return ' '.join(
        filter(
            None,
            [
                classes.get(card_type),
                'position-relative overflow-hidden',
                class_name,
            ],
        )
    )


def _build_wrapper_class_name(
    *,
    class_name: str | None = None,
) -> str:
    return ' '.join(
        filter(
            None,
            [
                class_name,
                'g-0',
            ],
        )
    )


def _build_footer_component(
    *,
    card_type: DisplayCardType = DisplayCardType.GENERIC,
    uuid: str | None = None,
    name: str | None = None,
    show_identifier: bool = False,
    show_definition: bool = False,
) -> Component:
    content = [
        html.Div(
            className='d-flex',
            children=[
                (
                    html.P(
                        className='fw-bold m-0',
                        children=[name],
                    )
                    if show_identifier
                    else None
                ),
                (
                    _display_definition(
                        card_type=card_type,
                        uuid=uuid,
                    )
                    if show_definition
                    else None
                ),
            ],
        ),
    ]

    alignment = 'center'

    if card_type == DisplayCardType.IO and uuid:
        content.append(
            html.Div(
                id=f'{uuid}-extra-footer-content',
            )
        )
        alignment = 'between'

    return html.Div(
        className='display-card-footer {0}'.format(
            (
                'position-relative'
                if card_type == DisplayCardType.GENERIC
                else ''
            )
        ).strip(),
        children=[
            html.Div(
                className=f'd-flex justify-content-{alignment}',
                children=content,
            )
        ],
    )


def _display_definition(
    *,
    uuid: str | None = None,
    card_type: DisplayCardType = DisplayCardType.GENERIC,
) -> Component:
    definition = html.I(
        className='bi bi-info-circle ps-1 active-cursor',
    )

    if card_type == DisplayCardType.GENERIC:
        definition = html.Div(
            className='position-absolute bottom-0 end-0',
            children=[definition],
        )

    return definition