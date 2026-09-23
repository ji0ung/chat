from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _parse_access_tokens(raw: str) -> dict[str, str]:
    """Parse MVP_ACCESS_TOKENS as token:user_id pairs separated by commas."""
    result: dict[str, str] = {}
    for item in raw.split(","):
        item = item.strip()
        if not item or ":" not in item:
            continue
        token, user_id = item.split(":", 1)
        token, user_id = token.strip(), user_id.strip()
        if token and user_id:
            result[token] = user_id
    return result


@dataclass(frozen=True)
class Settings:
    app_env: str = os.getenv("APP_ENV", "development").lower()
    chat_model: str = os.getenv("CHAT_MODEL", "gpt-4.1-mini")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai").lower()
    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    ollama_chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:3b")
    ollama_embedding_model: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    local_embedding_model: str = os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    hash_embedding_dimensions: int = int(os.getenv("HASH_EMBEDDING_DIMENSIONS", "384"))
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openrouter/free")
    db_path: str = os.getenv("MEMORY_DB_PATH", "data/memories.db")
    top_k: int = int(os.getenv("MEMORY_TOP_K", "5"))
    candidate_limit: int = int(os.getenv("MEMORY_CANDIDATE_LIMIT", "20"))
    half_life_days: float = float(os.getenv("MEMORY_HALF_LIFE_DAYS", "30"))

    access_tokens: dict[str, str] = None  # type: ignore[assignment]
    admin_api_token: str | None = os.getenv("ADMIN_API_TOKEN")
    rate_limit_per_minute: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "20"))
    ip_rate_limit_per_minute: int = int(os.getenv("IP_RATE_LIMIT_PER_MINUTE", "60"))
    message_max_chars: int = int(os.getenv("MESSAGE_MAX_CHARS", "4000"))
    message_max_same_char_run: int = int(os.getenv("MESSAGE_MAX_SAME_CHAR_RUN", "100"))
    message_max_urls: int = int(os.getenv("MESSAGE_MAX_URLS", "10"))
    replacement_char_ratio: float = float(os.getenv("REPLACEMENT_CHAR_RATIO", "0.20"))
    idempotency_ttl_seconds: int = int(os.getenv("IDEMPOTENCY_TTL_SECONDS", "300"))

    allowed_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv(
            "ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000"
        ).split(",")
        if origin.strip()
    )
    log_level: str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_path: str = os.getenv("LOG_PATH", "logs/character-memory.jsonl")
    log_max_bytes: int = int(os.getenv("LOG_MAX_BYTES", "10485760"))
    log_backup_count: int = int(os.getenv("LOG_BACKUP_COUNT", "7"))
    log_include_content: bool = os.getenv("LOG_INCLUDE_CONTENT", "false").lower() == "true"
    log_hash_salt: str | None = os.getenv("LOG_HASH_SALT")

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "access_tokens",
            _parse_access_tokens(os.getenv("MVP_ACCESS_TOKENS", "")),
        )
        if not self.log_hash_salt:
            seed = self.admin_api_token or "development-admin-token"
            derived = hashlib.sha256(f"luna-log-salt:{seed}".encode()).hexdigest()
            object.__setattr__(self, "log_hash_salt", derived)

        if self.app_env == "production":
            problems: list[str] = []
            if not self.access_tokens:
                problems.append("MVP_ACCESS_TOKENS must contain at least one token:user_id pair")
            if not self.admin_api_token or len(self.admin_api_token) < 16:
                problems.append("ADMIN_API_TOKEN must be set and at least 16 characters")
            if not self.allowed_origins or "*" in self.allowed_origins:
                problems.append("ALLOWED_ORIGINS must list explicit frontend origins")
            if self.log_include_content:
                problems.append("LOG_INCLUDE_CONTENT must be false in production")
            if problems:
                raise RuntimeError("Unsafe production configuration: " + "; ".join(problems))
