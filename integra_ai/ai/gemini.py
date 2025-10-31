from __future__ import annotations
import os
import requests
import logging
from typing import Optional
from dotenv import load_dotenv
from ..core.logger import get_logger

load_dotenv()
log = get_logger(__name__)

DEFAULT_MODEL = "gemini-1.5-flash" # Changed from "Generative Language API Key"


def generate_code(prompt: str, api_key: Optional[str] = None, model: str = DEFAULT_MODEL) -> str:
    """Generate code using Google Gemini API (Generative Language API).

    Uses API key via query parameter (?key=) as per REST guidelines.
    """
    key = (api_key or os.getenv("GEMINI_API_KEY") or "").strip()
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set in environment")

    # Determine API version based on the model
    api_version = "v1beta"
    if model == "gemini-pro":
        api_version = "v1"

    url = f"https://generativelanguage.googleapis.com/{api_version}/models/{model}:generateContent"

    headers = {
        "Content-Type": "application/json",
    }
    params = {"key": key}
    body = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    log.info("Calling Gemini generateContent", extra={"model": model})
    resp = requests.post(url, headers=headers, params=params, json=body, timeout=60)
    try:
        resp.raise_for_status()
    except requests.HTTPError:
        log.error("Gemini error", extra={"status": resp.status_code, "text": resp.text[:500]})
        raise

    data = resp.json()
    # Best-effort extraction for v1beta
    text = None
    try:
        cands = data.get("candidates", [])
        if cands:
            parts = cands[0].get("content", {}).get("parts", [])
            for part in parts:
                if "text" in part:
                    text = part["text"]
                    break
    except Exception:  # noqa: BLE001
        pass

    if not text:
        text = str(data)
    return text
