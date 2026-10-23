"""OpenAI-compatible, Ollama, and Anthropic chat adapters."""
from __future__ import annotations

import json
import os
from collections.abc import Iterator

import httpx

from core.config import LLMConfig
from core.interfaces import LLM


def _messages(system_prompt: str, prompt: str) -> list[dict[str, str]]:
    messages = []
    if system_prompt.strip():
        messages.append({"role": "system", "content": system_prompt.strip()})
    messages.append({"role": "user", "content": prompt})
    return messages


class OpenAICompatibleLLM(LLM):
    def __init__(self, config: LLMConfig):
        self.c = config

    def _request(self, system_prompt: str, prompt: str, stream: bool = False) -> dict:
        base = self.c.base_url or os.getenv("RAG_LLM_BASE_URL", "https://api.openai.com/v1")
        key = os.getenv(self.c.api_key_env) or os.getenv("RAG_LLM_API_KEY")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        response = httpx.post(
            base.rstrip("/") + "/chat/completions",
            headers=headers,
            json={
                "model": self.c.model,
                "temperature": self.c.temperature,
                "max_tokens": self.c.max_tokens,
                "stream": stream,
                "messages": _messages(system_prompt, prompt),
            },
            timeout=120,
        )
        response.raise_for_status()
        return response.json()

    def generate(self, prompt: str) -> str:
        return self.generate_with_system("", prompt)

    def generate_with_system(self, system_prompt: str, prompt: str) -> str:
        payload = self._request(system_prompt, prompt)
        return payload["choices"][0]["message"]["content"]

    def stream(self, prompt: str) -> Iterator[str]:
        yield from self.stream_with_system("", prompt)

    def stream_with_system(self, system_prompt: str, prompt: str) -> Iterator[str]:
        base = self.c.base_url or os.getenv("RAG_LLM_BASE_URL", "https://api.openai.com/v1")
        key = os.getenv(self.c.api_key_env) or os.getenv("RAG_LLM_API_KEY")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        with httpx.stream(
            "POST",
            base.rstrip("/") + "/chat/completions",
            headers=headers,
            json={
                "model": self.c.model,
                "temperature": self.c.temperature,
                "max_tokens": self.c.max_tokens,
                "stream": True,
                "messages": _messages(system_prompt, prompt),
            },
            timeout=120,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if not line.startswith("data: ") or line == "data: [DONE]":
                    continue
                payload = json.loads(line[6:])
                content = payload["choices"][0].get("delta", {}).get("content")
                if content:
                    yield content


class OllamaLLM(LLM):
    def __init__(self, config: LLMConfig):
        self.c = config

    def generate(self, prompt: str) -> str:
        return self.generate_with_system("", prompt)

    def generate_with_system(self, system_prompt: str, prompt: str) -> str:
        base = self.c.base_url or os.getenv("RAG_OLLAMA_BASE_URL", "http://localhost:11434")
        response = httpx.post(
            base.rstrip("/") + "/api/chat",
            json={
                "model": self.c.model,
                "stream": False,
                "think": False,
                "messages": _messages(system_prompt, prompt),
                "options": {"temperature": self.c.temperature, "num_predict": self.c.max_tokens},
            },
            timeout=300,
        )
        response.raise_for_status()
        return response.json()["message"]["content"]

    def stream(self, prompt: str) -> Iterator[str]:
        yield from self.stream_with_system("", prompt)

    def stream_with_system(self, system_prompt: str, prompt: str) -> Iterator[str]:
        base = self.c.base_url or os.getenv("RAG_OLLAMA_BASE_URL", "http://localhost:11434")
        with httpx.stream(
            "POST",
            base.rstrip("/") + "/api/chat",
            json={
                "model": self.c.model,
                "stream": True,
                "think": False,
                "messages": _messages(system_prompt, prompt),
                "options": {"temperature": self.c.temperature, "num_predict": self.c.max_tokens},
            },
            timeout=300,
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    content = json.loads(line).get("message", {}).get("content")
                    if content:
                        yield content


class AnthropicLLM(LLM):
    def __init__(self, config: LLMConfig):
        self.c = config

    def generate(self, prompt: str) -> str:
        return self.generate_with_system("", prompt)

    def generate_with_system(self, system_prompt: str, prompt: str) -> str:
        import anthropic

        key = os.getenv(self.c.api_key_env)
        if not key:
            raise RuntimeError(f"Set {self.c.api_key_env} for Anthropic")
        kwargs = {"system": system_prompt} if system_prompt.strip() else {}
        result = anthropic.Anthropic(api_key=key).messages.create(
            model=self.c.model,
            max_tokens=self.c.max_tokens,
            temperature=self.c.temperature,
            messages=[{"role": "user", "content": prompt}],
            **kwargs,
        )
        return result.content[0].text


def make_llm(config: LLMConfig) -> LLM:
    return {"openai_compatible": OpenAICompatibleLLM, "ollama": OllamaLLM, "anthropic": AnthropicLLM}[config.provider](config)
