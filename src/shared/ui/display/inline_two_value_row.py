from __future__ import annotations

from dash import html
from dash.development.base_component import Component

from ..theme import resolve_color_class


def build_inline_two_values_row(
    label: str | Component,
    first_label: str | None,
    first_value: str | html.Img | None,
    second_label: str | None,
    second_value: str | html.Img | None,
    first_color: str | None = None,
    first_unit: str | Component | None = None,
    first_value_class_name: str | None = None,
    second_color: str | None = None,
    second_unit: str | Component | None = None,
    second_value_class_name: str | None = None,
    container_class_name: str = 'app-border-bottom pt-1',
    font_size_class_name: str = 'font-size-200',
    divider_value: str | None = '/',
) -> html.Div:
    # 1. Limpiar fw-bold del segundo valor para que NO se imponga la negrita
    raw_class = _resolve_class_name(color=second_color, class_name=second_value_class_name) or ''
    clean_second_class = raw_class.replace('fw-bold', '').strip()
    second_classes = f"{clean_second_class} text-muted fw-normal".strip()

    # 2. Estilos para el plan (gris suave y peso normal)
    second_style = dict(_resolve_style(color=second_color) or {})
    second_style.setdefault('color', '#8c8c8c')
    second_style['fontWeight'] = '400'
    second_style['opacity'] = '0.8'

    # 3. Estilos para el separador '/'
    divider_style = {
        'color': '#8c8c8c',
        'fontWeight': '400',
        'opacity': '0.8',
    }

    return html.Div(
        className=f'd-flex justify-content-between {container_class_name} {font_size_class_name}',
        children=[
            html.P(children=[_safe_text(value=label)]),
            html.Div(
                className='d-flex',
                children=[
                    html.P(className='pe-1', children=[_safe_text(value=first_label)]),
                    html.P(
                        className=_resolve_class_name(
                            color=first_color, class_name=first_value_class_name
                        ),
                        style=_resolve_style(color=first_color),
                        children=[_safe_text(value=first_value)],
                    ),
                    _safe_unit(value=first_unit),
                    html.P(
                        className='px-1 text-muted fw-normal',
                        style=divider_style,
                        children=[divider_value],
                    ),
                    html.P(className='pe-1', children=[_safe_text(value=second_label)]),
                    html.P(
                        className=second_classes,
                        style=second_style,
                        children=[_safe_text(value=second_value)],
                    ),
                    _safe_unit(value=second_unit),
                ],
            ),
        ],
    )

def _safe_unit(value: str | None) -> Component | None:
    return (
        html.P(style={'paddingLeft': '.1rem'}, children=[_safe_text(value=value)])
        if value is not None
        else None
    )


def _safe_text(value: str | None | Component) -> Component | str:
    if value is None:
        return ''
    return value


def _resolve_style(color: str | None) -> dict[str, str] | None:
    """Aplica color inline si el valor es un código hexadecimal o rgb."""
    if color and isinstance(color, str) and (color.startswith('#') or color.startswith('rgb')):
        return {'color': color}
    return None


def _resolve_class_name(
    *,
    color: str | None = None,
    class_name: str | None = None,
) -> str:
    color_class = resolve_color_class(value=color or '0') if color and not color.startswith('#') else ''
    classes = ['fw-bold', color_class, class_name or '']
    return ' '.join(classes).strip()