from __future__ import annotations
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import os
from dotenv import load_dotenv

CONFIG_DIR = Path(".integra")
CONFIG_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = CONFIG_DIR / "config.json"

load_dotenv()


@dataclass
class AppConfig:
    project_name: str = "Integra.AI"
    language: str = "python"  # python | node
    output_dir: str = "integrations"

    @property
    def gemini_api_key(self) -> str | None:
        return os.getenv("GEMINI_API_KEY")

    def save(self) -> None:
        CONFIG_PATH.write_text(json.dumps(asdict(self), indent=2), encoding="utf-8")

    @staticmethod
    def load() -> "AppConfig":
        if CONFIG_PATH.exists():
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return AppConfig(**data)
        cfg = AppConfig()
        cfg.save()
        return cfg
