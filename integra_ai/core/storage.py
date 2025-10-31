from __future__ import annotations
from pathlib import Path
import json
from typing import Any

ROOT = Path.cwd()
INTEGRATIONS_DIR = ROOT / "integrations"
INTEGRATIONS_DIR.mkdir(parents=True, exist_ok=True)


def slugify(name: str) -> str:
    s = "".join(c.lower() if c.isalnum() else "-" for c in name).strip("-")
    while "--" in s:
        s = s.replace("--", "-")
    return s or "integration"


def integration_dir(name: str) -> Path:
    d = INTEGRATIONS_DIR / slugify(name)
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_integration_metadata(name: str, meta: dict[str, Any]) -> Path:
    d = integration_dir(name)
    p = d / "integration.json"
    p.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return p


def load_integration_metadata(name: str) -> dict[str, Any]:
    p = integration_dir(name) / "integration.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def list_integrations() -> list[str]:
    if not INTEGRATIONS_DIR.exists():
        return []
    return sorted([p.name for p in INTEGRATIONS_DIR.iterdir() if p.is_dir()])
