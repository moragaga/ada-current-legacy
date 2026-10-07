from __future__ import annotations

from dash import ALL, Input, Output, State, callback, callback_context, ctx
from dash.exceptions import PreventUpdate

from src.app.dash import get_dash_app
from src.shared.ui.status.running_button import build_running_button_children

from .components.admin_status_panel import build_alarm_image_admin_status_panel
from .components.group_list import (
    build_alarm_image_group_list,
    build_group_page_label,
)
from .components.image_panel import build_alarm_image_panel
from .ids import AlarmImageDefinitionIds
from .models.alarm_image_admin_view_model import AlarmImageAdminDraft
from .models.alarm_image_publication import AlarmImagePublicationResult
from .services.alarm_image_admin_application_service import (
    AlarmImageAdminApplicationService,
    build_alarm_image_admin_application_service,
)
from .services.alarm_image_admin_refresh_service import (
    AlarmImageAdminRefreshService,
    build_alarm_image_admin_refresh_service,
)
from .services.alarm_image_admin_state_service import AlarmImageAdminStateService
from .services.alarm_image_admin_status_service import (
    AlarmImageAdminStatus,
    build_alarm_image_admin_status_service,
)
from .services.alarm_image_draft_file_service import AlarmImageDraftFileService
from .services.alarm_image_publication_service import AlarmImagePublicationService


