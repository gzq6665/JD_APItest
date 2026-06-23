from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """项目运行配置。"""

    base_url: str
    admin_base_url: str
    timeout: int = 15
    verify_ssl: bool = False


def _to_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_settings() -> Settings:
    """读取运行环境配置，默认指向当前项目测试环境。"""

    timeout = int(os.getenv("HTTP_TIMEOUT", "15"))
    verify_ssl = _to_bool(os.getenv("VERIFY_SSL"), default=False)
    return Settings(
        base_url=os.getenv("BASE_URL", "http://your-front-host:8081").rstrip("/"),
        admin_base_url=os.getenv("ADMIN_BASE_URL", "http://your-admin-host:8082").rstrip("/"),
        timeout=timeout,
        verify_ssl=verify_ssl,
    )
