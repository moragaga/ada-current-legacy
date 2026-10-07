from __future__ import annotations

from dash import Input, Output, State, ctx, no_update
from flask import session

from src.app.dash import get_dash_app
from src.app.dependencies import get_alarm_message_admin_service
from src.features.admin_framework.services import AdminFeedbackService, AdminGridService
from src.shared.ui.status.running_button import build_running_button_children

from .ids import build_alarm_management_message_admin_ids
from .services.alarm_message_bucket_service import AlarmMessageBucketService
from .services.alarm_message_row_factory_service import AlarmMessageRowFactoryService


def register_alarm_management_message_admin_callback() -> None:
    app = get_dash_app()
    ids = build_alarm_management_message_admin_ids()

    @app.callback(
        Output(component_id=ids['snapshot'], component_property='data'),
        Output(component_id=ids['bucket_selector'], component_property='options'),
        Output(component_id=ids['bucket_selector'], component_property='value'),
        Input(component_id=ids['init'], component_property='data'),
        Input(component_id=ids['reload_button'], component_property='n_clicks'),
        State(component_id=ids['bucket_selector'], component_property='value'),
        running=[
            (Output(component_id=ids['reload_button'], component_property='disabled'), True, False),
            (
                Output(component_id=ids['reload_button'], component_property='children'),
                build_running_button_children(text='Recargando'),
                'Recargar',
            ),
            (
                Output(component_id=ids['delete_rows_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['add_row_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['bucket_selector'], component_property='disabled'),
                True,
                False,
            ),
            (Output(component_id=ids['save_button'], component_property='disabled'), True, False),
            (Output(component_id=ids['loading'], component_property='display'), 'show', 'auto'),
        ],
        prevent_initial_call=False,
    )
    def load_snapshot(
        _init_data,
        _reload_clicks,
        current_bucket,
    ):
        service = get_alarm_message_admin_service()
        snapshot = service.build_snapshot()

        options = snapshot['bucket_options']
        option_values = {option['value'] for option in options}

        selected_bucket = current_bucket

        if selected_bucket not in option_values:
            selected_bucket = options[0]['value'] if options else None

        return snapshot, options, selected_bucket

    @app.callback(
        Output(component_id=ids['grid'], component_property='rowData'),
        Output(component_id=ids['grid'], component_property='selectedRows'),
        Input(component_id=ids['snapshot'], component_property='data'),
        Input(component_id=ids['bucket_selector'], component_property='value'),
        prevent_initial_call=False,
    )
    def render_bucket_rows(
        snapshot,
        selected_bucket,
    ):
        if not snapshot or not selected_bucket:
            return [], []

        message_configuration = snapshot.get('message_configuration') or {}

        rows = AlarmMessageBucketService.get_rows_for_bucket(
            selected_bucket=selected_bucket,
            message_configuration=message_configuration,
        )

        prepared_rows = AdminGridService.prepare_rows_for_grid(
            rows=rows,
        )

        return prepared_rows, []

    @app.callback(
        Output(component_id=ids['grid'], component_property='rowData', allow_duplicate=True),
        Output(component_id=ids['grid'], component_property='selectedRows', allow_duplicate=True),
        Input(component_id=ids['add_row_button'], component_property='n_clicks'),
        State(component_id=ids['grid'], component_property='rowData'),
        prevent_initial_call=True,
    )
    def add_row(
        n_clicks,
        current_rows,
    ):
        if not n_clicks:
            return no_update, no_update

        current_rows = list(current_rows or [])

        new_row = AlarmMessageRowFactoryService.build_new_row(
            current_rows=current_rows,
        )

        updated_rows = AdminGridService.append_row(
            rows=current_rows,
            row=new_row,
        )

        return updated_rows, []

    @app.callback(
        Output(component_id=ids['grid'], component_property='rowData', allow_duplicate=True),
        Output(component_id=ids['grid'], component_property='selectedRows', allow_duplicate=True),
        Input(component_id=ids['delete_rows_button'], component_property='n_clicks'),
        State(component_id=ids['grid'], component_property='rowData'),
        State(component_id=ids['grid'], component_property='selectedRows'),
        prevent_initial_call=True,
    )
    def delete_selected_rows(
        n_clicks,
        current_rows,
        selected_rows,
    ):
        if not n_clicks:
            return no_update, no_update

        updated_rows = AdminGridService.delete_selected_rows(
            rows=current_rows or [],
            selected_rows=selected_rows or [],
        )

        return updated_rows, []

    @app.callback(
        Output(component_id=ids['snapshot'], component_property='data', allow_duplicate=True),
        Output(component_id=ids['grid'], component_property='rowData', allow_duplicate=True),
        Output(component_id=ids['grid'], component_property='selectedRows', allow_duplicate=True),
        Output(component_id=ids['toast_host'], component_property='children'),
        Input(component_id=ids['save_button'], component_property='n_clicks'),
        State(component_id=ids['bucket_selector'], component_property='value'),
        State(component_id=ids['grid'], component_property='rowData'),
        running=[
            (Output(component_id=ids['save_button'], component_property='disabled'), True, False),
            (
                Output(component_id=ids['save_button'], component_property='children'),
                build_running_button_children(text='Guardando'),
                'Guardar',
            ),
            (
                Output(component_id=ids['delete_rows_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['add_row_button'], component_property='disabled'),
                True,
                False,
            ),
            (
                Output(component_id=ids['bucket_selector'], component_property='disabled'),
                True,
                False,
            ),
            (Output(component_id=ids['reload_button'], component_property='disabled'), True, False),
        ],
        prevent_initial_call=True,
    )
    def save_bucket(
        n_clicks,
        selected_bucket,
        current_rows,
    ):
        if not n_clicks or ctx.triggered_id is None:
            return no_update, no_update, no_update, no_update, no_update, no_update

        if not selected_bucket:
            return (
                no_update,
                no_update,
                [],
                AdminFeedbackService.build_warning('Seleccione un grupo de mensajes'),
            )

        updated_by = (session.get('identity') or {}).get('email')
        service = get_alarm_message_admin_service()

        clean_rows = AdminGridService.clean_rows_for_save(
            rows=current_rows or [],
        )

        ok, errors, _updated_configuration = service.save_bucket(
            selected_bucket=selected_bucket,
            rows=clean_rows,
            updated_by=updated_by,
        )

        snapshot = service.build_snapshot()

        message_configuration = snapshot.get('message_configuration') or {}
        rows = AlarmMessageBucketService.get_rows_for_bucket(
            selected_bucket=selected_bucket,
            message_configuration=message_configuration,
        )

        prepared_rows = AdminGridService.prepare_rows_for_grid(
            rows=rows,
        )

        if not ok:
            return (
                snapshot,
                prepared_rows,
                [],
                AdminFeedbackService.build_error(_format_errors(errors)),
            )

        return (
            snapshot,
            prepared_rows,
            [],
            AdminFeedbackService.build_success('Mensajes de gestión guardados correctamente'),
        )


def _format_errors(errors: list[str]) -> list[str] | str:
    if not errors:
        return 'Ocurrió un error inesperado.'

    if len(errors) == 1:
        return errors[0]

    return errors
