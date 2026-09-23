from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    chat_model: str = os.getenv("CHAT_MODEL", "gpt-4.1-mini")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    llm_provider: str = os.getenv("LLM_PROVIDER", "openai").lower()
    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "openai").lower()
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    ollama_chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "qwen2.5:3b")
    ollama_embedding_model: str = os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text")
    local_embedding_model: str = os.getenv("LOCAL_EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv("OPENROUTER_MODEL", "openrouter/free")
    db_path: str = os.getenv("MEMORY_DB_PATH", "data/memories.db")
    top_k: int = int(os.getenv("MEMORY_TOP_K", "5"))
    candidate_limit: int = int(os.getenv("MEMORY_CANDIDATE_LIMIT", "20"))
    half_life_days: float = float(os.getenv("MEMORY_HALF_LIFE_DAYS", "30"))
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
    log_hash_salt: str = os.getenv("LOG_HASH_SALT", "change-this-in-production")
