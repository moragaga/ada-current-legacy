from __future__ import annotations

import re

from dash import html

from ..ids import AlarmImageDefinitionIds
from ..models.alarm_image_admin_view_model import AlarmImageAdminDraft, AlarmImageAdminGroup
from ..services.alarm_image_admin_state_service import AlarmImageAdminStateService


def build_alarm_image_group_list(
    *,
    draft: AlarmImageAdminDraft,
    state_service: AlarmImageAdminStateService,
) -> html.Div:
    page_groups = state_service.get_page_groups(draft)

    if not draft.groups:
        return _build_empty_group_list(
            message='No se encontraron grupos en alarm_configuration.',
        )

    if not page_groups:
        return _build_empty_group_list(
            message='No hay grupos que coincidan con la búsqueda.',
        )

    fillers_needed = max(0, draft.page_size - len(page_groups))

    children = [
        _build_group_card(
            group=group,
            selected=group.message_group_key == draft.selected_message_group_key,
        )
        for group in page_groups
    ]

    children.extend(_build_group_filler(index) for index in range(fillers_needed))

    return html.Div(
        className='alarm-image-definition-group-list',
        children=children,
    )


def build_group_page_label(
    *,
    draft: AlarmImageAdminDraft,
    state_service: AlarmImageAdminStateService,
) -> str:
    total_pages = state_service.get_total_pages(draft)

    if not draft.groups:
        return 'Sin grupos'

    return f'Página {draft.current_page} de {total_pages}'


def _build_group_card(
    *,
    group: AlarmImageAdminGroup,
    selected: bool,
) -> html.Div:
    class_name = 'alarm-image-definition-group-card'
    if selected:
        class_name += ' is-selected'

    image_text = (
        f'{group.image_count} imagen' if group.image_count == 1 else f'{group.image_count} imágenes'
    )
    alarm_text = (
        f'{group.alarm_count} alarma' if group.alarm_count == 1 else f'{group.alarm_count} alarmas'
    )
    # icon_id = _build_group_alarm_icon_id(group.message_group_key)

    return html.Div(
        className='alarm-image-definition-group-card-wrapper',
        children=[
            html.Button(
                id=AlarmImageDefinitionIds.group_card(group.message_group_key),
                type='button',
                className=class_name,
                children=[
                    html.Div(
                        className='alarm-image-definition-group-card-main',
                        children=[
                            html.Div(
                                className='alarm-image-definition-group-title',
                                children=group.message_group_key,
                            ),
                        ],
                    ),
                    html.Div(
                        className='alarm-image-definition-group-meta',
                        children=[
                            html.Span(alarm_text),
                            html.Span(' · '),
                            html.Span(image_text),
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_group_filler(index: int) -> html.Div:
    return html.Div(
        key=f'filler-{index}',
        className='alarm-image-definition-group-card-wrapper is-filler',
        children=[
            html.Div(
                className='alarm-image-definition-group-card is-filler',
            )
        ],
    )


def _build_empty_group_list(*, message: str) -> html.Div:
    return html.Div(
        className='alarm-image-definition-group-empty',
        children=[
            html.I(className='bi bi-inbox alarm-image-definition-panel-empty-icon'),
            html.Div(className='alarm-image-definition-panel-empty-text', children=[message]),
        ],
    )


def _build_group_alarm_icon_id(message_group_key: str) -> str:
    safe_key = re.sub(
        r'[^a-zA-Z0-9_-]+',
        '_',
        message_group_key.strip(),
    ).strip('_')

    return f'alarm-image-definition-group-info-{safe_key or "unknown"}'
