from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import dcc, html

from src.features.admin_framework.components import build_admin_page_header
from src.features.configuration.admin_panels.alarm_management.images.definitions.alarm_image_configuration_definition import (
    ALARM_IMAGE_CONFIGURATION_ADMIN_DEFINITION,
)

from .ids import AlarmImageDefinitionIds


def build_alarm_image_definition_layout() -> html.Div:
    return html.Div(
        id=AlarmImageDefinitionIds.ROOT,
        className='alarm-image-definition-root',
        children=[
            dcc.Interval(
                id=AlarmImageDefinitionIds.INIT_TRIGGER,
                interval=250,
                max_intervals=1,
            ),
            dcc.Store(
                id=AlarmImageDefinitionIds.STORE_DRAFT,
                storage_type='memory',
            ),
            build_admin_page_header(ALARM_IMAGE_CONFIGURATION_ADMIN_DEFINITION.title),
            html.Main(
                className='alarm-image-definition-page-main',
                children=[
                    _information(),
                    dcc.Loading(
                        id=AlarmImageDefinitionIds.MAIN_LOADER,
                        type='default',
                        delay_show=0,
                        show_initially=True,
                        display='show',
                        className='loading-component-spinner',
                        parent_className='alarm-image-definition-loader',
                        children=[
                            html.Div(id=AlarmImageDefinitionIds.MONITOR),
                            html.Div(
                                id=AlarmImageDefinitionIds.MAIN_DEFINITION_SHELL,
                                className='alarm-image-definition-shell',
                                children=[
                                    _build_nav(),
                                    html.Div(
                                        className='alarm-image-definition-images-card d-flex flex-fill h-100 w-100',
                                        children=[
                                            html.Div(
                                                id=AlarmImageDefinitionIds.IMAGE_PANEL,
                                                className='alarm-image-definition-images-card-body w-100 h-100',
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


def _information() -> html.Div:
    return html.Div(
        className='alarm-image-definition-page-header',
        children=[
            html.Div(
                className='alarm-image-definition-page-title-block',
                children=[
                    html.H4(
                        'Imágenes de alarmas',
                        className='alarm-image-definition-title',
                    ),
                    html.Div(
                        'Administra imágenes asociadas a grupos de alarmas.',
                        className='alarm-image-definition-description',
                    ),
                ],
            ),
            html.Div(
                className='alarm-image-definition-header-actions',
                children=[
                    dbc.Button(
                        id=AlarmImageDefinitionIds.REFRESH_BUTTON,
                        color='secondary',
                        outline=True,
                        size='md',
                        className='alarm-image-definition-header-button',
                        children=['Actualizar'],
                    ),
                    dbc.Button(
                        id=AlarmImageDefinitionIds.PUBLISH_BUTTON,
                        color='dark',
                        outline=True,
                        size='md',
                        disabled=True,
                        className='alarm-image-definition-header-button',
                        children=['Guardar / Publicar cambios'],
                    ),
                ],
            ),
        ],
    )


def _build_nav() -> html.Div:
    return html.Div(
        className='alarm-image-definition-nav-card d-flex flex-fill flex-column h-100',
        children=[
            html.Div(
                className='alarm-image-definition-card-header',
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                className='alarm-image-definition-card-title',
                                children='Grupos de alarmas',
                            ),
                            html.Div(
                                className='alarm-image-definition-card-subtitle',
                                children='Selecciona el grupo que recibirá imágenes.',
                            ),
                        ],
                    ),
                ],
            ),
            html.Div(
                className='alarm-image-definition-search-wrapper',
                children=[
                    dbc.Input(
                        id=AlarmImageDefinitionIds.SEARCH_INPUT,
                        placeholder='Buscar grupo...',
                        size='sm',
                        debounce=True,
                        className='alarm-image-definition-search',
                    ),
                ],
            ),
            html.Div(
                id=AlarmImageDefinitionIds.GROUP_LIST,
                className='alarm-image-definition-group-list-wrapper',
            ),
            html.Div(
                className='alarm-image-definition-pagination',
                children=[
                    dbc.Button(
                        html.I(className='bi bi-chevron-left'),
                        id=AlarmImageDefinitionIds.GROUP_PREVIOUS_PAGE,
                        color='light',
                        size='sm',
                        className='alarm-image-definition-pagination-button',
                    ),
                    html.Span(
                        id=AlarmImageDefinitionIds.GROUP_PAGE_LABEL,
                        className='alarm-image-definition-page-label',
                    ),
                    dbc.Button(
                        html.I(className='bi bi-chevron-right'),
                        id=AlarmImageDefinitionIds.GROUP_NEXT_PAGE,
                        color='light',
                        size='sm',
                        className='alarm-image-definition-pagination-button',
                    ),
                ],
            ),
        ],
    )
