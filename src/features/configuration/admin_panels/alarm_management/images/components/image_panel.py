from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from ..ids import AlarmImageDefinitionIds
from ..models.alarm_image_admin_view_model import (
    DELETED_STATUS,
    NEW_STATUS,
    REORDERED_STATUS,
    REPLACED_STATUS,
    AlarmImageAdminDraft,
    AlarmImageAdminGroup,
    AlarmImageAdminImage,
)

_UPLOAD_ACCEPT = 'image/jpeg,image/png'


def build_alarm_image_panel(draft: AlarmImageAdminDraft) -> html.Div:
    if not draft.groups:
        return html.Div(
            className='alarm-image-definition-empty-panel h-100',
            children=[
                html.I(className='bi bi-images alarm-image-definition-panel-empty-icon'),
                html.Div(
                    className='alarm-image-definition-panel-empty-text',
                    children=['No hay grupos disponibles para administrar imágenes.'],
                ),
            ],
        )

    group = _get_selected_group(draft)

    if group is None:
        return html.Div(
            className='alarm-image-definition-empty-panel h-100',
            children=[
                html.I(className='bi bi-arrow-left-circle alarm-image-definition-panel-empty-icon'),
                html.Div(
                    className='alarm-image-definition-panel-empty-text',
                    children=['Selecciona un grupo para administrar sus imágenes.'],
                ),
            ],
        )

    images = group.active_images

    if not images:
        image_cards = [
            html.Div(
                className='alarm-image-definition-empty-images',
                children=[
                    html.I(className='bi bi-image alarm-image-definition-panel-empty-icon'),
                    html.Div(
                        className='alarm-image-definition-panel-empty-text',
                        children=['Este grupo todavía no tiene imágenes.'],
                    ),
                    html.Div(
                        className='alarm-image-definition-panel-empty-help',
                        children=['Agrega una imagen para comenzar.'],
                    ),
                ],
            )
        ]
    else:
        image_cards = [
            _build_image_card(
                image=image,
                index=index,
                total=len(images),
            )
            for index, image in enumerate(images, start=1)
        ]

    return html.Div(
        className='alarm-image-definition-panel h-100',
        children=[
            html.Div(
                className='alarm-image-definition-panel-header',
                children=[
                    html.Div(
                        className='alarm-image-definition-panel-title-block',
                        children=[
                            html.Div(
                                className='alarm-image-definition-panel-title',
                                children=group.message_group_key,
                            ),
                            html.Div(
                                className='alarm-image-definition-panel-subtitle',
                                children=[
                                    html.Span(
                                        f'{group.alarm_count} alarma'
                                        if group.alarm_count == 1
                                        else f'{group.alarm_count} alarmas'
                                    ),
                                    html.Span(' · '),
                                    html.Span(
                                        f'{group.image_count} imagen'
                                        if group.image_count == 1
                                        else f'{group.image_count} imágenes'
                                    ),
                                ],
                            ),
                        ],
                    ),
                    html.Div(
                        className='alarm-image-definition-upload-wrapper',
                        children=[
                            dcc.Upload(
                                id=AlarmImageDefinitionIds.add_image_upload(
                                    group.message_group_key,
                                ),
                                accept=_UPLOAD_ACCEPT,
                                multiple=False,
                                className='alarm-image-definition-upload',
                                children=dbc.Button(
                                    [
                                        html.I(className='bi bi-plus-lg me-1'),
                                        'Agregar imagen',
                                    ],
                                    color='dark',
                                    outline=True,
                                    size='sm',
                                    className='alarm-image-definition-add-button',
                                ),
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className='alarm-image-definition-image-grid',
                children=image_cards,
            ),
        ],
    )


def _build_image_card(
    *,
    image: AlarmImageAdminImage,
    index: int,
    total: int,
) -> html.Div:
    return html.Div(
        className='alarm-image-definition-image-card d-flex flex-column justify-content-center',
        children=[
            html.Div(
                className='alarm-image-definition-image-card-top',
                children=[
                    html.Div(
                        className='alarm-image-definition-image-label',
                        children=f'Imagen {index}',
                    ),
                    _build_status_badge(image.status),
                ],
            ),
            html.Div(
                className='alarm-image-definition-thumb-frame',
                children=html.Img(
                    src=image.thumb_url,
                    className='alarm-image-definition-thumb',
                )
                if image.thumb_url
                else html.Div(
                    className='alarm-image-definition-thumb-placeholder',
                    children='Sin vista previa',
                ),
            ),
            html.Div(
                className='alarm-image-definition-image-actions',
                children=[
                    dbc.Button(
                        html.I(className='bi bi-arrow-up'),
                        id=AlarmImageDefinitionIds.image_move_up(
                            image.message_group_key,
                            image.image_key,
                        ),
                        color='light',
                        size='sm',
                        disabled=index == 1,
                        className='alarm-image-definition-icon-button',
                    ),
                    dbc.Button(
                        html.I(className='bi bi-arrow-down'),
                        id=AlarmImageDefinitionIds.image_move_down(
                            image.message_group_key,
                            image.image_key,
                        ),
                        color='light',
                        size='sm',
                        disabled=index == total,
                        className='alarm-image-definition-icon-button',
                    ),
                    dcc.Upload(
                        id=AlarmImageDefinitionIds.image_replace_upload(
                            image.message_group_key,
                            image.image_key,
                        ),
                        accept=_UPLOAD_ACCEPT,
                        multiple=False,
                        className='alarm-image-definition-replace-upload',
                        children=dbc.Button(
                            color='dark',
                            outline=True,
                            size='sm',
                            className='alarm-image-definition-action-button',
                            children=['Reemplazar'],
                        ),
                    ),
                    html.Div(
                        className='alarm-image-definition-replace-upload',
                        children=[
                            dbc.Button(
                                id=AlarmImageDefinitionIds.image_delete(
                                    image.message_group_key,
                                    image.image_key,
                                ),
                                color='danger',
                                outline=True,
                                size='sm',
                                className='alarm-image-definition-action-button',
                                children=['Eliminar'],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _build_status_badge(status: str) -> dbc.Badge:
    statuses = {
        DELETED_STATUS: ('Eliminada', 'danger'),
        REORDERED_STATUS: ('Orden', 'warning'),
        NEW_STATUS: ('Nueva', 'info'),
        REPLACED_STATUS: ('Reemplazada', 'warning'),
    }
    children, color = statuses.get(status, ('Publicada', 'secondary'))
    return dbc.Badge(
        className='alarm-image-definition-image-badge', children=[children], color=color, pill=True
    )


def _get_selected_group(draft: AlarmImageAdminDraft) -> AlarmImageAdminGroup | None:
    for group in draft.groups:
        if group.message_group_key == draft.selected_message_group_key:
            return group
    return None
