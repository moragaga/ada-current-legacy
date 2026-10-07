from __future__ import annotations

from ..models.alarm_management_context_result import AlarmManagementContextResult
from ..models.alarm_management_request import AlarmManagementRequest
from ..models.alarm_management_result import AlarmManagementResult
from ..models.alarm_management_user import AlarmManagementUser
from .alarm_management_command_service import AlarmManagementCommandService
from .alarm_management_context_service import AlarmManagementContextService


class AlarmManagementUseCaseService:
    def __init__(
        self,
        *,
        runtime_input_provider,
        context_service: AlarmManagementContextService,
        command_service: AlarmManagementCommandService,
    ) -> None:
        self._runtime_input_provider = runtime_input_provider
        self._context_service = context_service
        self._command_service = command_service

    def build_context(
        self,
        *,
        alarm_id: str,
        alarm_key: str | None = None,
        group_occurrence_id: str | None = None,
        visibility_group_key: str | None = None,
        management_scope_key: str | None = None,
        priority_order: int | None = None,
    ) -> AlarmManagementContextResult:
        inputs = self._runtime_input_provider.load_inputs()

        return self._context_service.build_context(
            alarm_id=alarm_id,
            alarm_key=alarm_key,
            group_occurrence_id=group_occurrence_id,
            visibility_group_key=visibility_group_key,
            management_scope_key=management_scope_key,
            priority_order=priority_order,
            runtime_snapshot=inputs.runtime_snapshot,
            alarm_configuration_rows=inputs.alarm_configuration_rows,
            message_configuration=inputs.message_configuration,
            managed_alarm_ids=inputs.managed_alarm_ids,
            now_utc=inputs.now_utc,
            shift_end_utc=inputs.shift_end_utc,
        )

    def manage_alarm(
        self,
        *,
        request: AlarmManagementRequest,
        user: AlarmManagementUser,
    ) -> AlarmManagementResult:
        inputs = self._runtime_input_provider.load_inputs()

        return self._command_service.manage_alarm(
            request=request,
            user=user,
            runtime_snapshot=inputs.runtime_snapshot,
            alarm_configuration_rows=inputs.alarm_configuration_rows,
            message_configuration=inputs.message_configuration,
            managed_alarm_ids=inputs.managed_alarm_ids,
            shift_end_utc=inputs.shift_end_utc,
        )
