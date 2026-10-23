"""Abstract contracts that keep RAG components replaceable."""
from abc import ABC, abstractmethod
from typing import Sequence
from core.models import Document

class Loader(ABC):
    @abstractmethod
    def load(self, source: str) -> list[Document]: """Load a path, URL, or configured data source."""

class Chunker(ABC):
    @abstractmethod
    def chunk(self, document: Document) -> list[Document]: """Split a document into indexed chunks."""

class Embedder(ABC):
    @property
    @abstractmethod
    def model_name(self) -> str: ...
    @abstractmethod
    def embed(self, texts: Sequence[str]) -> list[list[float]]: """Embed a batch of texts."""

class VectorStore(ABC):
    @abstractmethod
    def upsert(self, documents: list[Document], vectors: list[list[float]]) -> None: ...
    @abstractmethod
    def dense_search(self, query_vector: list[float], limit: int, where: dict | None = None) -> list[dict]: ...
    @abstractmethod
    def delete_source(self, source_id: str) -> None: ...
    @abstractmethod
    def list_sources(self) -> list[dict]: ...

class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str: ...
    def generate_with_system(self, system_prompt: str, prompt: str) -> str:
        """Generate with a policy channel when the provider supports one."""
        combined = f"{system_prompt.strip()}\n\n{prompt}" if system_prompt.strip() else prompt
        return self.generate(combined)
    def stream(self, prompt: str):
        """Yield a response; providers may override with token streaming."""
        yield self.generate(prompt)
    def stream_with_system(self, system_prompt: str, prompt: str):
        """Stream with a separate policy channel when supported."""
        combined = f"{system_prompt.strip()}\n\n{prompt}" if system_prompt.strip() else prompt
        yield from self.stream(combined)

