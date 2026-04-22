from __future__ import annotations

from typing import Any

import requests
from requests import Response
from requests.sessions import Session


class ApiClient:
    """对 requests.Session 的轻量封装，统一处理基础地址、Cookie 和超时。"""

    def __init__(self, base_url: str, timeout: int = 15, verify: bool = False) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.verify = verify
        self.session: Session = requests.Session()

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        multipart: dict[str, Any] | None = None,
    ) -> Response:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        final_headers = dict(headers or {})
        request_kwargs: dict[str, Any] = {
            "method": method.upper(),
            "url": url,
            "params": params,
            "data": data,
            "json": json,
            "headers": final_headers,
            "timeout": self.timeout,
            "verify": self.verify,
        }

        if multipart is not None:
            final_headers.pop("Content-Type", None)
            request_kwargs["files"] = [
                (key, (None, "" if value is None else str(value))) for key, value in multipart.items()
            ]

        return self.session.request(**request_kwargs)

    def close(self) -> None:
        """关闭底层会话。"""

        self.session.close()
