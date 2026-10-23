"""Shared data types used throughout the RAG pipeline."""
from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field, field_validator

class Document(BaseModel):
    """A normalized source document before or after chunking."""
    id: str
    text: str
    metadata: dict[str, Any] = Field(default_factory=dict)

class SourceRecord(BaseModel):
    id: str
    source: str
    type: str
    chunks: int
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class QueryRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4000)
    session_id: str | None = Field(default=None, min_length=8, max_length=128, pattern=r"^[A-Za-z0-9_-]+$")
    top_k: int | None = Field(default=None, ge=1, le=100)
    metadata_filter: dict[str, Any] | None = None
    customer_context: dict[str, Any] = Field(default_factory=dict)

    @field_validator("question")
    @classmethod
    def question_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("question must contain non-whitespace text")
        return value

    @field_validator("customer_context")
    @classmethod
    def customer_context_must_be_bounded(cls, value: dict[str, Any]) -> dict[str, Any]:
        import json
        if len(value) > 40 or len(json.dumps(value, ensure_ascii=False, default=str)) > 12000:
            raise ValueError("customer_context is too large; send only approved context fields")
        return value

class Citation(BaseModel):
    chunk_id: str
    source: str
    page: int | None = None
    text: str
    score: float | None = None

class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]
    rewritten_query: str

