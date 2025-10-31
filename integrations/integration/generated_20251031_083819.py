"""
Cliente Python gerado por Integra.AI
"""
from __future__ import annotations
import os
import requests

BASE_URL = os.getenv("API_BASE_URL", "https://httpbin.org")
TOKEN = os.getenv("API_TOKEN", "")


def _headers(extra: dict[str, str] | None = None) -> dict[str, str]:
    h = {"Accept": "application/json"}
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    if extra:
        h.update(extra)
    return h


def call_api(path: str, method: str = "GET", params: dict | None = None, json_body: dict | None = None):
    url = BASE_URL.rstrip("/") + "/" + path.lstrip("/")
    func = getattr(requests, method.lower(), requests.get)
    resp = func(url, headers=_headers(), params=params, json=json_body, timeout=30)
    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"API error {resp.status_code}: {resp.text}") from e
    return resp.json() if "application/json" in resp.headers.get("Content-Type", "") else resp.text


if __name__ == "__main__":
    # Exemplo: GET /
    print(call_api("/"))
