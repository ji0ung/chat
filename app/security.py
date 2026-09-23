from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from threading import Lock
from time import monotonic
import re
import unicodedata

URL_RE = re.compile(r"https?://[^\s]+", re.IGNORECASE)
CONTROL_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
PROMPT_INJECTION_PATTERNS = [
    re.compile(r"(이전|위의|앞의).{0,12}(지시|명령).{0,12}(무시|잊어)", re.IGNORECASE),
    re.compile(r"(system|developer)\s*prompt", re.IGNORECASE),
    re.compile(r"(시스템|개발자)\s*(프롬프트|지시)", re.IGNORECASE),
    re.compile(r"(비밀키|api\s*key|환경변수|내부\s*로그).{0,12}(출력|보여|공개)", re.IGNORECASE),
    re.compile(r"(long_term_memory|memory block).{0,12}(출력|보여|공개)", re.IGNORECASE),
]
MEMORY_COMMAND_PATTERNS = [
    re.compile(r"(중요도|importance)\s*[:=]?\s*(100|1\.0)", re.IGNORECASE),
    re.compile(r"(영원히|무조건).{0,8}기억", re.IGNORECASE),
    re.compile(r"(기억|메모리).{0,12}(전부|모두).{0,8}(삭제|지워)", re.IGNORECASE),
]


@dataclass(frozen=True)
class InputPolicyError(Exception):
    code: str
    message: str
    status_code: int = 400


def normalize_message(
    text: str,
    *,
    max_chars: int = 4000,
    max_same_char_run: int = 100,
    max_urls: int = 10,
    replacement_char_ratio: float = 0.20,
) -> str:
    if not isinstance(text, str):
        raise InputPolicyError("INVALID_TEXT", "입력 내용을 확인해주세요.")

    normalized = unicodedata.normalize("NFC", text)
    normalized = CONTROL_RE.sub("", normalized)
    normalized = re.sub(r"\n{4,}", "\n\n\n", normalized)
    normalized = normalized.strip()

    if not normalized:
        raise InputPolicyError("EMPTY_MESSAGE", "메시지를 입력해주세요.")

    if len(normalized) > max_chars:
        raise InputPolicyError(
            "MESSAGE_TOO_LONG",
            f"메시지가 너무 길어요. {max_chars:,}자 이하로 줄여주세요.",
            413,
        )

    if re.search(rf"(.)\1{{{max_same_char_run - 1},}}", normalized, flags=re.DOTALL):
        raise InputPolicyError(
            "INVALID_TEXT",
            "같은 문자가 너무 많이 반복됐어요. 반복을 줄여주세요.",
        )

    url_count = len(URL_RE.findall(normalized))
    if url_count > max_urls:
        raise InputPolicyError(
            "INVALID_TEXT",
            f"한 메시지에는 링크를 {max_urls}개까지만 보낼 수 있어요.",
        )

    replacement_count = normalized.count("�")
    if replacement_count / max(len(normalized), 1) > replacement_char_ratio:
        raise InputPolicyError("INVALID_TEXT", "문자가 깨져 있어요. 입력 내용을 확인해주세요.")

    return normalized


def looks_like_prompt_injection(text: str) -> bool:
    return any(pattern.search(text) for pattern in PROMPT_INJECTION_PATTERNS)


def looks_like_memory_command(text: str) -> bool:
    return any(pattern.search(text) for pattern in MEMORY_COMMAND_PATTERNS)


def should_store_as_memory(text: str) -> bool:
    compact = re.sub(r"\s+", "", text)
    low_signal = {
        "ㅇ", "응", "예", "네", "아", "ㅋ", "ㅋㅋ", "ㅋㅋㅋ", "ㅎㅎ", "ㅠㅠ",
        "뭔소리야", "뭐야", "뭐해", "잘자", "그래", "ㅇㅇ",
    }
    if len(compact) < 2 or compact in low_signal:
        return False
    if looks_like_prompt_injection(text) or looks_like_memory_command(text):
        return False
    return True


class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: float = 60.0) -> None:
        self.limit = max(1, limit)
        self.window_seconds = window_seconds
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def allow(self, key: str) -> bool:
        now = monotonic()
        cutoff = now - self.window_seconds
        with self._lock:
            bucket = self._events[key]
            while bucket and bucket[0] < cutoff:
                bucket.popleft()
            if len(bucket) >= self.limit:
                return False
            bucket.append(now)
            return True


class IdempotencyCache:
    def __init__(self, ttl_seconds: float = 300.0, max_entries: int = 1000) -> None:
        self.ttl_seconds = ttl_seconds
        self.max_entries = max_entries
        self._items: dict[str, tuple[float, dict]] = {}
        self._lock = Lock()

    def get(self, key: str) -> dict | None:
        now = monotonic()
        with self._lock:
            item = self._items.get(key)
            if not item:
                return None
            created_at, value = item
            if now - created_at > self.ttl_seconds:
                self._items.pop(key, None)
                return None
            return value

    def put(self, key: str, value: dict) -> None:
        now = monotonic()
        with self._lock:
            if len(self._items) >= self.max_entries:
                oldest_key = min(self._items, key=lambda item_key: self._items[item_key][0])
                self._items.pop(oldest_key, None)
            self._items[key] = (now, value)
