from __future__ import annotations

from dataclasses import dataclass

from .field_definition import FieldDefinition


@dataclass(frozen=True)
class AdminSchema:
    key: str
    title: str
    fields: tuple[FieldDefinition, ...]
