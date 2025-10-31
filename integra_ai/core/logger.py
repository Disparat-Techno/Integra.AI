from __future__ import annotations
import logging
from pathlib import Path

_LOG_DIR = Path("logs")
_LOG_DIR.mkdir(parents=True, exist_ok=True)

_formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

_console = logging.StreamHandler()
_console.setFormatter(_formatter)

_file = logging.FileHandler(_LOG_DIR / "integra.log", encoding="utf-8")
_file.setFormatter(_formatter)

logging.basicConfig(level=logging.INFO, handlers=[_console, _file])


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
