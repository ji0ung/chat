from __future__ import annotations

import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

from app.models import Memory, RankedMemory


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _parse_dt(value: str) -> datetime:
    dt = datetime.fromisoformat(value)
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Embedding dimensions do not match")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0


class SQLiteMemoryStore:
    """Small embedded vector store. Vectors live in SQLite; ranking runs in Python."""

    def __init__(self, path: str) -> None:
        self.path = path
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    conversation_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    importance REAL NOT NULL,
                    created_at TEXT NOT NULL,
                    last_accessed_at TEXT NOT NULL,
                    access_count INTEGER NOT NULL DEFAULT 0,
                    embedding TEXT NOT NULL
                )
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_user ON memories(user_id, id DESC)"
            )

    def add(
        self,
        *,
        user_id: str,
        conversation_id: str,
        role: str,
        content: str,
        importance: float,
        embedding: list[float],
    ) -> int:
        now = _utcnow().isoformat()
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO memories
                    (user_id, conversation_id, role, content, importance,
                     created_at, last_accessed_at, embedding)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, conversation_id, role, content, importance, now, now, json.dumps(embedding)),
            )
            return int(cursor.lastrowid)

    def search(
        self,
        *,
        user_id: str,
        query_embedding: list[float],
        top_k: int,
        candidate_limit: int,
        half_life_days: float,
        now: datetime | None = None,
    ) -> list[RankedMemory]:
        now = now or _utcnow()
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM memories WHERE user_id = ? ORDER BY id DESC",
                (user_id,),
            ).fetchall()

        candidates: list[tuple[Memory, float]] = []
        for row in rows:
            memory = self._row_to_memory(row)
            similarity = max(0.0, cosine_similarity(query_embedding, memory.embedding))
            candidates.append((memory, similarity))

        # Stage 1: semantic preselection. A production vector DB would do this step.
        candidates.sort(key=lambda item: item[1], reverse=True)
        ranked: list[RankedMemory] = []
        for memory, similarity in candidates[:candidate_limit]:
            age_days = max(0.0, (now - memory.created_at).total_seconds() / 86400)
            recency = math.exp(-math.log(2) * age_days / max(half_life_days, 0.001))
            frequency = min(1.0, math.log1p(memory.access_count) / math.log(11))
            # Semantic relevance dominates; the other signals break close matches.
            score = 0.60 * similarity + 0.20 * memory.importance + 0.15 * recency + 0.05 * frequency
            ranked.append(
                RankedMemory(memory, similarity, recency, memory.importance, frequency, score)
            )

        selected = sorted(ranked, key=lambda item: item.score, reverse=True)[:top_k]
        if selected:
            ids = [item.memory.id for item in selected]
            placeholders = ",".join("?" for _ in ids)
            with self._connect() as conn:
                conn.execute(
                    f"UPDATE memories SET last_accessed_at = ?, access_count = access_count + 1 "
                    f"WHERE id IN ({placeholders})",
                    [now.isoformat(), *ids],
                )
        return selected

    @staticmethod
    def _row_to_memory(row: sqlite3.Row) -> Memory:
        return Memory(
            id=row["id"],
            user_id=row["user_id"],
            conversation_id=row["conversation_id"],
            role=row["role"],
            content=row["content"],
            importance=row["importance"],
            created_at=_parse_dt(row["created_at"]),
            last_accessed_at=_parse_dt(row["last_accessed_at"]),
            access_count=row["access_count"],
            embedding=json.loads(row["embedding"]),
        )
