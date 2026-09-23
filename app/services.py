from __future__ import annotations

from typing import Protocol
import json
from urllib.request import Request, urlopen

from openai import OpenAI


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]: ...


class ChatGenerator(Protocol):
    def generate(self, system_prompt: str, user_message: str) -> str: ...


class OpenAIEmbedder:
    def __init__(self, client: OpenAI, model: str) -> None:
        self.client = client
        self.model = model

    def embed(self, text: str) -> list[float]:
        normalized = text.replace("\n", " ").strip()
        result = self.client.embeddings.create(model=self.model, input=normalized)
        return result.data[0].embedding


class OpenAIChatGenerator:
    def __init__(self, client: OpenAI, model: str) -> None:
        self.client = client
        self.model = model

    def generate(self, system_prompt: str, user_message: str) -> str:
        result = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=user_message,
        )
        return result.output_text


class OllamaEmbedder:
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def embed(self, text: str) -> list[float]:
        payload = json.dumps({"model": self.model, "input": text}).encode()
        request = Request(
            f"{self.base_url}/api/embed",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=120) as response:
            body = json.loads(response.read())
        embeddings = body.get("embeddings")
        if not embeddings:
            raise RuntimeError(f"Ollama embedding response did not contain embeddings: {body}")
        return embeddings[0]


class LocalSentenceTransformerEmbedder:
    def __init__(self, model_name: str) -> None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "로컬 임베딩을 사용하려면 sentence-transformers를 설치하세요."
            ) from exc
        self.model = SentenceTransformer(model_name)

    def embed(self, text: str) -> list[float]:
        vector = self.model.encode(text, normalize_embeddings=True)
        return vector.tolist()


class OllamaChatGenerator:
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, system_prompt: str, user_message: str) -> str:
        payload = json.dumps(
            {
                "model": self.model,
                "stream": False,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
            }
        ).encode()
        request = Request(
            f"{self.base_url}/api/chat",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request, timeout=180) as response:
            body = json.loads(response.read())
        answer = body.get("message", {}).get("content")
        if not answer:
            raise RuntimeError(f"Ollama chat response did not contain content: {body}")
        return answer
