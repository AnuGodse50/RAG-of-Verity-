"""Local Sentence Transformers, Ollama, and OpenAI-compatible embedders."""
from collections.abc import Sequence
import os, httpx
from core.config import EmbeddingConfig
from core.interfaces import Embedder
class SentenceTransformerEmbedder(Embedder):
    def __init__(self,model:str,local_files_only:bool=False):
        self._name=model;self._model=None;self.local_files_only=local_files_only
    @property
    def model_name(self):return self._name
    def embed(self,texts:Sequence[str])->list[list[float]]:
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model=SentenceTransformer(self._name,local_files_only=self.local_files_only)
        return self._model.encode(list(texts),normalize_embeddings=True).tolist()
class OpenAIEmbedder(Embedder):
    def __init__(self,model:str,base_url:str|None=None):self._name=model;self.base=(base_url or "https://api.openai.com/v1").rstrip("/")
    @property
    def model_name(self):return self._name
    def embed(self,texts:Sequence[str])->list[list[float]]:
        key=os.getenv("RAG_EMBEDDING_API_KEY") or os.getenv("RAG_LLM_API_KEY")
        if not key:raise RuntimeError("Set RAG_EMBEDDING_API_KEY or RAG_LLM_API_KEY for API embeddings")
        r=httpx.post(self.base+"/embeddings",headers={"Authorization":f"Bearer {key}"},json={"model":self._name,"input":list(texts)},timeout=90);r.raise_for_status()
        return [x["embedding"] for x in sorted(r.json()["data"],key=lambda x:x["index"])]
class OllamaEmbedder(Embedder):
    """Use Ollama's local /api/embed endpoint; no external API or key is needed."""
    def __init__(self,model:str,base_url:str|None=None):
        self._name=model;self.base=(base_url or os.getenv("RAG_OLLAMA_BASE_URL","http://localhost:11434")).rstrip("/")
    @property
    def model_name(self):return f"ollama:{self._name}"
    def embed(self,texts:Sequence[str])->list[list[float]]:
        if not texts:return []
        try:
            r=httpx.post(self.base+"/api/embed",json={"model":self._name,"input":list(texts)},timeout=180)
            r.raise_for_status()
            vectors=r.json().get("embeddings")
            if not isinstance(vectors,list) or len(vectors)!=len(texts):
                raise RuntimeError("Ollama returned an invalid embedding response; check the model and Ollama version")
            return vectors
        except httpx.ConnectError as exc:
            raise RuntimeError(f"Cannot connect to Ollama at {self.base}. Start the Ollama service and ensure model {self._name!r} is installed.") from exc
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code == 404:
                raise RuntimeError(f"Ollama embedding model {self._name!r} is not available. Pull it on the preparation machine and rebuild the offline bundle.") from exc
            raise RuntimeError(f"Ollama embedding request failed with HTTP {exc.response.status_code}: {exc.response.text[:300]}") from exc
def make_embedder(config:EmbeddingConfig)->Embedder:
    if config.provider=="openai_compatible":return OpenAIEmbedder(config.model,config.base_url)
    if config.provider=="ollama":return OllamaEmbedder(config.model,config.base_url)
    return SentenceTransformerEmbedder(config.model,config.local_files_only)
