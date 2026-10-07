from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from ..models.alarm_management_request import AlarmManagementRequest
from ..models.alarm_management_result import AlarmManagementResult
from ..models.alarm_management_user import AlarmManagementUser
from .alarm_management_action_builder import AlarmManagementActionBuilder


class AlarmManagementCommandService:
    def __init__(
        self,
        *,
        action_builder: AlarmManagementActionBuilder,
        action_repository,
    ) -> None:
        self._action_builder = action_builder
        self._action_repository = action_repository

    def manage_alarm(
        self,
        *,
        request: AlarmManagementRequest,
        user: AlarmManagementUser,
        runtime_snapshot: dict[str, Any],
        alarm_configuration_rows: list[dict[str, Any]],
        message_configuration: dict[str, Any],
        managed_alarm_ids: set[str],
        shift_end_utc: datetime,
    ) -> AlarmManagementResult:
        now_utc = datetime.now(timezone.utc)

        result = self._action_builder.build_action(
            request=request,
            user=user,
            runtime_snapshot=runtime_snapshot,
            alarm_configuration_rows=alarm_configuration_rows,
            message_configuration=message_configuration,
            managed_alarm_ids=managed_alarm_ids,
            now_utc=now_utc,
            shift_end_utc=shift_end_utc,
        )

        if not result.is_success or result.action is None:
            return result

        saved = self._action_repository.save_action(
            action=result.action,
        )

        if not saved:
            return AlarmManagementResult(
                status='error',
                message='No se pudo guardar la gestión de la alarma.',
            )

        return result
