from __future__ import annotations

from dataclasses import dataclass

ORDER_ONLY_MODE = 'order_only'
CONTENT_MODE = 'content'


@dataclass(slots=True)
class AlarmImagePublicationResult:
    success: bool
    message: str
    mode: str
    trace_id: str | None = None

    @classmethod
    def ok(
        cls,
        *,
        mode: str,
        message: str = 'Cambios publicados correctamente.',
        trace_id: str | None = None,
    ) -> AlarmImagePublicationResult:
        return cls(
            success=True,
            message=message,
            mode=mode,
            trace_id=trace_id,
        )

    @classmethod
    def fail(
        cls,
        *,
        mode: str,
        message: str,
        trace_id: str | None = None,
    ) -> AlarmImagePublicationResult:
        return cls(
            success=False,
            message=message,
            mode=mode,
            trace_id=trace_id,
        )
