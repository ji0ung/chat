from __future__ import annotations

from functools import lru_cache
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

from app.config import Settings
from app.memory import MemoryService, build_character_prompt
from app.observability import PrivacyFilter, configure_logging, log_event, request_id_var
from app.services import (
    LocalSentenceTransformerEmbedder,
    OllamaChatGenerator,
    OllamaEmbedder,
    OpenAIChatGenerator,
    OpenAIEmbedder,
)
from app.store import SQLiteMemoryStore

settings = Settings()
logger = configure_logging(settings)
privacy = PrivacyFilter(settings)
app = FastAPI(title="Character Chat Long-term Memory MVP", version="0.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


@app.middleware("http")
async def request_logging(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", str(uuid4()))[:128]
    token = request_id_var.set(request_id)
    started = perf_counter()
    try:
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        log_event(
            logger,
            "http_request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round((perf_counter() - started) * 1000, 2),
        )
        return response
    except Exception:
        logger.exception(
            "http_request_failed",
            extra={
                "event": "http_request_failed",
                "fields": {
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": round((perf_counter() - started) * 1000, 2),
                },
            },
        )
        raise
    finally:
        request_id_var.reset(token)


class MessageRequest(BaseModel):
    user_id: str
    conversation_id: str
    message: str = Field(min_length=1)
    character_prompt: str = "너는 다정하고 일관된 가상 캐릭터다. 한국어로 자연스럽게 답한다."
    importance: float = Field(default=0.5, ge=0, le=1)


class MemoryResult(BaseModel):
    id: int
    content: str
    score: float
    similarity: float
    importance: float
    recency: float
    frequency: float


class ChatResponse(BaseModel):
    answer: str
    recalled_memories: list[MemoryResult]

class EvaluationRequest(BaseModel):
    conversation_id: str
    user_id: str = "anonymous"
    memory_recall: int = Field(ge=1, le=5)
    natural_use: int = Field(ge=1, le=5)
    no_false_memory: int = Field(ge=1, le=5)
    character_consistency: int = Field(ge=1, le=5)
    relationship_continuity: int = Field(ge=1, le=5)
    note: str = Field(default="", max_length=500)


@lru_cache
def dependencies() -> tuple[MemoryService, OpenAIChatGenerator]:
    client: OpenAI | None = None
    if settings.embedding_provider == "openai" or settings.llm_provider == "openai":
        client = OpenAI()
    if settings.embedding_provider == "ollama":
        embedder = OllamaEmbedder(settings.ollama_base_url, settings.ollama_embedding_model)
    elif settings.embedding_provider == "local":
        embedder = LocalSentenceTransformerEmbedder(settings.local_embedding_model)
    elif settings.embedding_provider == "openai":
        assert client is not None
        embedder = OpenAIEmbedder(client, settings.embedding_model)
    else:
        raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {settings.embedding_provider}")

    if settings.llm_provider == "ollama":
        generator = OllamaChatGenerator(settings.ollama_base_url, settings.ollama_chat_model)
    elif settings.llm_provider == "openrouter":
        if not settings.openrouter_api_key:
            raise RuntimeError("OPENROUTER_API_KEY is required when LLM_PROVIDER=openrouter")
        router_client = OpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
            default_headers={"HTTP-Referer": "http://localhost", "X-Title": "Luna Memory"},
        )
        generator = OpenAIChatGenerator(router_client, settings.openrouter_model)
    elif settings.llm_provider == "openai":
        assert client is not None
        generator = OpenAIChatGenerator(client, settings.chat_model)
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {settings.llm_provider}")

    store = SQLiteMemoryStore(settings.db_path)
    memory = MemoryService(
        store,
        embedder,
        top_k=settings.top_k,
        candidate_limit=settings.candidate_limit,
        half_life_days=settings.half_life_days,
    )
    return memory, generator


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "llm_provider": settings.llm_provider,
        "embedding_provider": settings.embedding_provider,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: MessageRequest) -> ChatResponse:
    memory, generator = dependencies()
    user_ref = privacy.hash_identifier(request.user_id)
    conversation_ref = privacy.hash_identifier(request.conversation_id)
    started = perf_counter()
    log_event(
        logger,
        "chat_received",
        user_ref=user_ref,
        conversation_ref=conversation_ref,
        importance=request.importance,
        **privacy.text_fields(request.message),
    )

    recall_started = perf_counter()
    recalled = memory.recall(user_id=request.user_id, query=request.message)
    log_event(
        logger,
        "memory_recalled",
        user_ref=user_ref,
        conversation_ref=conversation_ref,
        duration_ms=round((perf_counter() - recall_started) * 1000, 2),
        result_count=len(recalled),
        results=[
            {
                "memory_id": item.memory.id,
                "score": round(item.score, 4),
                "similarity": round(item.similarity, 4),
                "importance": round(item.importance, 4),
                "recency": round(item.recency, 4),
                "frequency": round(item.frequency, 4),
                **privacy.text_fields(item.memory.content, "memory"),
            }
            for item in recalled
        ],
    )
    prompt = build_character_prompt(request.character_prompt, recalled)
    generation_started = perf_counter()
    answer = generator.generate(prompt, request.message)
    generation_ms = round((perf_counter() - generation_started) * 1000, 2)

    # The user turn and generated reply both become future retrieval candidates.
    memory.remember(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        role="user",
        content=request.message,
        importance=request.importance,
    )
    memory.remember(
        user_id=request.user_id,
        conversation_id=request.conversation_id,
        role="assistant",
        content=answer,
        importance=max(0.3, request.importance * 0.8),
    )
    log_event(
        logger,
        "chat_completed",
        user_ref=user_ref,
        conversation_ref=conversation_ref,
        total_duration_ms=round((perf_counter() - started) * 1000, 2),
        generation_duration_ms=generation_ms,
        recalled_count=len(recalled),
        **privacy.text_fields(answer, "answer"),
    )
    return ChatResponse(
        answer=answer,
        recalled_memories=[
            MemoryResult(
                id=item.memory.id,
                content=item.memory.content,
                score=item.score,
                similarity=item.similarity,
                importance=item.importance,
                recency=item.recency,
                frequency=item.frequency,
            )
            for item in recalled
        ],
    )

@app.post("/evaluations")
def create_evaluation(request: EvaluationRequest) -> dict[str, int | str]:
    memory, _ = dependencies()
    evaluation_id = memory.store.add_evaluation(**request.model_dump())
    log_event(logger, "session_evaluated", conversation_ref=privacy.hash_identifier(request.conversation_id), evaluation_id=evaluation_id)
    return {"id": evaluation_id, "status": "saved"}

@app.get("/evaluations")
def get_evaluations(limit: int = 100) -> dict[str, object]:
    memory, _ = dependencies()
    items = memory.store.list_evaluations(max(1, min(limit, 500)))
    scores = [sum(item[key] for key in ("memory_recall", "natural_use", "no_false_memory", "character_consistency", "relationship_continuity")) / 5 for item in items]
    return {"items": items, "count": len(items), "average": round(sum(scores) / len(scores), 2) if scores else None}

@app.get("/admin/overview")
def admin_overview() -> dict[str, object]:
    memory, _ = dependencies()
    return memory.store.admin_overview()
