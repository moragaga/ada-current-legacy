from __future__ import annotations

from typing import Any

# Paleta de colores estándar
# COLOR_RED = '#b02a37'      # 0: Alerta / Rojo
COLOR_RED = '#d93829' 
COLOR_YELLOW = '#eab308'   # 1: Advertencia / Amarillo
COLOR_DEFAULT = None       # 2: Sin pintar / Normal


def extract_status_code(status: Any) -> int | None:
    """Extrae el código numérico de estado (0, 1, 2) desde int, float, str o dict."""
    if status is None:
        return None

    # Si viene como objeto/diccionario ej: {"value": "0", "status": "ok", ...}
    if isinstance(status, dict):
        raw = status.get('value')
        if raw is None or str(raw).strip().lower() in ('', 'nan', 'none', 'null'):
            raw = status.get('parsed_value')
        status = raw

    if status is None:
        return None

    val_str = str(status).strip()
    if val_str in ('', '-', '--', 'nan', 'NaN', 'None', 'null'):
        return None

    try:
        return int(float(val_str.replace(',', '.')))
    except (ValueError, TypeError):
        return None


def get_status_color(status: Any) -> str | None:
    """Retorna el color según el código recibido:

    - 0 -> '#b02a37' (Rojo)
    - 1 -> '#eab308' (Amarillo)
    - 2 -> None (Sin pintar / color base)
    """
    code = extract_status_code(status)
    if code == 0:
        return COLOR_RED
    if code == 1:
        return COLOR_YELLOW
    return COLOR_DEFAULT