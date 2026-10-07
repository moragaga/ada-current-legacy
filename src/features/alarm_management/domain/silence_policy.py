from __future__ import annotations

SILENCE_POLICY_INHERIT = 'inherit'
SILENCE_POLICY_NONE = 'none'
SILENCE_POLICY_SHIFT_END = 'shift_end'

SILENCE_POLICY_HOUR_CODES = tuple(f'h{hour:02d}' for hour in range(1, 12))

SILENCE_POLICY_CODES = (
    SILENCE_POLICY_INHERIT,
    SILENCE_POLICY_NONE,
    *SILENCE_POLICY_HOUR_CODES,
    SILENCE_POLICY_SHIFT_END,
)


def is_valid_silence_policy_code(value: str | None) -> bool:
    return normalize_silence_policy_code(value) in SILENCE_POLICY_CODES


def normalize_silence_policy_code(value: str | None) -> str:
    if value is None:
        return SILENCE_POLICY_INHERIT

    normalized = str(value).strip().lower()

    if not normalized:
        return SILENCE_POLICY_INHERIT

    return normalized
