from __future__ import annotations

import os
import platform
import socket
from pathlib import Path


bind = '0.0.0.0:8000'
worker_class = 'gthread'
loglevel = 'info'
timeout = 90
keepalive = 5
errorlog = '-'

_MEMORY_GIB = 1024 * 1024 * 1024
_CGROUP_UNLIMITED_THRESHOLD = 1 << 60


def _read_text(path: str) -> str | None:
    try:
        return Path(path).read_text(encoding='utf-8', errors='replace').strip()
    except Exception:
        return None


def _to_int(value: str | None) -> int | None:
    if value is None:
        return None

    try:
        return int(value.strip())
    except Exception:
        return None


def _read_cgroup_v2_cpu() -> float | None:
    value = _read_text('/sys/fs/cgroup/cpu.max')
    if not value:
        return None

    parts = value.split()
    if not parts or parts[0] == 'max':
        return None

    quota_us = _to_int(parts[0])
    period_us = _to_int(parts[1]) if len(parts) > 1 else None

    if quota_us is None or period_us is None or period_us <= 0:
        return None

    return quota_us / period_us


def _read_cgroup_v1_cpu() -> float | None:
    quota = _to_int(
        _read_text('/sys/fs/cgroup/cpu/cpu.cfs_quota_us')
        or _read_text('/sys/fs/cgroup/cpu,cpuacct/cpu.cfs_quota_us')
    )
    period = _to_int(
        _read_text('/sys/fs/cgroup/cpu/cpu.cfs_period_us')
        or _read_text('/sys/fs/cgroup/cpu,cpuacct/cpu.cfs_period_us')
    )

    if quota is None or period is None or quota <= 0 or period <= 0:
        return None

    return quota / period


def _count_cpuset(value: str | None) -> int | None:
    if not value:
        return None

    total = 0

    for item in value.split(','):
        item = item.strip()
        if not item:
            continue

        if '-' in item:
            start_raw, end_raw = item.split('-', 1)
            start = _to_int(start_raw)
            end = _to_int(end_raw)

            if start is None or end is None:
                continue

            total += max(0, end - start + 1)
            continue

        if _to_int(item) is not None:
            total += 1

    return total or None


def _read_cpuset_cpu() -> int | None:
    return _count_cpuset(
        _read_text('/sys/fs/cgroup/cpuset.cpus.effective')
        or _read_text('/sys/fs/cgroup/cpuset.cpus')
        or _read_text('/sys/fs/cgroup/cpuset/cpuset.cpus')
    )


def _detect_cpu() -> tuple[float, str]:
    cgroup_v2_cpu = _read_cgroup_v2_cpu()
    if cgroup_v2_cpu is not None:
        return max(1.0, cgroup_v2_cpu), 'cgroup_v2_cpu_max'

    cgroup_v1_cpu = _read_cgroup_v1_cpu()
    if cgroup_v1_cpu is not None:
        return max(1.0, cgroup_v1_cpu), 'cgroup_v1_cpu_quota'

    cpuset_cpu = _read_cpuset_cpu()
    if cpuset_cpu is not None:
        return float(max(1, cpuset_cpu)), 'cpuset'

    os_cpu = os.cpu_count()
    if os_cpu is not None:
        return float(max(1, os_cpu)), 'os_cpu_count'

    return 1.0, 'fallback'


def _is_valid_memory_limit(value: int | None) -> bool:
    if value is None:
        return False

    if value <= 0:
        return False

    if value >= _CGROUP_UNLIMITED_THRESHOLD:
        return False

    return True


def _read_cgroup_memory_bytes() -> int | None:
    raw_value = (
        _read_text('/sys/fs/cgroup/memory.max')
        or _read_text('/sys/fs/cgroup/memory/memory.limit_in_bytes')
    )

    if raw_value == 'max':
        return None

    value = _to_int(raw_value)

    if not _is_valid_memory_limit(value):
        return None

    return value


def _read_proc_memtotal_bytes() -> int | None:
    value = _read_text('/proc/meminfo')
    if not value:
        return None

    for line in value.splitlines():
        if not line.startswith('MemTotal:'):
            continue

        parts = line.split()
        if len(parts) < 2:
            return None

        memory_kib = _to_int(parts[1])
        if memory_kib is None:
            return None

        return memory_kib * 1024

    return None


def _detect_memory_bytes() -> tuple[int | None, str]:
    cgroup_memory = _read_cgroup_memory_bytes()
    if cgroup_memory is not None:
        return cgroup_memory, 'cgroup_memory_max'

    proc_memory = _read_proc_memtotal_bytes()
    if proc_memory is not None:
        return proc_memory, 'proc_meminfo'

    return None, 'fallback'


def _resolve_workers_from_memory(memory_bytes: int | None) -> int:
    if memory_bytes is None:
        return 1

    memory_gib = memory_bytes / _MEMORY_GIB

    if memory_gib <= 2.0:
        return 1

    if memory_gib <= 6.0:
        return 2

    return 3


def _resolve_gunicorn_capacity() -> tuple[int, int, dict[str, dict]]:
    effective_cpu, cpu_source = _detect_cpu()
    memory_bytes, memory_source = _detect_memory_bytes()

    resolved_workers = _resolve_workers_from_memory(memory_bytes)

    resolved_workers = min(
        resolved_workers,
        max(1, int(effective_cpu)),
    )

    detected_resources = (
        cpu_source != 'fallback'
        or memory_source != 'fallback'
    )

    resolved_threads = 2 if detected_resources else 1

    diagnostics = {
        'effective_cpu': effective_cpu,
        'cpu_source': cpu_source,
        'memory_bytes': memory_bytes,
        'memory_gib': None if memory_bytes is None else round(memory_bytes / _MEMORY_GIB, 2),
        'memory_source': memory_source,
        'workers': resolved_workers,
        'threads': resolved_threads,
        'detected_resources': detected_resources,
    }

    return resolved_workers, resolved_threads, diagnostics


workers, threads, _diagnostics = _resolve_gunicorn_capacity()


def _print_startup_info() -> None:
    print('[INFO] GUNICORN STARTUP')
    print(f'[INFO] bind={bind}')
    print(f'[INFO] worker_class={worker_class}')
    print(f'[INFO] workers={_diagnostics.get("workers", workers)}')
    print(f'[INFO] threads={_diagnostics.get("threads", threads)}')
    print(f'[INFO] timeout={timeout}')
    print(f'[INFO] keepalive={keepalive}')
    print(f'[INFO] effective_cpu={_diagnostics.get("effective_cpu", "unknown")}')
    print(f'[INFO] cpu_source={_diagnostics.get("cpu_source", "unknown")}')
    print(f'[INFO] memory_gib={_diagnostics.get("memory_gib", "unknown")}')
    print(f'[INFO] memory_source={_diagnostics.get("memory_source", "unknown")}')
    print(f'[INFO] detected_resources={_diagnostics.get("detected_resources", False)}')
    print(f'[INFO] os={platform.system()}')
    print(f'[INFO] os_release={platform.release()}')
    print(f'[INFO] os_version={platform.version()}')
    print(f'[INFO] machine={platform.machine()}')
    print(f'[INFO] hostname={socket.gethostname()}')
    print(f'[INFO] cwd={os.getcwd()}')
    print(f'[INFO] python={platform.python_version()}')


_print_startup_info()