def register_alarm_management_image_admin_callback() -> None:
    app = get_dash_app()

    image_admin_service = build_alarm_image_admin_application_service()
    state_service = AlarmImageAdminStateService()
    draft_file_service = AlarmImageDraftFileService()
    admin_status_service = build_alarm_image_admin_status_service()
    admin_refresh_service = build_alarm_image_admin_refresh_service()

    publication_service = AlarmImagePublicationService(
        publish_order_changes=image_admin_service.publish_order_changes,
        publish_content_changes=image_admin_service.publish_content_changes,
    )

    page_size = 8

    @app.callback(
        Output(
            component_id=AlarmImageDefinitionIds.STORE_DRAFT,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=AlarmImageDefinitionIds.INIT_TRIGGER, component_property='n_intervals'),
        running=[
            (
                Output(
                    component_id=AlarmImageDefinitionIds.REFRESH_BUTTON,
                    component_property='children',
                ),
                build_running_button_children(text='Cargando'),
                'Actualizar',
            ),
        ],
        prevent_initial_call=True,
    )
    def init_draft(n_intervals):
        if n_intervals is None or ctx.triggered_id is None:
            raise PreventUpdate

        return _refresh_draft(
            image_admin_service=image_admin_service,
            state_service=state_service,
            page_size=page_size,
        )

    @app.callback(
        Output(
            component_id=AlarmImageDefinitionIds.STORE_DRAFT,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=AlarmImageDefinitionIds.REFRESH_BUTTON, component_property='n_clicks'),
        running=[
            (
                Output(
                    component_id=AlarmImageDefinitionIds.REFRESH_BUTTON,
                    component_property='children',
                ),
                build_running_button_children(text='Actualizando'),
                'Actualizar',
            ),
            (
                Output(
                    component_id=AlarmImageDefinitionIds.PUBLISH_BUTTON,
                    component_property='disabled',
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=AlarmImageDefinitionIds.MAIN_DEFINITION_SHELL,
                    component_property='className',
                ),
                'alarm-image-definition-shell lock',
                'alarm-image-definition-shell',
            ),
        ],
        prevent_initial_call=True,
    )
    def refresh_draft(n_clicks):
        if n_clicks is None or ctx.triggered_id is None:
            raise PreventUpdate

        return _refresh_draft(
            image_admin_service=image_admin_service,
            state_service=state_service,
            page_size=page_size,
            admin_refresh_service=admin_refresh_service,
        )

    @app.callback(
        Output(
            component_id=AlarmImageDefinitionIds.STORE_DRAFT,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=AlarmImageDefinitionIds.SEARCH_INPUT, component_property='value'),
        Input(
            component_id=AlarmImageDefinitionIds.GROUP_PREVIOUS_PAGE, component_property='n_clicks'
        ),
        Input(component_id=AlarmImageDefinitionIds.GROUP_NEXT_PAGE, component_property='n_clicks'),
        State(component_id=AlarmImageDefinitionIds.STORE_DRAFT, component_property='data'),
        prevent_initial_call=True,
    )
    def change_state_draft(search_value, _previous_clicks, _next_clicks, draft_data):
        triggered_id = ctx.triggered_id
        if triggered_id is None:
            raise PreventUpdate

        draft = AlarmImageAdminDraft.from_dict(draft_data)
        # RESET KEY TO CHANGE
        draft.selected_message_group_key = ''
        if draft.ui_state == 'processing':
            raise PreventUpdate

        if triggered_id == AlarmImageDefinitionIds.SEARCH_INPUT:
            draft = state_service.update_search(
                draft=draft,
                search_text=search_value or '',
            )
            return draft.to_dict()

        if triggered_id == AlarmImageDefinitionIds.GROUP_PREVIOUS_PAGE:
            draft = state_service.go_previous_page(draft)
            return draft.to_dict()

        if triggered_id == AlarmImageDefinitionIds.GROUP_NEXT_PAGE:
            draft = state_service.go_next_page(draft)
            return draft.to_dict()

        raise PreventUpdate

    @app.callback(
        Output(
            component_id=AlarmImageDefinitionIds.STORE_DRAFT,
            component_property='data',
            allow_duplicate=True,
        ),
        Input(component_id=AlarmImageDefinitionIds.PUBLISH_BUTTON, component_property='n_clicks'),
        State(component_id=AlarmImageDefinitionIds.STORE_DRAFT, component_property='data'),
        running=[
            (
                Output(
                    component_id=AlarmImageDefinitionIds.PUBLISH_BUTTON,
                    component_property='children',
                ),
                build_running_button_children(text='Publicando'),
                'Guardar / Publicar cambios',
            ),
            (
                Output(
                    component_id=AlarmImageDefinitionIds.REFRESH_BUTTON,
                    component_property='disabled',
                ),
                True,
                False,
            ),
            (
                Output(
                    component_id=AlarmImageDefinitionIds.MAIN_DEFINITION_SHELL,
                    component_property='className',
                ),
                'alarm-image-definition-shell lock',
                'alarm-image-definition-shell',
            ),
        ],
        prevent_initial_call=True,
    )
    def publish_draft(n_clicks, draft_data):
        if n_clicks is None or ctx.triggered_id is None:
            raise PreventUpdate

        draft = AlarmImageAdminDraft.from_dict(draft_data)

        return _publish_draft(
            draft=draft,
            image_admin_service=image_admin_service,
            publication_service=publication_service,
            state_service=state_service,
            page_size=page_size,
        ).to_dict()

    @app.callback(
        Output(component_id=AlarmImageDefinitionIds.STORE_DRAFT, component_property='data'),
        Input(
            component_id={
                'type': AlarmImageDefinitionIds.GROUP_CARD,
                'message_group_key': ALL,
            },
            component_property='n_clicks',
        ),
        Input(
            component_id={
                'type': AlarmImageDefinitionIds.ADD_IMAGE_UPLOAD,
                'message_group_key': ALL,
            },
            component_property='contents',
        ),
        Input(
            component_id={
                'type': AlarmImageDefinitionIds.IMAGE_MOVE_UP,
                'message_group_key': ALL,
                'image_key': ALL,
            },
            component_property='n_clicks',
        ),
        Input(
            component_id={
                'type': AlarmImageDefinitionIds.IMAGE_MOVE_DOWN,
                'message_group_key': ALL,
                'image_key': ALL,
            },
            component_property='n_clicks',
        ),
        Input(
            component_id={
                'type': AlarmImageDefinitionIds.IMAGE_DELETE,
                'message_group_key': ALL,
                'image_key': ALL,
            },
            component_property='n_clicks',
        ),
        Input(
            component_id={
                'type': AlarmImageDefinitionIds.IMAGE_REPLACE_UPLOAD,
                'message_group_key': ALL,
                'image_key': ALL,
            },
            component_property='contents',
        ),
        State(
            component_id={
                'type': AlarmImageDefinitionIds.ADD_IMAGE_UPLOAD,
                'message_group_key': ALL,
            },
            component_property='filename',
        ),
        State(
            component_id={
                'type': AlarmImageDefinitionIds.ADD_IMAGE_UPLOAD,
                'message_group_key': ALL,
            },
            component_property='id',
        ),
        State(
            component_id={
                'type': AlarmImageDefinitionIds.IMAGE_REPLACE_UPLOAD,
                'message_group_key': ALL,
                'image_key': ALL,
            },
            component_property='filename',
        ),
        State(
            component_id={
                'type': AlarmImageDefinitionIds.IMAGE_REPLACE_UPLOAD,
                'message_group_key': ALL,
                'image_key': ALL,
            },
            component_property='id',
        ),
        State(component_id=AlarmImageDefinitionIds.STORE_DRAFT, component_property='data'),
        prevent_initial_call=False,
    )
    def update_draft(
        _group_clicks,
        add_image_contents,
        _move_up_clicks,
        _move_down_clicks,
        _delete_clicks,
        replace_image_contents,
        add_image_filenames,
        add_image_ids,
        replace_image_filenames,
        replace_image_ids,
        draft_data,
    ):
        triggered_id = callback_context.triggered_id

        if triggered_id is None:
            raise PreventUpdate

        draft = AlarmImageAdminDraft.from_dict(draft_data)

        if isinstance(triggered_id, dict):
            triggered_id_dict = dict(triggered_id)
            trigger_type = triggered_id_dict.get('type')
            message_group_key = triggered_id_dict.get('message_group_key')
            image_key = triggered_id_dict.get('image_key')

            if trigger_type == AlarmImageDefinitionIds.GROUP_CARD and message_group_key:
                draft = state_service.select_group(
                    draft=draft,
                    message_group_key=message_group_key,
                )
                return draft.to_dict()

            if trigger_type == AlarmImageDefinitionIds.ADD_IMAGE_UPLOAD and message_group_key:
                contents, filename = _get_triggered_upload(
                    triggered_id=triggered_id_dict,
                    contents_list=add_image_contents or [],
                    filenames_list=add_image_filenames or [],
                    ids_list=add_image_ids or [],
                )

                if not contents or not filename:
                    raise PreventUpdate

                new_image_key = _build_new_image_key()

                saved_image = draft_file_service.save_uploaded_image(
                    contents=contents,
                    filename=filename,
                    draft_id=draft.draft_id,
                    message_group_key=message_group_key,
                    image_key=new_image_key,
                )

                draft = state_service.add_image(
                    draft=draft,
                    message_group_key=message_group_key,
                    image_key=new_image_key,
                    thumb_url=saved_image.asset_url,
                    full_url=saved_image.asset_url,
                    mime_type=saved_image.mime_type,
                    content_hash=saved_image.content_hash,
                    source_filename=saved_image.source_filename,
                    draft_file_path=saved_image.file_path,
                )
                return draft.to_dict()

            if (
                trigger_type == AlarmImageDefinitionIds.IMAGE_MOVE_UP
                and message_group_key
                and image_key
            ):
                draft = state_service.move_image_up(
                    draft=draft,
                    message_group_key=message_group_key,
                    image_key=image_key,
                )
                return draft.to_dict()

            if (
                trigger_type == AlarmImageDefinitionIds.IMAGE_MOVE_DOWN
                and message_group_key
                and image_key
            ):
                draft = state_service.move_image_down(
                    draft=draft,
                    message_group_key=message_group_key,
                    image_key=image_key,
                )
                return draft.to_dict()

            if (
                trigger_type == AlarmImageDefinitionIds.IMAGE_DELETE
                and message_group_key
                and image_key
            ):
                draft = state_service.delete_image(
                    draft=draft,
                    message_group_key=message_group_key,
                    image_key=image_key,
                )
                return draft.to_dict()

            if (
                trigger_type == AlarmImageDefinitionIds.IMAGE_REPLACE_UPLOAD
                and message_group_key
                and image_key
            ):
                contents, filename = _get_triggered_upload(
                    triggered_id=triggered_id_dict,
                    contents_list=replace_image_contents or [],
                    filenames_list=replace_image_filenames or [],
                    ids_list=replace_image_ids or [],
                )

                if not contents or not filename:
                    raise PreventUpdate

                saved_image = draft_file_service.save_uploaded_image(
                    contents=contents,
                    filename=filename,
                    draft_id=draft.draft_id,
                    message_group_key=message_group_key,
                    image_key=image_key,
                )

                draft = state_service.replace_image(
                    draft=draft,
                    message_group_key=message_group_key,
                    image_key=image_key,
                    thumb_url=saved_image.asset_url,
                    full_url=saved_image.asset_url,
                    mime_type=saved_image.mime_type,
                    content_hash=saved_image.content_hash,
                    source_filename=saved_image.source_filename,
                    draft_file_path=saved_image.file_path,
                )
                return draft.to_dict()

        raise PreventUpdate

    @callback(
        # Output(AlarmImageDefinitionIds.STATUS_BANNER, 'children'),
        Output(component_id=AlarmImageDefinitionIds.MAIN_LOADER, component_property='display'),
        Output(component_id=AlarmImageDefinitionIds.MONITOR, component_property='children'),
        Output(component_id=AlarmImageDefinitionIds.GROUP_LIST, component_property='children'),
        Output(
            component_id=AlarmImageDefinitionIds.GROUP_PAGE_LABEL, component_property='children'
        ),
        Output(component_id=AlarmImageDefinitionIds.IMAGE_PANEL, component_property='children'),
        Output(component_id=AlarmImageDefinitionIds.PUBLISH_BUTTON, component_property='disabled'),
        Output(
            component_id=AlarmImageDefinitionIds.GROUP_PREVIOUS_PAGE, component_property='disabled'
        ),
        Output(component_id=AlarmImageDefinitionIds.GROUP_NEXT_PAGE, component_property='disabled'),
        Input(component_id=AlarmImageDefinitionIds.STORE_DRAFT, component_property='data'),
    )
    def render_panel(draft_data):
        status = _build_admin_status_safely(admin_status_service)

        if not draft_data:
            draft = AlarmImageAdminDraft(
                groups=[],
                ui_state='error',
                error_message='No se pudo inicializar el panel de imágenes.',
            )

            prev_page, next_page = _validate_pagination(draft=draft, state_service=state_service)

            return (
                'hide',
                build_alarm_image_admin_status_panel(status=status, draft=draft),
                build_alarm_image_group_list(
                    draft=draft,
                    state_service=state_service,
                ),
                build_group_page_label(
                    draft=draft,
                    state_service=state_service,
                ),
                build_alarm_image_panel(draft),
                True,
                prev_page,
                next_page,
            )

        draft = AlarmImageAdminDraft.from_dict(draft_data)

        publish_disabled = (
            not draft.change_summary.has_changes
            or draft.ui_state == 'processing'
            or draft.ui_state == 'error'
        )

        prev_page, next_page = _validate_pagination(draft=draft, state_service=state_service)

        return (
            'hide',
            build_alarm_image_admin_status_panel(status=status, draft=draft),
            build_alarm_image_group_list(
                draft=draft,
                state_service=state_service,
            ),
            build_group_page_label(
                draft=draft,
                state_service=state_service,
            ),
            build_alarm_image_panel(draft),
            publish_disabled,
            prev_page,
            next_page,
        )


