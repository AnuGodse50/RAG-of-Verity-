"""Tests for the Gemini OpenAI-compatible provider configuration."""

from types import SimpleNamespace

from core.config import load_project_config
from llms.providers import OpenAICompatibleLLM


def test_verity_uses_gemini_endpoint_and_model(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    config = load_project_config("verity")
    captured = {}

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"choices": [{"message": {"content": "Grounded test response"}}]}

    def fake_post(url, **kwargs):
        captured.update(url=url, **kwargs)
        return Response()

    monkeypatch.setattr("llms.providers.httpx.post", fake_post)
    answer = OpenAICompatibleLLM(config.llm).generate_with_system("system rule", "test question")

    assert answer == "Grounded test response"
    assert captured["url"] == "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    assert captured["headers"]["Authorization"] == "Bearer test-gemini-key"
    assert captured["json"]["model"] == "gemini-3.8-flash"
    assert captured["json"]["messages"][0] == {"role": "system", "content": "system rule"}
