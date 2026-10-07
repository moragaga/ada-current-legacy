from __future__ import annotations


def register_process_callback() -> None:
    # Hook intencionalmente vacío: el dashboard PRO todavía no tiene callbacks propios.
    return None


__all__ = ['register_process_callback']
