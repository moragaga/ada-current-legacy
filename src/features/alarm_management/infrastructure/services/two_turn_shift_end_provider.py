from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class TwoTurnShiftEndProvider:
    timezone_name: str = 'America/Santiago'
    day_shift_end_hour: int = 19
    night_shift_end_hour: int = 7

    def get_shift_end_utc(
        self,
        *,
        now_utc: datetime,
    ) -> datetime:
        local_timezone = ZoneInfo(self.timezone_name)
        now_local = self._ensure_aware_utc(now_utc).astimezone(local_timezone)

        today = now_local.date()

        night_end = datetime.combine(
            today,
            time(self.night_shift_end_hour, 0),
            tzinfo=local_timezone,
        )

        day_end = datetime.combine(
            today,
            time(self.day_shift_end_hour, 0),
            tzinfo=local_timezone,
        )

        if now_local < night_end:
            shift_end_local = night_end
        elif now_local < day_end:
            shift_end_local = day_end
        else:
            shift_end_local = datetime.combine(
                today + timedelta(days=1),
                time(self.night_shift_end_hour, 0),
                tzinfo=local_timezone,
            )

        return shift_end_local.astimezone(timezone.utc)

    @staticmethod
    def _ensure_aware_utc(value: datetime) -> datetime:
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)
