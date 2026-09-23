from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Memory:
    id: int
    user_id: str
    conversation_id: str
    role: str
    content: str
    importance: float
    created_at: datetime
    last_accessed_at: datetime
    access_count: int
    embedding: list[float]


@dataclass(frozen=True)
class RankedMemory:
    memory: Memory
    similarity: float
    recency: float
    importance: float
    frequency: float
    score: float
