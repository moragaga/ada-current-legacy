from __future__ import annotations

from dataclasses import asdict
from typing import Any

from dash import (
    ALL,
    Input,
    Output,
    State,
    ctx,
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
    ALARM_MANAGEMENT_OPEN_BUTTON_TYPE,
    build_alarm_management_operator_ids,
    get_alarm_open_payload_from_trigger,
)
from .models.alarm_management_modal_view_model import (
    AlarmManagementFeedbackViewModel,
    AlarmManagementModalViewModel,
)
from .services.alarm_management_modal_presenter import (
    AlarmManagementModalPresenter,
)


def register_alarm_management_operator_callback() -> None:
    app = get_dash_app()
    ids = build_alarm_management_operator_ids()

    @app.callback(
        Output(component_id=ids['context_store'], component_property='data'),
        Output(component_id=ids['feedback_store'], component_property='data'),
        Output(component_id=ids['validation_attempt_store'], component_property='data'),
        Input(
            component_id={
                'type': ALARM_MANAGEMENT_OPEN_BUTTON_TYPE,
                'alarm_id': ALL,
                'group_occurrence_id': ALL,
                'alarm_key': ALL,
                'visibility_group_key': ALL,
                'management_scope_key': ALL,
                'priority_order': ALL,
                'target_occurrence_started_at': ALL,
            },
            component_property='n_clicks',
        ),
        prevent_initial_call=True,
    )
    def open_alarm_management_modal(_open_clicks):
        if _get_triggered_n_clicks() <= 0:
            raise PreventUpdate

        open_payload = get_alarm_open_payload_from_trigger(
            triggered_id=ctx.triggered_id,
        )

        if open_payload is None:
            raise PreventUpdate

        try:
            result = get_alarm_management_use_case_service().build_context(
                alarm_id=open_payload['alarm_id'],
                alarm_key=open_payload['alarm_key'],
                group_occurrence_id=open_payload['group_occurrence_id'],
                visibility_group_key=open_payload['visibility_group_key'],
                management_scope_key=open_payload['management_scope_key'],
                priority_order=open_payload['priority_order'],
            )

            presentation = AlarmManagementModalPresenter.present_context_result(
                result=result,
            )

            modal_data = _merge_target_occurrence_started_at(
                modal_data=_modal_to_store(modal=presentation.modal),
                target_occurrence_started_at=open_payload.get(
                    'target_occurrence_started_at',
                ),
            )

            return (
                modal_data,
                _feedback_to_store(feedback=presentation.feedback),
                False,
            )

        except Exception as error:
            feedback = AlarmManagementFeedbackViewModel(
                is_open=True,
                kind='error',
                title='Error',
                message=str(error),
            )

            return None, _feedback_to_store(feedback=feedback), False

    @app.callback(
        Output(component_id=ids['modal'], component_property='is_open'),
        Output(component_id=ids['modal_title'], component_property='children'),
        Output(component_id=ids['alarm_title'], component_property='children'),
        Output(component_id=ids['alarm_cause'], component_property='children'),
        Output(component_id=ids['alarm_warning'], component_property='children'),
        Output(component_id=ids['alarm_warning'], component_property='className'),
        Output(component_id=ids['message_dropdown'], component_property='options'),
        Output(component_id=ids['message_dropdown'], component_property='disabled'),
        Output(component_id=ids['message_dropdown'], component_property='value'),
        Output(component_id=ids['personalized_message'], component_property='value'),
        Input(component_id=ids['context_store'], component_property='data'),
        prevent_initial_call=False,
    )
    def render_alarm_management_modal(modal_data):
        if not modal_data:
            return (
                False,
                'Gestión de alarma',
                '',
                '',
                '',
                'd-none',
                [],
                True,
                None,
                '',
            )

        message_options = modal_data.get('message_options') or []

        return (
            bool(modal_data.get('is_open')),
            modal_data.get('modal_title') or 'Gestión de alarma',
            modal_data.get('alarm_title') or '',
            modal_data.get('alarm_cause') or '',
            modal_data.get('warning_message') or '',
            modal_data.get('warning_class_name') or 'd-none',
            message_options,
            not bool(message_options),
            modal_data.get('selected_message_id'),
            modal_data.get('personalized_message') or '',
        )

    @app.callback(
        Output(component_id=ids['silence_container'], component_property='className'),
        Output(component_id=ids['silence_dropdown'], component_property='options'),
        Output(component_id=ids['silence_dropdown'], component_property='disabled'),
        Output(component_id=ids['silence_dropdown'], component_property='value'),
        Output(component_id=ids['silence_information'], component_property='children'),
        Output(component_id=ids['silence_checkbox'], component_property='value'),
        Output(component_id=ids['silence_checkbox'], component_property='disabled'),
        Input(component_id=ids['context_store'], component_property='data'),
        Input(component_id=ids['message_dropdown'], component_property='value'),
        Input(component_id=ids['silence_checkbox'], component_property='value'),
        prevent_initial_call=False,
    )
    def update_silence_controls(
        modal_data,
        selected_message_id,
        silence_requested,
    ):
        if not modal_data:
            return 'd-none', [], True, None, '', False, True

        silence_options = modal_data.get('silence_options') or []
        base_information = modal_data.get('silence_information') or ''

        selected_message = _find_selected_message(
            modal_data=modal_data,
            selected_message_id=selected_message_id,
        )

        manual_silence_allowed = _is_manual_silence_allowed(
            modal_data=modal_data,
        )

        message_policy_code = _get_selected_message_policy_code(
            selected_message=selected_message,
        )

        message_authorizes_silence = _message_authorizes_silence(
            policy_code=message_policy_code,
        )

        if ctx.triggered_id in {
            ids['context_store'],
            ids['message_dropdown'],
        }:
            silence_requested = False

        silence_checkbox_disabled = not silence_options or (
            not manual_silence_allowed and not message_authorizes_silence
        )

        if silence_checkbox_disabled:
            if not silence_options:
                information = 'No existen opciones disponibles para desactivar la alarma.'
            elif not manual_silence_allowed:
                information = (
                    'Esta alarma no permite desactivación libre. '
                    'Selecciona un mensaje predefinido autorizado para desactivarla.'
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
        Output(component_id=ids['message_validation'], component_property='className'),
        Output(component_id=ids['message_validation'], component_property='children'),
        Output(component_id=ids['personalized_message_validation'], component_property='className'),
        Output(component_id=ids['personalized_message_validation'], component_property='children'),
        Output(component_id=ids['silence_validation'], component_property='className'),
        Output(component_id=ids['silence_validation'], component_property='children'),
        Input(component_id=ids['validation_attempt_store'], component_property='data'),
        Input(component_id=ids['message_dropdown'], component_property='value'),
        Input(component_id=ids['personalized_message'], component_property='value'),
        Input(component_id=ids['silence_checkbox'], component_property='value'),
        Input(component_id=ids['silence_dropdown'], component_property='value'),
        State(component_id=ids['context_store'], component_property='data'),
        prevent_initial_call=False,
    )
    def render_form_validation(
        validation_attempted,
        selected_message_id,
        personalized_message,
        silence_requested,
        selected_silence_policy_code,
        modal_data,
    ):
        if not modal_data:
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
        Output(component_id=ids['context_store'], component_property='data', allow_duplicate=True),
        Output(component_id=ids['feedback_store'], component_property='data', allow_duplicate=True),
        Output(
            component_id=ids['validation_attempt_store'],
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=ids['modal_save_button'], component_property='n_clicks'),
        State(component_id=ids['context_store'], component_property='data'),
        State(component_id=ids['message_dropdown'], component_property='value'),
        State(component_id=ids['personalized_message'], component_property='value'),
        State(component_id=ids['silence_checkbox'], component_property='value'),
        State(component_id=ids['silence_dropdown'], component_property='value'),
        running=[
            (
                Output(component_id=ids['modal_save_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['modal_cancel_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['modal_close_button'], component_property='className'),
                'bi bi-x-lg text-muted',
                'bi bi-x-lg active-cursor',
            ),
            (
                Output(component_id=ids['modal_save_button'], component_property='children'),
                build_running_button_children(text='Gestionando'),
                'Gestionar',
            ),
        ],
        prevent_initial_call=True,
    )
    def save_alarm_management(
        n_clicks,
        modal_data,
        selected_message_id,
        personalized_message,
        silence_requested,
        selected_silence_policy_code,
    ):
        if not n_clicks:
            raise PreventUpdate

        if not modal_data:
            feedback = AlarmManagementFeedbackViewModel(
                is_open=True,
                kind='error',
                title='Error',
                message='No existe contexto de gestión para la alarma.',
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

        try:
            refreshed_modal_data = _refresh_modal_data_or_current(
                current_modal_data=modal_data,
                alarm_id=str(modal_data.get('alarm_id') or '').strip(),
                alarm_key=str(modal_data.get('alarm_key') or '').strip(),
            )

            refreshed_modal_data = _merge_form_values(
                modal_data=refreshed_modal_data,
                selected_message_id=selected_message_id,
                personalized_message=personalized_message,
                silence_requested=bool(silence_requested),
                selected_silence_policy_code=selected_silence_policy_code,
            )

            if bool(silence_requested):
                available = _is_silence_policy_available(
                    modal_data=refreshed_modal_data,
                    selected_silence_policy_code=selected_silence_policy_code,
                )

                if not available:
                    refreshed_modal_data = {
                        **refreshed_modal_data,
                        'selected_silence_policy_code': None,
                    }

                    feedback = AlarmManagementFeedbackViewModel(
                        is_open=True,
                        kind='validation_error',
                        title='Validación',
                        message=(
                            'La duración seleccionada ya no está disponible. '
                            'Selecciona una opción válida.'
                        ),
                    )

                    return refreshed_modal_data, _feedback_to_store(feedback=feedback), True

            request = _build_management_request_from_modal_data(
                modal_data=refreshed_modal_data,
                selected_message_id=selected_message_id,
                personalized_message=personalized_message,
                silence_requested=bool(silence_requested),
                selected_silence_policy_code=selected_silence_policy_code,
            )

            result = get_alarm_management_use_case_service().manage_alarm(
                request=request,
                user=_build_user_from_session(),
            )

            feedback = AlarmManagementModalPresenter.present_command_result(
                result=result,
            )

            should_close_modal = result.status in {
                'success',
                'empty',
                'exists',
                'management_disabled',
            }

            next_modal_data = None if should_close_modal else refreshed_modal_data

            return next_modal_data, _feedback_to_store(feedback=feedback), False

        except Exception as error:
            feedback = AlarmManagementFeedbackViewModel(
                is_open=True,
                kind='error',
                title='Error',
                message=str(error),
            )

            return modal_data, _feedback_to_store(feedback=feedback), True

    @app.callback(
        Output(component_id=ids['context_store'], component_property='data', allow_duplicate=True),
        Output(
            component_id=ids['validation_attempt_store'],
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=ids['modal_close_button'], component_property='n_clicks'),
        Input(component_id=ids['modal_cancel_button'], component_property='n_clicks'),
        prevent_initial_call=True,
    )
    def close_alarm_management_modal(
        close_clicks,
        cancel_clicks,
    ):
        if not close_clicks and not cancel_clicks:
            raise PreventUpdate

        return None, False

    @app.callback(
        Output(component_id=ids['feedback_modal'], component_property='is_open'),
        Output(component_id=ids['feedback_title'], component_property='children'),
        Output(component_id=ids['feedback_message'], component_property='children'),
        Input(component_id=ids['feedback_store'], component_property='data'),
        prevent_initial_call=False,
    )
    def render_feedback_modal(feedback_data):
        if not feedback_data:
            return False, 'Información', ''

        return (
            bool(feedback_data.get('is_open')),
            feedback_data.get('title') or 'Información',
            feedback_data.get('message') or '',
        )

    @app.callback(
        Output(component_id=ids['feedback_store'], component_property='data', allow_duplicate=True),
        Input(component_id=ids['feedback_modal_close_button'], component_property='n_clicks'),
        Input(
            component_id=ids['feedback_modal_footer_close_button'], component_property='n_clicks'
        ),
        prevent_initial_call=True,
    )
    def close_feedback_modal(
        close_clicks,
        footer_close_clicks,
    ):
        if not close_clicks and not footer_close_clicks:
            raise PreventUpdate

        return None


def _refresh_modal_data(
    *,
    alarm_id: str,
    alarm_key: str,
    group_occurrence_id: str | None,
    visibility_group_key: str | None,
    management_scope_key: str | None,
    priority_order: int | None,
) -> tuple[dict[str, Any] | None, AlarmManagementFeedbackViewModel | None]:
    result = get_alarm_management_use_case_service().build_context(
        alarm_id=alarm_id,
        alarm_key=alarm_key,
        group_occurrence_id=group_occurrence_id,
        visibility_group_key=visibility_group_key,
        management_scope_key=management_scope_key,
        priority_order=priority_order,
    )

    presentation = AlarmManagementModalPresenter.present_context_result(
        result=result,
    )

    modal_data = _modal_to_store(modal=presentation.modal)
    feedback_data = presentation.feedback

    if modal_data is None and feedback_data.is_open:
        return None, feedback_data

    return modal_data, None


def _refresh_modal_data_or_current(
    *,
    current_modal_data: dict[str, Any],
    alarm_id: str,
    alarm_key: str,
) -> dict[str, Any]:
    try:
        refreshed_modal_data, _refresh_feedback = _refresh_modal_data(
            alarm_id=alarm_id,
            alarm_key=alarm_key,
            group_occurrence_id=str(current_modal_data.get('group_occurrence_id') or '').strip(),
            visibility_group_key=str(current_modal_data.get('visibility_group_key') or '').strip(),
            management_scope_key=str(current_modal_data.get('management_scope_key') or '').strip(),
            priority_order=_optional_int(current_modal_data.get('priority_order')),
        )

        if refreshed_modal_data is not None:
            return _merge_identity_from_current_modal_data(
                refreshed_modal_data=refreshed_modal_data,
                current_modal_data=current_modal_data,
            )

    except Exception:
        pass

    return current_modal_data


def _merge_form_values(
    *,
    modal_data: dict[str, Any] | None,
    selected_message_id: str | None,
    personalized_message: str | None,
    silence_requested: bool,
    selected_silence_policy_code: str | None,
) -> dict[str, Any]:
    if not modal_data:
        return {}

    return {
        **modal_data,
        'selected_message_id': selected_message_id,
        'personalized_message': str(personalized_message or '').strip(),
        'silence_requested': silence_requested,
        'selected_silence_policy_code': selected_silence_policy_code,
    }


def _build_management_request_from_modal_data(
    *,
    modal_data: dict[str, Any],
    selected_message_id: str | None,
    personalized_message: str | None,
    silence_requested: bool,
    selected_silence_policy_code: str | None,
) -> AlarmManagementRequest:
    return AlarmManagementRequest(
        alarm_id=str(modal_data.get('alarm_id') or '').strip(),
        group_occurrence_id=str(modal_data.get('group_occurrence_id') or '').strip(),
        alarm_key=str(modal_data.get('alarm_key') or '').strip(),
        visibility_group_key=str(modal_data.get('visibility_group_key') or '').strip(),
        management_scope_key=str(modal_data.get('management_scope_key') or '').strip(),
        priority_order=_optional_int(modal_data.get('priority_order')),
        target_occurrence_started_at=str(
            modal_data.get('target_occurrence_started_at') or ''
        ).strip(),
        selected_message_id=selected_message_id,
        personalized_message=str(personalized_message or '').strip(),
        silence_requested=silence_requested,
        selected_silence_policy_code=selected_silence_policy_code,
    )


def _is_silence_policy_available(
    *,
    modal_data: dict[str, Any],
    selected_silence_policy_code: str | None,
) -> bool:
    selected_value = str(selected_silence_policy_code or '').strip()

    if not selected_value:
        return False

    if selected_value == 'shift_end':
        return True

    available_values = {
        str(option.get('value') or '').strip()
        for option in modal_data.get('silence_options') or []
        if isinstance(option, dict)
    }

    return selected_value in available_values


def _modal_to_store(
    *,
    modal: AlarmManagementModalViewModel,
) -> dict[str, Any] | None:
    if not modal.is_open or modal.context_data is None:
        return None

    return asdict(modal)


def _feedback_to_store(
    *,
    feedback: AlarmManagementFeedbackViewModel,
) -> dict[str, Any] | None:
    if not feedback.is_open:
        return None

    return asdict(feedback)


def _find_selected_message(
    *,
    modal_data: dict[str, Any],
    selected_message_id: str | None,
) -> dict[str, Any] | None:
    if not selected_message_id:
        return None

    messages_by_id = modal_data.get('messages_by_id') or {}
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
    modal_data: dict[str, Any],
) -> bool:
    context_data = modal_data.get('context_data') or {}

    if not isinstance(context_data, dict):
        return False

    return _to_bool(
        context_data.get('allow_manual_silence'),
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


def _merge_identity_from_current_modal_data(
    *,
    refreshed_modal_data: dict[str, Any],
    current_modal_data: dict[str, Any],
) -> dict[str, Any]:
    identity_keys = (
        'alarm_id',
        'group_occurrence_id',
        'alarm_key',
        'visibility_group_key',
        'management_scope_key',
        'priority_order',
        'operator_bucket',
        'target_occurrence_started_at',
    )

    result = dict(refreshed_modal_data)

    for key in identity_keys:
        refreshed_value = result.get(key)
        current_value = current_modal_data.get(key)

        if refreshed_value not in (None, ''):
            continue

        if current_value in (None, ''):
            continue

        result[key] = current_value

    context_data = result.get('context_data')
    current_context_data = current_modal_data.get('context_data')

    if isinstance(context_data, dict) and isinstance(current_context_data, dict):
        context_data = dict(context_data)

        for key in identity_keys:
            refreshed_value = context_data.get(key)
            current_value = current_context_data.get(key)

            if refreshed_value not in (None, ''):
                continue

            if current_value in (None, ''):
                continue

            context_data[key] = current_value

        result['context_data'] = context_data

    return result


def _merge_target_occurrence_started_at(
    *,
    modal_data: dict[str, Any] | None,
    target_occurrence_started_at: Any,
) -> dict[str, Any] | None:
    if modal_data is None:
        return None

    result = dict(modal_data)

    current_value = str(result.get('target_occurrence_started_at') or '').strip()

    context_data = result.get('context_data')
    context_value = ''

    if isinstance(context_data, dict):
        context_value = str(context_data.get('target_occurrence_started_at') or '').strip()

    fallback_value = str(target_occurrence_started_at or '').strip()

    resolved_value = current_value or context_value or fallback_value

    if not resolved_value:
        return result

    result['target_occurrence_started_at'] = resolved_value

    if isinstance(context_data, dict):
        context_data = dict(context_data)
        context_data['target_occurrence_started_at'] = resolved_value
        result['context_data'] = context_data

    return result
