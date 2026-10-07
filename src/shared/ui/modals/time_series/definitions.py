from __future__ import annotations

from .models import TimeSeriesVariantsData

MODAL_VARIANTS: TimeSeriesVariantsData = TimeSeriesVariantsData(
    backdrop='static',
    centered=True,
    keyboard=False,
    close_button=False,
    header_class_name='modal-background',
    header_font_color_class_name='text-white',
    body_class_name='background-primary',
    body_font_color_class_name='font-custom-text-color',
    footer_class_name='modal-background',
    footer_font_color_class_name='text-white',
    width='80%',
    font_size_class_name='font-custom-text-size',
)
