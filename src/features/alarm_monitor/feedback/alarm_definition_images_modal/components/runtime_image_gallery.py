from __future__ import annotations

import dash_bootstrap_components as dbc
from dash import html

from src.features.configuration.admin_panels.alarm_management.images.models.alarm_image_runtime_view_model import (
    AlarmImageRuntimeGroup,
)


def build_alarm_image_runtime_gallery(
    *,
    image_group: AlarmImageRuntimeGroup,
) -> html.Div:
    if not image_group.has_images:
        return html.Div(
            className='alarm-image-runtime-images-gallery '
            ' d-flex flex-column align-items-center justify-content-center w-100',
            children=[
                html.I(className='bi bi-image alarm-image-definition-empty-icon'),
                html.P(
                    className='alarm-image-definition-text-empty',
                    children='No hay una definición asociada a la alarma',
                ),
            ],
        )

    return html.Div(
        className='alarm-image-runtime-images-gallery',
        children=[_build_image_carousel(image_group=image_group)],
    )


def _build_image_carousel(image_group: AlarmImageRuntimeGroup) -> dbc.Carousel:
    return dbc.Carousel(
        items=[
            {'key': index, 'src': image.full_url}
            for index, image in enumerate(image_group.images, start=1)
        ],
        indicators=False,
        controls=len(image_group.images) > 1,
    )
