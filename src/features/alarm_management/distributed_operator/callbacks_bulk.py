from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from typing import Any

from dash import (
    ALL,
    Input,
    Output,
    State,
    ctx,
    html,
    no_update,
)
from dash.exceptions import PreventUpdate
from flask import session

from src.app.dash import get_dash_app
from src.app.dependencies import get_alarm_management_use_case_service
from src.shared.ui.status.running_button import build_running_button_children

from ..core.models import (
    AlarmManagementRequest,
    AlarmManagementUser,
)
from .ids import (
    DISTRIBUTED_ALARM_BULK_MANAGEMENT_OPEN_BUTTON_TYPE,
    DISTRIBUTED_ALARM_BULK_MANAGEMENT_SOURCE_STORE_TYPE,
    build_distributed_alarm_management_operator_ids,
    get_distributed_alarm_bulk_open_payload_from_trigger,
)
from .models.distributed_alarm_management_modal_view_model import (
    DistributedAlarmManagementFeedbackViewModel,
    DistributedAlarmManagementModalViewModel,
)
from .services.distributed_alarm_management_modal_presenter import (
    DistributedAlarmManagementModalPresenter,
)


def register_distributed_alarm_bulk_management_callback() -> None:
    app = get_dash_app()
    ids = build_distributed_alarm_management_operator_ids()

    @app.callback(
        Output(
            component_id=ids['bulk_alarm_list_collapse'],
            component_property='is_open',
            allow_duplicate=True,
        ),
        Input(component_id=ids['bulk_alarm_list_button'], component_property='n_clicks'),
        State(component_id=ids['bulk_alarm_list_collapse'], component_property='is_open'),
        prevent_initial_call=True,
    )
    def toggle_distributed_bulk_alarm_list_collapse(
        n_clicks,
        is_open,
    ):
        if ctx.triggered_id is None or n_clicks is None:
            raise PreventUpdate

        return not is_open

    @app.callback(
        Output(component_id=ids['bulk_context_store'], component_property='data'),
        Output(component_id=ids['feedback_store'], component_property='data', allow_duplicate=True),
        Output(component_id=ids['bulk_validation_attempt_store'], component_property='data'),
        Input(
            component_id={
                'type': DISTRIBUTED_ALARM_BULK_MANAGEMENT_OPEN_BUTTON_TYPE,
                'group_key': ALL,
            },
            component_property='n_clicks',
        ),
        State(
            component_id={
                'type': DISTRIBUTED_ALARM_BULK_MANAGEMENT_SOURCE_STORE_TYPE,
                'group_key': ALL,
            },
            component_property='id',
        ),
        State(
            component_id={
                'type': DISTRIBUTED_ALARM_BULK_MANAGEMENT_SOURCE_STORE_TYPE,
                'group_key': ALL,
            },
            component_property='data',
        ),
        prevent_initial_call=True,
    )
    def open_distributed_bulk_management_modal(
        _open_clicks,
        source_ids,
        source_values,
    ):
        if _get_triggered_n_clicks() <= 0:
            raise PreventUpdate

        open_payload = get_distributed_alarm_bulk_open_payload_from_trigger(
            triggered_id=ctx.triggered_id,
        )

        if open_payload is None:
            raise PreventUpdate

        source_payload = _find_source_payload(
            group_key=open_payload['group_key'],
            source_ids=source_ids,
            source_values=source_values,
        )

        if not source_payload:
            feedback = DistributedAlarmManagementFeedbackViewModel(
                is_open=True,
                kind='empty',
                title='Información',
                message='No se encontraron alarmas para gestionar.',
            )

            return None, _feedback_to_store(feedback=feedback), False

        bulk_context, status_counter = _build_distributed_bulk_context(
            source_payload=source_payload,
        )

        if bulk_context is None:
            feedback = _build_bulk_open_feedback(
                group_label=str(
                    source_payload.get('group_label') or source_payload.get('group_key') or 'grupo'
                ),
                statuses=status_counter,
            )

            return None, _feedback_to_store(feedback=feedback), False

        return bulk_context, None, False

    @app.callback(
        Output(component_id=ids['bulk_modal'], component_property='is_open'),
        Output(component_id=ids['bulk_title'], component_property='children'),
        Output(component_id=ids['bulk_summary'], component_property='children'),
        Output(component_id=ids['bulk_alarm_list'], component_property='children'),
        Output(component_id=ids['bulk_message_dropdown'], component_property='options'),
        Output(component_id=ids['bulk_message_dropdown'], component_property='disabled'),
        Output(component_id=ids['bulk_message_dropdown'], component_property='value'),
        Output(component_id=ids['bulk_personalized_message'], component_property='value'),
        Input(component_id=ids['bulk_context_store'], component_property='data'),
        prevent_initial_call=False,
    )
    def render_distributed_bulk_management_modal(context_data):
        if not context_data:
            return False, 'Gestión masiva', '', [], [], True, None, ''

        alarm_items = context_data.get('alarm_items') or []
        message_options = context_data.get('message_options') or []
        group_label = context_data.get('group_label') or 'grupo'

        return (
            bool(context_data.get('is_open')),
            f'Gestión masiva {group_label}',
            f'Se gestionarán {len(alarm_items)} alarma(s) del grupo {group_label}.',
            _build_bulk_alarm_list(alarm_items=alarm_items),
            message_options,
            not bool(message_options),
            context_data.get('selected_message_id'),
            context_data.get('personalized_message') or '',
        )

    @app.callback(
        Output(component_id=ids['bulk_silence_container'], component_property='className'),
        Output(component_id=ids['bulk_silence_dropdown'], component_property='options'),
        Output(component_id=ids['bulk_silence_dropdown'], component_property='disabled'),
        Output(component_id=ids['bulk_silence_dropdown'], component_property='value'),
        Output(component_id=ids['bulk_silence_information'], component_property='children'),
        Output(component_id=ids['bulk_silence_checkbox'], component_property='value'),
        Output(component_id=ids['bulk_silence_checkbox'], component_property='disabled'),
        Input(component_id=ids['bulk_context_store'], component_property='data'),
        Input(component_id=ids['bulk_message_dropdown'], component_property='value'),
        Input(component_id=ids['bulk_silence_checkbox'], component_property='value'),
        prevent_initial_call=False,
    )
    def update_distributed_bulk_silence_controls(
        context_data,
        selected_message_id,
        silence_requested,
    ):
        if not context_data:
            return 'd-none', [], True, None, '', False, True

        silence_options = context_data.get('silence_options') or []
        base_information = context_data.get('silence_information') or ''

        selected_message = _find_selected_message(
            context_data=context_data,
            selected_message_id=selected_message_id,
        )

        manual_silence_allowed = _is_manual_silence_allowed(
            context_data=context_data,
        )

        message_policy_code = _get_selected_message_policy_code(
            selected_message=selected_message,
        )

        message_authorizes_silence = _message_authorizes_silence(
            policy_code=message_policy_code,
        )

        if ctx.triggered_id in {
            ids['bulk_context_store'],
            ids['bulk_message_dropdown'],
        }:
            silence_requested = False

        silence_checkbox_disabled = not silence_options or (
            not manual_silence_allowed and not message_authorizes_silence
        )

        if silence_checkbox_disabled:
            if not silence_options:
                information = 'No existen opciones disponibles para desactivar las alarmas.'
            elif not manual_silence_allowed:
                information = (
                    'Estas alarmas no permiten desactivación libre. '
                    'Selecciona un mensaje predefinido autorizado para desactivarlas.'
                )
            else:
                information = base_information

            return (
                'd-none',
                silence_options,
                True,
                None,
                information,
                False,
                True,
            )

        if not silence_requested:
            return (
                'd-none',
                silence_options,
                True,
                None,
                base_information,
                False,
                False,
            )

        if selected_message and not _to_bool(
            selected_message.get('allow_silence_edit'),
            default=True,
        ):
            return (
                'd-none',
                silence_options,
                True,
                message_policy_code or None,
                'El mensaje seleccionado usa una política de silencio definida.',
                True,
                False,
            )

        return (
            '',
            silence_options,
            False,
            None,
            base_information,
            True,
            False,
        )

    @app.callback(
        Output(component_id=ids['bulk_message_validation'], component_property='className'),
        Output(component_id=ids['bulk_message_validation'], component_property='children'),
        Output(
            component_id=ids['bulk_personalized_message_validation'], component_property='className'
        ),
        Output(
            component_id=ids['bulk_personalized_message_validation'], component_property='children'
        ),
        Output(component_id=ids['bulk_silence_validation'], component_property='className'),
        Output(component_id=ids['bulk_silence_validation'], component_property='children'),
        Input(component_id=ids['bulk_validation_attempt_store'], component_property='data'),
        Input(component_id=ids['bulk_message_dropdown'], component_property='value'),
        Input(component_id=ids['bulk_personalized_message'], component_property='value'),
        Input(component_id=ids['bulk_silence_checkbox'], component_property='value'),
        Input(component_id=ids['bulk_silence_dropdown'], component_property='value'),
        State(component_id=ids['bulk_context_store'], component_property='data'),
        prevent_initial_call=False,
    )
    def render_distributed_bulk_form_validation(
        validation_attempted,
        selected_message_id,
        personalized_message,
        silence_requested,
        selected_silence_policy_code,
        context_data,
    ):
        if not context_data:
            return _empty_form_validation()

        if not validation_attempted:
            return _empty_form_validation()

        errors = _get_form_validation_errors(
            selected_message_id=selected_message_id,
            personalized_message=personalized_message,
            silence_requested=bool(silence_requested),
            selected_silence_policy_code=selected_silence_policy_code,
        )

        return (
            _validation_class(message=errors.get('message')),
            errors.get('message') or '',
            _validation_class(message=errors.get('personalized_message')),
            errors.get('personalized_message') or '',
            _validation_class(message=errors.get('silence')),
            errors.get('silence') or '',
        )

    @app.callback(
        Output(
            component_id=ids['bulk_context_store'], component_property='data', allow_duplicate=True
        ),
        Output(component_id=ids['feedback_store'], component_property='data', allow_duplicate=True),
        Output(
            component_id=ids['bulk_validation_attempt_store'],
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=ids['bulk_modal_save_button'], component_property='n_clicks'),
        State(component_id=ids['bulk_context_store'], component_property='data'),
        State(component_id=ids['bulk_message_dropdown'], component_property='value'),
        State(component_id=ids['bulk_personalized_message'], component_property='value'),
        State(component_id=ids['bulk_silence_checkbox'], component_property='value'),
        State(component_id=ids['bulk_silence_dropdown'], component_property='value'),
        running=[
            (
                Output(component_id=ids['bulk_modal_save_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['bulk_modal_cancel_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['bulk_modal_close_button'], component_property='className'),
                'bi bi-x-lg text-muted',
                'bi bi-x-lg active-cursor',
            ),
            (
                Output(component_id=ids['bulk_modal_save_button'], component_property='children'),
                build_running_button_children(text='Gestionando'),
                'Gestionar grupo',
            ),
        ],
        prevent_initial_call=True,
    )
    def save_distributed_bulk_management(
        n_clicks,
        context_data,
        selected_message_id,
        personalized_message,
        silence_requested,
        selected_silence_policy_code,
    ):
        if not n_clicks:
            raise PreventUpdate

        if not context_data:
            feedback = DistributedAlarmManagementFeedbackViewModel(
                is_open=True,
                kind='error',
                title='Error',
                message='No existe contexto de gestión masiva.',
            )

            return None, _feedback_to_store(feedback=feedback), False

        local_errors = _get_form_validation_errors(
            selected_message_id=selected_message_id,
            personalized_message=personalized_message,
            silence_requested=bool(silence_requested),
            selected_silence_policy_code=selected_silence_policy_code,
        )

        if local_errors:
            return no_update, no_update, True

        alarm_items = context_data.get('alarm_items') or []

        if not alarm_items:
            feedback = DistributedAlarmManagementFeedbackViewModel(
                is_open=True,
                kind='empty',
                title='Información',
                message='No hay alarmas para gestionar.',
            )

            return None, _feedback_to_store(feedback=feedback), False

        statuses: Counter[str] = Counter()

        for item in alarm_items:
            try:
                request = _build_management_request_from_alarm_item(
                    item=item,
                    selected_message_id=selected_message_id,
                    personalized_message=personalized_message,
                    silence_requested=bool(silence_requested),
                    selected_silence_policy_code=selected_silence_policy_code,
                )

                if not request.alarm_id or not request.alarm_key:
                    statuses['validation_error'] += 1
                    continue

                result = get_alarm_management_use_case_service().manage_alarm(
                    request=request,
                    user=_build_user_from_session(),
                )

                statuses[result.status] += 1

            except Exception:
                statuses['error'] += 1

        feedback = _build_bulk_feedback(
            group_label=context_data.get('group_label') or 'grupo',
            statuses=statuses,
        )

        return None, _feedback_to_store(feedback=feedback), False

    @app.callback(
        Output(
            component_id=ids['bulk_alarm_list_collapse'],
            component_property='is_open',
            allow_duplicate=True,
        ),
        Output(
            component_id=ids['bulk_context_store'], component_property='data', allow_duplicate=True
        ),
        Output(
            component_id=ids['bulk_validation_attempt_store'],
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=ids['bulk_modal_close_button'], component_property='n_clicks'),
        Input(component_id=ids['bulk_modal_cancel_button'], component_property='n_clicks'),
        prevent_initial_call=True,
    )
    def close_distributed_bulk_management_modal(
        close_clicks,
        cancel_clicks,
    ):
        if not close_clicks and not cancel_clicks:
            raise PreventUpdate

        return None, False, False


def _build_distributed_bulk_context(
    *,
    source_payload: dict[str, Any],
) -> tuple[dict[str, Any] | None, Counter[str]]:
    service = get_alarm_management_use_case_service()

    group_key = str(source_payload.get('group_key') or '').strip()
    group_label = str(source_payload.get('group_label') or group_key or 'grupo').strip()
    icon_class_name = str(source_payload.get('icon_class_name') or '').strip()

    source_items = [
        item for item in source_payload.get('alarm_items') or [] if isinstance(item, dict)
    ]

    alarm_items: list[dict[str, Any]] = []
    first_modal_data: dict[str, Any] | None = None
    seen_alarm_ids: set[str] = set()
    status_counter: Counter[str] = Counter()

    for item in source_items:
        alarm_id = str(item.get('alarm_id') or '').strip()
        alarm_key = str(item.get('alarm_key') or '').strip()

        if not alarm_id or not alarm_key:
            status_counter['validation_error'] += 1
            continue

        if alarm_id in seen_alarm_ids:
            continue

        seen_alarm_ids.add(alarm_id)

        try:
            result = service.build_context(
                alarm_id=alarm_id,
                alarm_key=alarm_key,
                group_occurrence_id=str(item.get('group_occurrence_id') or '').strip(),
                visibility_group_key=str(item.get('visibility_group_key') or '').strip(),
                management_scope_key=str(item.get('management_scope_key') or '').strip(),
                priority_order=_optional_int(item.get('priority_order')),
            )

            status_counter[result.status] += 1

            if not result.is_ready or result.context is None:
                continue

            presentation = DistributedAlarmManagementModalPresenter.present_context_result(
                result=result,
            )

            modal_data = _modal_to_store(
                modal=presentation.modal,
            )

            if modal_data is None:
                continue

            if first_modal_data is None:
                first_modal_data = modal_data

            alarm_items.append(
                _build_bulk_alarm_item(
                    source_item=item,
                    modal_data=modal_data,
                    is_stale=result.context.is_stale,
                )
            )

        except Exception:
            status_counter['error'] += 1

    if not alarm_items or first_modal_data is None:
        return None, status_counter

    return {
        'is_open': True,
        'group_key': group_key,
        'group_label': group_label,
        'icon_class_name': icon_class_name,
        'alarm_items': alarm_items,
        'message_options': _safe_list_from_modal_data(
            modal_data=first_modal_data,
            key='message_options',
        ),
        'messages_by_id': _safe_dict_from_modal_data(
            modal_data=first_modal_data,
            key='messages_by_id',
        ),
        'silence_options': _safe_list_from_modal_data(
            modal_data=first_modal_data,
            key='silence_options',
        ),
        'silence_information': first_modal_data.get('silence_information') or '',
        'context_data': first_modal_data.get('context_data') or {},
        'selected_message_id': None,
        'personalized_message': '',
        'silence_requested': False,
        'selected_silence_policy_code': None,
    }, status_counter


def _build_bulk_alarm_item(
    *,
    source_item: dict[str, Any],
    modal_data: dict[str, Any],
    is_stale: bool,
) -> dict[str, Any]:
    alarm_key = modal_data.get('alarm_key') or source_item.get('alarm_key') or ''

    alarm_title = (
        modal_data.get('alarm_title')
        or source_item.get('alarm_display_name')
        or source_item.get('alarm_name')
        or source_item.get('title')
        or alarm_key
    )

    return {
        'alarm_id': str(modal_data.get('alarm_id') or source_item.get('alarm_id') or '').strip(),
        'group_occurrence_id': str(
            modal_data.get('group_occurrence_id') or source_item.get('group_occurrence_id') or ''
        ).strip(),
        'alarm_key': str(alarm_key).strip(),
        'visibility_group_key': str(
            modal_data.get('visibility_group_key') or source_item.get('visibility_group_key') or ''
        ).strip(),
        'management_scope_key': str(
            modal_data.get('management_scope_key') or source_item.get('management_scope_key') or ''
        ).strip(),
        'priority_order': _optional_int(
            modal_data.get('priority_order')
            if modal_data.get('priority_order') is not None
            else source_item.get('priority_order')
        ),
        'target_occurrence_started_at': _resolve_target_occurrence_started_at(
            modal_data=modal_data,
            source_item=source_item,
        ),
        'operator_bucket': str(
            modal_data.get('operator_bucket') or source_item.get('operator_bucket') or 'default'
        ).strip(),
        'alarm_display_name': str(alarm_title).strip(),
        'title': str(alarm_title).strip(),
        'cause': str(modal_data.get('alarm_cause') or source_item.get('cause') or '').strip(),
        'alarm_kind': str(source_item.get('alarm_kind') or '').strip(),
        'color': str(source_item.get('color') or '').strip(),
        'late_management_candidate': bool(is_stale),
    }


def _build_management_request_from_alarm_item(
    *,
    item: dict[str, Any],
    selected_message_id: str | None,
    personalized_message: str | None,
    silence_requested: bool,
    selected_silence_policy_code: str | None,
) -> AlarmManagementRequest:
    return AlarmManagementRequest(
        alarm_id=str(item.get('alarm_id') or '').strip(),
        group_occurrence_id=str(item.get('group_occurrence_id') or '').strip(),
        alarm_key=str(item.get('alarm_key') or '').strip(),
        visibility_group_key=str(item.get('visibility_group_key') or '').strip(),
        management_scope_key=str(item.get('management_scope_key') or '').strip(),
        priority_order=_optional_int(item.get('priority_order')),
        target_occurrence_started_at=str(item.get('target_occurrence_started_at') or '').strip(),
        selected_message_id=selected_message_id,
        personalized_message=str(personalized_message or '').strip(),
        silence_requested=silence_requested,
        selected_silence_policy_code=selected_silence_policy_code,
    )


def _find_source_payload(
    *,
    group_key: str,
    source_ids: list[dict[str, Any]] | None,
    source_values: list[Any] | None,
) -> dict[str, Any] | None:
    if not source_ids or not source_values:
        return None

    for source_id, source_value in zip(source_ids, source_values, strict=False):
        if not isinstance(source_id, dict):
            continue

        if str(source_id.get('group_key') or '').strip() != group_key:
            continue

        if isinstance(source_value, dict):
            return source_value

    return None


def _build_bulk_alarm_list(
    *,
    alarm_items: list[dict[str, Any]],
) -> list:
    return [
        html.Div(
            className='border rounded-2 py-1 px-2 background-primary',
            children=[
                html.Div(
                    className='d-flex justify-content-between align-items-center',
                    children=[
                        html.Strong(
                            className='bulk-alarm-management-list-title',
                            children=item.get('alarm_display_name') or item.get('alarm_key') or '',
                        ),
                    ],
                ),
                html.Div(
                    className='bulk-alarm-management-list-cause',
                    children=item.get('cause') or '',
                ),
            ],
        )
        for item in alarm_items
    ]


def _build_bulk_feedback(
    *,
    group_label: str,
    statuses: Counter[str],
) -> DistributedAlarmManagementFeedbackViewModel:
    total = sum(statuses.values())

    lines = [
        f'Gestión masiva {group_label} procesada para {total} alarma(s).',
    ]

    if statuses.get('success'):
        lines.append(f'{statuses["success"]} registrada(s) correctamente.')

    if statuses.get('exists'):
        lines.append(f'{statuses["exists"]} ya estaba(n) gestionada(s).')

    if statuses.get('empty'):
        lines.append(f'{statuses["empty"]} ya no estaba(n) activa(s).')

    if statuses.get('management_disabled'):
        lines.append(f'{statuses["management_disabled"]} no permite(n) gestión.')

    if statuses.get('validation_error'):
        lines.append(f'{statuses["validation_error"]} tuvo/tuvieron error de validación.')

    if statuses.get('error'):
        lines.append(f'{statuses["error"]} falló/fallaron por error técnico.')

    kind = 'success'

    if statuses.get('error') or statuses.get('validation_error'):
        kind = 'error'

    return DistributedAlarmManagementFeedbackViewModel(
        is_open=True,
        kind=kind,
        title='Información',
        message=' '.join(lines),
    )


def _modal_to_store(
    *,
    modal: DistributedAlarmManagementModalViewModel,
) -> dict[str, Any] | None:
    if not modal.is_open or modal.context_data is None:
        return None

    return asdict(modal)


def _feedback_to_store(
    *,
    feedback: DistributedAlarmManagementFeedbackViewModel,
) -> dict[str, Any] | None:
    if not feedback.is_open:
        return None

    return asdict(feedback)


def _find_selected_message(
    *,
    context_data: dict[str, Any],
    selected_message_id: str | None,
) -> dict[str, Any] | None:
    if not selected_message_id:
        return None

    messages_by_id = context_data.get('messages_by_id') or {}
    message = messages_by_id.get(selected_message_id)

    if isinstance(message, dict):
        return message

    return None


def _build_user_from_session() -> AlarmManagementUser:
    identity = session.get('identity') or {}

    email = str(identity.get('email') or '').strip()
    name = str(identity.get('name') or identity.get('display_name') or email or 'Usuario').strip()

    return AlarmManagementUser(
        email=email,
        name=name,
    )


def _get_form_validation_errors(
    *,
    selected_message_id: str | None,
    personalized_message: str | None,
    silence_requested: bool,
    selected_silence_policy_code: str | None,
) -> dict[str, str]:
    errors: dict[str, str] = {}

    has_message = bool(str(selected_message_id or '').strip())
    has_personalized_message = bool(str(personalized_message or '').strip())

    if not has_message and not has_personalized_message:
        message = 'Selecciona un mensaje predefinido o ingresa una descripción.'

        errors['message'] = message
        errors['personalized_message'] = message

    if silence_requested and not str(selected_silence_policy_code or '').strip():
        errors['silence'] = 'Selecciona una duración de inactividad.'

    return errors


def _empty_form_validation() -> tuple[str, str, str, str, str, str]:
    return (
        'd-none',
        '',
        'd-none',
        '',
        'd-none',
        '',
    )


def _validation_class(
    *,
    message: str | None,
) -> str:
    return '' if message else 'd-none'


def _to_bool(
    value: Any,
    *,
    default: bool,
) -> bool:
    if value is None:
        return default

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.strip().lower() in {'true', '1', 'yes', 'si', 'sí'}

    return bool(value)


def _optional_int(value: Any) -> int | None:
    if value is None or value == '':
        return None

    try:
        return int(float(value))
    except Exception:
        return None


def _get_triggered_n_clicks() -> int:
    if not ctx.triggered:
        return 0

    value = ctx.triggered[0].get('value')

    try:
        return int(value or 0)
    except Exception:
        return 0


def _is_manual_silence_allowed(
    *,
    context_data: dict[str, Any],
) -> bool:
    data = context_data.get('context_data') or {}

    if not isinstance(data, dict):
        return False

    return _to_bool(
        data.get('allow_manual_silence'),
        default=False,
    )


def _get_selected_message_policy_code(
    *,
    selected_message: dict[str, Any] | None,
) -> str:
    if not selected_message:
        return ''

    return str(selected_message.get('silence_policy_code') or '').strip().lower()


def _message_authorizes_silence(
    *,
    policy_code: str,
) -> bool:
    return policy_code not in {
        '',
        'inherit',
        'none',
    }


def _safe_list_from_modal_data(
    *,
    modal_data: dict[str, Any] | None,
    key: str,
) -> list[dict[str, Any]]:
    if not modal_data:
        return []

    value = modal_data.get(key)

    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]

    if isinstance(value, tuple):
        return [item for item in value if isinstance(item, dict)]

    return []


