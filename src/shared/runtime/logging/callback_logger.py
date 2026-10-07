from __future__ import annotations

import traceback
from collections.abc import Callable
from functools import wraps
from typing import Any

from dash import ctx
from dash.exceptions import PreventUpdate

from src.shared.ui.display.error_component import build_error_component


def log_component_callback(
    callback_name: str,
    components: int,
    flags: int,
    *,
    ui_size: str = 'large',
    prevent_update_on_error: bool = True,
) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                triggered_by = ctx.triggered_id
            except Exception as e:
                print(f'[Error] Not triggered callback {e}')
                triggered_by = None

            try:
                result = func(*args, **kwargs)
                return result
            except PreventUpdate as pu:
                raise PreventUpdate from pu
            except Exception as e:
                print(
                    f'[ERROR] callback={callback_name} triggered_by={triggered_by} error={e} prevent'
                )
                traceback.print_exc()

                if components != 0 or flags != 0:
                    return [build_error_component(ui_size=ui_size)] * components + ['true'] * flags

                if prevent_update_on_error:
                    raise PreventUpdate from e

        return wrapper

    return decorator
