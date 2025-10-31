from __future__ import annotations
from pathlib import Path
from datetime import datetime
from .storage import integration_dir, slugify


def save_generated_code(name: str, language: str, content: str) -> Path:
    d = integration_dir(name)
    ext = {"python": "py", "node": "js"}.get(language, "txt")
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    p = d / f"generated_{ts}.{ext}"
    p.write_text(content, encoding="utf-8")
    return p


def render_python_client(base_url: str, token: str | None = None) -> str:
    template = (Path(__file__).parent.parent / "templates" / "python_client_template.py").read_text(encoding="utf-8")
    return template.replace("{{BASE_URL}}", base_url).replace("{{TOKEN}}", token or "")
