from __future__ import annotations

from dash import html

from src.shared.time.timestamps import parse_utc_datetime, to_santiago_display, utc_to_local

from ..models.alarm_image_admin_view_model import AlarmImageAdminDraft
from ..services.alarm_image_admin_status_service import AlarmImageAdminStatus


def build_alarm_image_admin_status_panel(
    status: AlarmImageAdminStatus, draft: AlarmImageAdminDraft | None
) -> html.Div:
    value, subtitle, color = _build_content_draft(draft=draft)

    return html.Div(
        className='alarm-image-definition-monitor',
        children=[
            _build_metric(title='Estado actual', value=value, subtitle=subtitle, color=color),
            _build_metric(
                title='Última publicación',
                value=_format_empty(status.last_published_at),
                subtitle=_build_publisher(status),
            ),
            _build_metric(
                title='Bundles',
                value=f'{status.ready_count}/{status.bundle_count} disponibles',
                subtitle=(
                    f'{status.pending_count} pendientes · '
                    f'{status.failed_count} fallidos · '
                    f'{_format_size(status.total_size_bytes)}'
                ),
            ),
            _build_metric(
                title='Última revisión local',
                value=_format_empty(status.last_runtime_check_at),
                subtitle=f'Próxima revisión: {_format_empty(status.next_runtime_check_at)}',
            ),
            _build_metric(
                title='Estado runtime',
                value='Con errores'
                if status.failed_count or status.last_runtime_error
                else 'Operativo',
                subtitle=status.last_runtime_error or 'Sin errores registrados.',
                color='danger'
                if bool(status.failed_count or status.last_runtime_error)
                else 'success',
            ),
        ],
    )


def _build_metric(
    *,
    title: str,
    value: str,
    subtitle: str,
    color: str = '',
) -> html.Div:
    information_color = {
        'danger': 'is-danger',
        'info': 'is-info',
        'warning': 'is-warning',
        'success': 'is-success',
    }
    class_name = 'alarm-image-definition-monitor-title-badge {0}'.format(
        information_color.get(color, 'd-none')
    )

    return html.Div(
        className='alarm-image-definition-monitor-card',
        children=[
            html.Div(
                className='d-flex align-items-start gap-1',
                children=[
                    html.P(className='alarm-image-definition-monitor-title', children=[title]),
                    html.Span(className=class_name),
                ],
            ),
            html.Div(
                className='alarm-image-definition-monitor-value',
                children=value,
            ),
            html.Div(
                className='alarm-image-definition-monitor-subtitle',
                children=subtitle,
            ),
        ],
    )


def _build_publisher(status: AlarmImageAdminStatus) -> str:
    if not status.last_published_by and not status.last_published_by_email:
        return 'Sin publicador registrado.'

    if status.last_published_by_email:
        return f'{status.last_published_by or "Usuario"} · {status.last_published_by_email}'

    return status.last_published_by or 'Usuario no registrado'


def _format_empty(value: str | None) -> str:
    if value is None:
        return 'Sin registro'

    return to_santiago_display(utc_to_local(value=parse_utc_datetime(value=value)))


def _format_size(size_bytes: int) -> str:
    if size_bytes <= 0:
        return '0 MB'

    size_mb = size_bytes / (1024 * 1024)
    return f'{size_mb:.2f} MB'


def _build_content_draft(draft: AlarmImageAdminDraft | None) -> tuple:
    if draft is None:
        return ('Cargando definiciones de imágenes...', 'Espere un momento', 'info')

    messages = {
        'processing': ['Procesando imágenes', 'Espere hasta que termine el proceso', 'info'],
        'error': [
            'No se pudieron publical los cambios',
            'La versión anterior sigue activa',
            'danger',
        ],
        'success': [
            'Cambios publicados correctamente',
            'Se renovaran las imágenes correspondientes',
            'success',
        ],
    }

    message = messages.get(draft.ui_state, None)
    if message is not None:
        return tuple(message)

    summary = draft.change_summary

    if not summary.has_changes:
        # success
        return (
            'Sin cambios pendientes',
            'Las imágenes se encuentran en la última versión',
            'success',
        )

    message = (
        'Cambios pendientes en orden en {0}'
        if summary.only_order_changes
        else 'Cambios pendientes en {0} grupo(s)'
    )

    return (message.format(summary.changed_group_count), 'Se deben publicar los datos', 'warning')
