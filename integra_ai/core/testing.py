from __future__ import annotations
import requests
from typing import Any


def simple_request_test(base_url: str, endpoint: str, method: str = "GET", headers: dict[str, str] | None = None, payload: Any = None) -> tuple[int, str]:
    url = base_url.rstrip("/") + "/" + endpoint.lstrip("/")
    m = method.upper()
    func = getattr(requests, m.lower(), requests.get)
    resp = func(url, headers=headers or {}, json=payload, timeout=30)
    return resp.status_code, resp.text