def _safe_dict_from_modal_data(
    *,
    modal_data: dict[str, Any] | None,
    key: str,
) -> dict[str, Any]:
    if not modal_data:
        return {}

    value = modal_data.get(key)

    if isinstance(value, dict):
        return value

    return {}


def _build_bulk_open_feedback(
    *,
    group_label: str,
    statuses: Counter[str],
) -> DistributedAlarmManagementFeedbackViewModel:
    total = sum(statuses.values())

    if total <= 0:
        return DistributedAlarmManagementFeedbackViewModel(
            is_open=True,
            kind='empty',
            title='Información',
            message='No se encontraron alarmas para gestionar.',
        )

    if statuses.get('exists') == total:
        return DistributedAlarmManagementFeedbackViewModel(
            is_open=True,
            kind='exists',
            title='Información',
            message=f'Todas las alarmas del grupo {group_label} ya fueron gestionadas.',
        )

    if statuses.get('management_disabled') == total:
        return DistributedAlarmManagementFeedbackViewModel(
            is_open=True,
            kind='management_disabled',
            title='Información',
            message=f'Las alarmas del grupo {group_label} no permiten gestión.',
        )

    if statuses.get('empty') == total:
        return DistributedAlarmManagementFeedbackViewModel(
            is_open=True,
            kind='empty',
            title='Información',
            message=f'No hay alarmas activas gestionables para el grupo {group_label}.',
        )

    lines = [
        f'No hay alarmas gestionables para abrir el grupo {group_label}.',
    ]

    if statuses.get('exists'):
        lines.append(f'{statuses["exists"]} ya estaba(n) gestionada(s).')

    if statuses.get('empty'):
        lines.append(f'{statuses["empty"]} no tiene(n) contexto activo o tardío disponible.')

    if statuses.get('management_disabled'):
        lines.append(f'{statuses["management_disabled"]} no permite(n) gestión.')

    if statuses.get('validation_error'):
        lines.append(f'{statuses["validation_error"]} tiene(n) datos incompletos.')

    if statuses.get('error'):
        lines.append(f'{statuses["error"]} falló/fallaron por error técnico.')

    kind = 'empty'

    if statuses.get('error') or statuses.get('validation_error'):
        kind = 'error'
    elif statuses.get('exists'):
        kind = 'exists'
    elif statuses.get('management_disabled'):
        kind = 'management_disabled'

    return DistributedAlarmManagementFeedbackViewModel(
        is_open=True,
        kind=kind,
        title='Información',
        message=' '.join(lines),
    )


def _resolve_target_occurrence_started_at(
    *,
    modal_data: dict[str, Any],
    source_item: dict[str, Any],
) -> str:
    candidates = (
        modal_data.get('target_occurrence_started_at'),
        source_item.get('target_occurrence_started_at'),
        source_item.get('start_timestamp'),
    )

    context_data = modal_data.get('context_data')

    if isinstance(context_data, dict):
        candidates = (
            *candidates,
            context_data.get('target_occurrence_started_at'),
            context_data.get('start_timestamp'),
        )

    for value in candidates:
        normalized_value = str(value or '').strip()

        if normalized_value:
            return normalized_value

    return ''
