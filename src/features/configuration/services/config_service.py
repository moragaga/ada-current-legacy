from __future__ import annotations

from ..models import AdminSchema
from ..services.config_validation_service import ConfigValidationService


class ConfigService:
    @staticmethod
    def validate_and_normalize(
        schema: AdminSchema,
        rows: list[dict],
    ) -> tuple[list[dict], list[str]]:
        return ConfigValidationService.normalize_rows(schema=schema, rows=rows)
