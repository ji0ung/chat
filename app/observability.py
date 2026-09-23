from __future__ import annotations

import contextvars
import hashlib
import json
import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from app.config import Settings

request_id_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default="-"
)


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "event": getattr(record, "event", record.getMessage()),
            "request_id": getattr(record, "request_id", request_id_var.get()),
        }
        fields = getattr(record, "fields", None)
        if fields:
            payload.update(fields)
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def configure_logging(settings: Settings) -> logging.Logger:
    logger = logging.getLogger("character_memory")
    logger.setLevel(settings.log_level)
    logger.propagate = False
    if logger.handlers:
        return logger

    path = Path(settings.log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    formatter = JsonFormatter()

    file_handler = RotatingFileHandler(
        path,
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger


def log_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    logger.info(event, extra={"event": event, "fields": fields})


class PrivacyFilter:
    def __init__(self, settings: Settings) -> None:
        self.include_content = settings.log_include_content
        self.salt = settings.log_hash_salt

    def hash_identifier(self, value: str) -> str:
        digest = hashlib.sha256(f"{self.salt}:{value}".encode()).hexdigest()
        return digest[:16]

    def text_fields(self, text: str, name: str = "message") -> dict[str, Any]:
        fields: dict[str, Any] = {
            f"{name}_length": len(text),
            f"{name}_sha256": hashlib.sha256(text.encode()).hexdigest()[:16],
        }
        if self.include_content:
            fields[f"{name}_content"] = text
        return fields