def _build_initial_draft_safely(
    *,
    image_admin_service,
    state_service: AlarmImageAdminStateService,
    page_size: int,
) -> AlarmImageAdminDraft:
    try:
        return state_service.build_initial_draft(
            message_groups=image_admin_service.load_message_groups(),
            published_images=image_admin_service.load_published_images(),
            page_size=page_size,
        )
    except Exception as exc:
        return AlarmImageAdminDraft(
            groups=[],
            ui_state='error',
            error_message=(
                f'No se pudo cargar alarm_configuration o imágenes publicadas. Detalle: {exc}'
            ),
            page_size=page_size,
        )


def _publish_draft(
    *,
    draft: AlarmImageAdminDraft,
    image_admin_service,
    publication_service: AlarmImagePublicationService,
    state_service: AlarmImageAdminStateService,
    page_size: int,
) -> AlarmImageAdminDraft:
    draft.ui_state = 'processing'
    draft.error_message = None

    result = publication_service.publish(draft)

    if not result.success:
        draft.ui_state = 'error'
        draft.error_message = _format_publication_error(result)
        return draft

    refreshed_draft = _build_initial_draft_safely(
        image_admin_service=image_admin_service,
        state_service=state_service,
        page_size=page_size,
    )
    refreshed_draft.ui_state = 'success'
    refreshed_draft.error_message = result.message
    return refreshed_draft


