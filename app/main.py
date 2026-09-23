from __future__ import annotations

from functools import lru_cache
import re
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from pydantic import BaseModel, Field

from app.config import Settings
from app.memory import MemoryService, build_character_prompt
from app.observability import PrivacyFilter, configure_logging, log_event, request_id_var
from app.security import (
    IdempotencyCache,
    InputPolicyError,
    SlidingWindowRateLimiter,
    looks_like_prompt_injection,
    normalize_message,
    should_store_as_memory,
)
from app.services import (
    HashingEmbedder,
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
user_limiter = SlidingWindowRateLimiter(settings.rate_limit_per_minute)
ip_limiter = SlidingWindowRateLimiter(settings.ip_rate_limit_per_minute)
idempotency_cache = IdempotencyCache(settings.idempotency_ttl_seconds)

app = FastAPI(title="Character Chat Long-term Memory MVP", version="0.3.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.allowed_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-Request-ID",
        "Idempotency-Key",
        "X-Admin-Token",
    ],
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
    # Development fallback only. When MVP_ACCESS_TOKENS is configured, the
    # authenticated token decides the real user id and this field is ignored.
    user_id: str = Field(min_length=1, max_length=128)
    conversation_id: str = Field(min_length=1, max_length=128)
    message: str
    character_prompt: str = Field(
        default="너는 다정하고 일관된 가상 캐릭터다. 한국어로 자연스럽게 답한다.",
        max_length=12000,
    )
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
    conversation_id: str = Field(min_length=1, max_length=128)
    user_id: str = Field(default="anonymous", min_length=1, max_length=128)
    memory_recall: int = Field(ge=1, le=5)
    natural_use: int = Field(ge=1, le=5)
    no_false_memory: int = Field(ge=1, le=5)
    character_consistency: int = Field(ge=1, le=5)
    relationship_continuity: int = Field(ge=1, le=5)
    note: str = Field(default="", max_length=500)


def policy_error(error: InputPolicyError) -> HTTPException:
    return HTTPException(
        status_code=error.status_code,
        detail={"code": error.code, "message": error.message},
    )


def _bearer_token(authorization: str | None) -> str | None:
    if not authorization:
        return None
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        return None
    return authorization[len(prefix):].strip()


def resolve_user_id(body_user_id: str, authorization: str | None) -> str:
    # Local/dev compatibility: no token map means body user_id is allowed.
    # Before external sharing, configure MVP_ACCESS_TOKENS.
    if not settings.access_tokens:
        return body_user_id

    token = _bearer_token(authorization)
    if not token or token not in settings.access_tokens:
        raise HTTPException(
            status_code=401,
            detail={"code": "AUTH_REQUIRED", "message": "다시 로그인해주세요."},
        )
    return settings.access_tokens[token]


def require_admin(x_admin_token: str | None) -> None:
    if not settings.admin_api_token:
        return
    if x_admin_token != settings.admin_api_token:
        raise HTTPException(
            status_code=403,
            detail={"code": "FORBIDDEN", "message": "이 요청을 처리할 권한이 없습니다."},
        )


def enforce_rate_limits(user_id: str, request: Request) -> None:
    client_ip = request.client.host if request.client else "unknown"
    if not ip_limiter.allow(client_ip):
        raise HTTPException(
            status_code=429,
            detail={"code": "RATE_LIMIT", "message": "요청이 너무 많아요. 잠시 후 다시 시도해주세요."},
        )
    if not user_limiter.allow(user_id):
        raise HTTPException(
            status_code=429,
            detail={"code": "RATE_LIMIT", "message": "요청이 너무 많아요. 잠시 후 다시 시도해주세요."},
        )


def clean_model_answer(answer: str) -> str:
    cleaned = re.sub(r"(?im)^\s*(user safety|safety|assistant|system)\s*:\s*.*$", "", answer)
    cleaned = re.sub(r"<[^>]+>", "", cleaned).strip()
    odd_ratio = sum(1 for char in cleaned if char in "�□■●○◇◆�") / max(len(cleaned), 1)
    if not cleaned or odd_ratio > 0.05:
        return "잠깐, 방금 말이 조금 꼬였어. 다시 자연스럽게 얘기해볼게. 무슨 일이 있었어?"
    return cleaned


@lru_cache
def dependencies() -> tuple[MemoryService, object]:
    client: OpenAI | None = None
    if settings.embedding_provider == "openai" or settings.llm_provider == "openai":
        client = OpenAI()
    if settings.embedding_provider == "ollama":
        embedder = OllamaEmbedder(settings.ollama_base_url, settings.ollama_embedding_model)
    elif settings.embedding_provider in {"hash", "local"}:
        embedder = HashingEmbedder(settings.hash_embedding_dimensions)
    elif settings.embedding_provider in {"sentence-transformer", "sentence_transformer"}:
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


@lru_cache
def memory_store() -> SQLiteMemoryStore:
    return SQLiteMemoryStore(settings.db_path)


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "llm_provider": settings.llm_provider,
        "embedding_provider": settings.embedding_provider,
        "auth_mode": "token" if settings.access_tokens else "development",
    }


