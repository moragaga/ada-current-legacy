from __future__ import annotations

from typing import Literal

from dash import html

InvalidType = Literal['invalid_data', 'not_mapped', 'empty_data', 'internal_error']


def build_alerting_icon(invalid_type: InvalidType) -> html.Img:
    return html.Img(
        src=f'assets/img/icons/{invalid_type}.svg', className='img-fluid invalid-value-icon'
    )
