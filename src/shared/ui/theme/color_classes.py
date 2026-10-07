from __future__ import annotations

from typing import Literal

ColorType = Literal['background', 'text', 'border', 'hex']
SemanticColor = Literal['red', 'yellow', 'blue', '1', '2', '3']
VariantType = Literal['normal', 'soft', 'strong']

_HEX_COLORS = {
    'red': '#DC3545',
    'yellow': '#E0A800',
    'blue': '#4782B4',
}


def resolve_color_class(
    value: SemanticColor | str,
    color_type: ColorType = 'text',
    variant_type: VariantType = 'normal',
    default: str = '',
) -> str:
    if not isinstance(value, str):
        return default

    normalized_value = str(value).strip().lower()
    code_to_semantic = {'1': 'red', '2': 'yellow', '3': 'blue'}

    if value in code_to_semantic:
        normalized_value = code_to_semantic.get(normalized_value)
    else:
        return default

    variant = '' if variant_type == 'normal' else f'-{variant_type}'
    color = '{0}-{1}{2}'.format(color_type, normalized_value, variant).strip()

    if color_type == 'hex':
        color = _HEX_COLORS.get(normalized_value)

    return color


def resolve_h2s_color_class(value: str) -> str:
    colors = {
        '1': 'h2s-danger',
        '2': 'h2s-warning',
    }
    return colors.get(value, 'h2s-normal')
