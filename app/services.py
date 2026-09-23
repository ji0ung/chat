from __future__ import annotations

from typing import Protocol

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