def _format_publication_error(result: AlarmImagePublicationResult) -> str:
    if result.trace_id:
        return f'{result.message} Trace ID: {result.trace_id}'

    return result.message


def _build_admin_status_safely(admin_status_service) -> AlarmImageAdminStatus:
    try:
        return admin_status_service.get_status()
    except Exception:
        return AlarmImageAdminStatus(
            bundle_count=0,
            ready_count=0,
            failed_count=0,
            pending_count=0,
            total_size_bytes=0,
            last_published_at=None,
            last_published_by=None,
            last_published_by_email=None,
            last_runtime_check_at=None,
            next_runtime_check_at=None,
            last_runtime_success_at=None,
            last_runtime_failure_at=None,
            last_runtime_error='No se pudo cargar el estado de publicación/runtime.',
        )


def _build_new_image_key() -> str:
    from uuid import uuid4

    return f'img_{uuid4().hex}'


def _get_triggered_upload(
    *,
    triggered_id: dict,
    contents_list: list[str | None],
    filenames_list: list[str | None],
    ids_list: list[dict | None],
) -> tuple[str | None, str | None]:
    for contents, filename, upload_id in zip(contents_list, filenames_list, ids_list, strict=False):
        if not upload_id:
            continue

        if dict(upload_id) == triggered_id:
            return contents, filename

    return None, None


def _refresh_draft(
    image_admin_service: AlarmImageAdminApplicationService,
    state_service: AlarmImageAdminStateService,
    page_size: int,
    admin_refresh_service: AlarmImageAdminRefreshService = None,
) -> dict:
    if admin_refresh_service is not None:
        admin_refresh_service.refresh_runtime_if_due()

    draft = _build_initial_draft_safely(
        image_admin_service=image_admin_service,
        state_service=state_service,
        page_size=page_size,
    )
    draft.selected_message_group_key = ''
    return draft.to_dict()


def _validate_pagination(draft: AlarmImageAdminDraft, state_service: AlarmImageAdminStateService):
    if not draft.groups:
        return True, True

    total_pages = state_service.get_total_pages(draft=draft)
    if draft.current_page == 1 and total_pages == 1:
        return True, True
    elif draft.current_page == total_pages:
        return False, True
    elif draft.current_page == 1 and total_pages > 1:
        return True, False
    else:
        return False, False