@app.post("/chat", response_model=ChatResponse)
def chat(
    payload: MessageRequest,
    http_request: Request,
    authorization: str | None = Header(default=None),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
) -> ChatResponse:
    user_id = resolve_user_id(payload.user_id, authorization)
    enforce_rate_limits(user_id, http_request)

    try:
        message = normalize_message(
            payload.message,
            max_chars=settings.message_max_chars,
            max_same_char_run=settings.message_max_same_char_run,
            max_urls=settings.message_max_urls,
            replacement_char_ratio=settings.replacement_char_ratio,
        )
    except InputPolicyError as exc:
        raise policy_error(exc) from exc

    cache_key = None
    if idempotency_key:
        cache_key = f"{user_id}:{idempotency_key[:128]}"
        cached = idempotency_cache.get(cache_key)
        if cached:
            return ChatResponse(**cached)

    memory, generator = dependencies()
    user_ref = privacy.hash_identifier(user_id)
    conversation_ref = privacy.hash_identifier(payload.conversation_id)
    started = perf_counter()
    suspicious_prompt = looks_like_prompt_injection(message)

    log_event(
        logger,
        "chat_received",
        user_ref=user_ref,
        conversation_ref=conversation_ref,
        importance=payload.importance,
        prompt_injection_suspected=suspicious_prompt,
        **privacy.text_fields(message),
    )

    recall_started = perf_counter()
    recalled = memory.recall(user_id=user_id, query=message)
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

    prompt = build_character_prompt(payload.character_prompt, recalled)
    generation_started = perf_counter()
    answer = clean_model_answer(generator.generate(prompt, message))
    generation_ms = round((perf_counter() - generation_started) * 1000, 2)

    if should_store_as_memory(message):
        memory.remember(
            user_id=user_id,
            conversation_id=payload.conversation_id,
            role="user",
            content=message,
            importance=payload.importance,
        )

    log_event(
        logger,
        "chat_completed",
        user_ref=user_ref,
        conversation_ref=conversation_ref,
        total_duration_ms=round((perf_counter() - started) * 1000, 2),
        generation_duration_ms=generation_ms,
        recalled_count=len(recalled),
        prompt_injection_suspected=suspicious_prompt,
        **privacy.text_fields(answer, "answer"),
    )

    result = ChatResponse(
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
    if cache_key:
        idempotency_cache.put(cache_key, result.model_dump())
    return result


@app.post("/evaluations")
def create_evaluation(
    payload: EvaluationRequest,
    authorization: str | None = Header(default=None),
) -> dict[str, int | str]:
    user_id = resolve_user_id(payload.user_id, authorization)
    memory, _ = dependencies()
    data = payload.model_dump()
    data["user_id"] = user_id
    evaluation_id = memory.store.add_evaluation(**data)
    log_event(
        logger,
        "session_evaluated",
        conversation_ref=privacy.hash_identifier(payload.conversation_id),
        evaluation_id=evaluation_id,
    )
    return {"id": evaluation_id, "status": "saved"}


@app.get("/evaluations")
def get_evaluations(
    limit: int = 100,
    x_admin_token: str | None = Header(default=None, alias="X-Admin-Token"),
) -> dict[str, object]:
    require_admin(x_admin_token)
    memory, _ = dependencies()
    items = memory.store.list_evaluations(max(1, min(limit, 500)))
    scores = [
        sum(
            item[key]
            for key in (
                "memory_recall",
                "natural_use",
                "no_false_memory",
                "character_consistency",
                "relationship_continuity",
            )
        )
        / 5
        for item in items
    ]
    return {
        "items": items,
        "count": len(items),
        "average": round(sum(scores) / len(scores), 2) if scores else None,
    }


@app.get("/admin/overview")
def admin_overview(
    x_admin_token: str | None = Header(default=None, alias="X-Admin-Token"),
) -> dict[str, object]:
    require_admin(x_admin_token)
    return memory_store().admin_overview()
