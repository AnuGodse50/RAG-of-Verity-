"""Validated per-project YAML configuration."""
from __future__ import annotations
import os
from pathlib import Path
from typing import Any, Literal
import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

class LoaderConfig(BaseModel):
    allowed_extensions: list[str] = Field(default_factory=list)
    allowed_sources: list[str] = Field(default_factory=list)
    ocr: bool = True
    sql_query: str | None = None

class ChunkingConfig(BaseModel):
    strategy: Literal["recursive", "structure", "code", "row_group"] = "recursive"
    chunk_size: int = Field(default=1000, ge=100, le=50000)
    overlap: int = Field(default=150, ge=0, le=10000)
    row_group_size: int = Field(default=10, ge=1, le=1000)
    @model_validator(mode="after")
    def overlap_smaller_than_chunk(self):
        if self.overlap >= self.chunk_size:
            raise ValueError("chunking.overlap must be smaller than chunking.chunk_size")
        return self

class EmbeddingConfig(BaseModel):
    provider: Literal["sentence_transformers", "openai_compatible", "ollama"] = "sentence_transformers"
    model: str = "BAAI/bge-m3"
    base_url: str | None = None
    local_files_only: bool = False

class StoreConfig(BaseModel):
    provider: Literal["chroma", "qdrant"] = "chroma"
    path: str = "./data/chroma"
    url: str | None = None

class RetrievalConfig(BaseModel):
    top_k: int = Field(default=5, ge=1, le=100)
    candidate_k: int = Field(default=30, ge=1, le=500)
    rrf_k: int = Field(default=60, ge=1)
    min_similarity: float = Field(default=0.32, ge=-1.0, le=1.0)
    reranker: bool = False
    reranker_model: str = "BAAI/bge-reranker-v2-m3"

class LLMConfig(BaseModel):
    provider: Literal["openai_compatible", "ollama", "anthropic"] = "openai_compatible"
    model: str = Field(default_factory=lambda: os.getenv("RAG_LLM_MODEL", "openai/gpt-oss-20b"))
    base_url: str | None = None
    api_key_env: str = "RAG_LLM_API_KEY"
    temperature: float = 0.0
    max_tokens: int = 1200

class ContextRequirement(BaseModel):
    patterns: list[str]
    required_fields: list[str]
    missing_responses: dict[str, str] = Field(default_factory=dict)
    @field_validator("patterns")
    @classmethod
    def validate_context_patterns(cls, patterns: list[str]) -> list[str]:
        import re
        for pattern in patterns:
            try: re.compile(pattern)
            except re.error as exc: raise ValueError(f"Invalid context requirement regex {pattern!r}: {exc}") from exc
        return patterns

class AgentConfig(BaseModel):
    name: str = ""
    role: str = ""
    system_instructions: str = ""
    customer_context_fields: list[str] = Field(default_factory=list)
    retrieval_context_fields: list[str] = Field(default_factory=list)
    private_content_patterns: list[str] = Field(default_factory=list)
    private_output_patterns: list[str] = Field(default_factory=list)
    sensitive_context_patterns: list[str] = Field(default_factory=list)
    blocked_question_patterns: list[str] = Field(default_factory=list)
    out_of_scope_patterns: list[str] = Field(default_factory=list)
    out_of_scope_response: str = "I can help with your KYC/KYB verification, documents, status, consent requests, appeals, and account security. Please ask a question related to your verification."
    bypass_question_patterns: list[str] = Field(default_factory=list)
    bypass_response: str = "I can’t help with bypassing verification or security controls. Please complete the required steps in your KYC/KYB application."
    clarification_patterns: list[str] = Field(default_factory=list)
    clarification_response: str = "Which section are you currently on in your KYC/KYB application?"
    context_requirements: list[ContextRequirement] = Field(default_factory=list)
    context_sensitive_patterns: list[str] = Field(default_factory=list)
    context_required_fields: list[str] = Field(default_factory=list)
    context_questions: dict[str, str] = Field(default_factory=dict)
    sensitive_input_patterns: list[str] = Field(default_factory=list)
    sensitive_input_response: str = "For your security, please do not share passwords, OTPs, card details, or full identity-document numbers in chat."
    fallback_response: str = "I couldn't find this in the provided data."
    @field_validator("private_content_patterns","private_output_patterns","sensitive_context_patterns","blocked_question_patterns","out_of_scope_patterns","bypass_question_patterns","clarification_patterns","context_sensitive_patterns","sensitive_input_patterns")
    @classmethod
    def validate_patterns(cls,patterns:list[str])->list[str]:
        import re
        for pattern in patterns:
            try:re.compile(pattern)
            except re.error as exc:raise ValueError(f"Invalid agent safety regex {pattern!r}: {exc}") from exc
        return patterns

class ProjectConfig(BaseModel):
    name: str
    collection: str
    loaders: LoaderConfig = Field(default_factory=LoaderConfig)
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)
    embedding: EmbeddingConfig = Field(default_factory=EmbeddingConfig)
    store: StoreConfig = Field(default_factory=StoreConfig)
    retrieval: RetrievalConfig = Field(default_factory=RetrievalConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    agent_profile: str | None = None
    prompt_template: str = """Answer only from the context below. If it does not support an answer, say: I couldn't find this in the provided data. Cite supporting claims with [source, page/chunk id].\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"""
    metadata_schema: dict[str, str] = Field(default_factory=dict)
    @model_validator(mode="after")
    def validate_prompt(self):
        if "{context}" not in self.prompt_template or "{question}" not in self.prompt_template:
            raise ValueError("prompt_template must contain {context} and {question}")
        return self

def load_project_config(name: str, projects_dir: str | Path | None = None) -> ProjectConfig:
    """Load and validate a named YAML config; errors identify the config path."""
    base = Path(projects_dir or os.getenv("RAG_PROJECTS_DIR", "projects"))
    path = base / f"{name}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Project config not found: {path}")
    try:
        raw: Any = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        profile_name=raw.get("agent_profile")
        if profile_name:
            if not isinstance(profile_name,str) or not profile_name.replace("_","").replace("-","").isalnum():raise ValueError("agent_profile may contain letters, numbers, hyphens, and underscores")
            agents_dir=Path(os.getenv("RAG_AGENTS_DIR", "agents"))
            agent_path=agents_dir/f"{profile_name}.yaml"
            if not agent_path.exists():raise FileNotFoundError(f"Agent profile not found: {agent_path}")
            profile=yaml.safe_load(agent_path.read_text(encoding="utf-8")) or {}
            if profile.get("name")!=profile_name:raise ValueError(f"Agent profile {agent_path} declares name={profile.get('name')!r}, expected {profile_name!r}")
            merged={**profile.get("agent",{}),**raw.get("agent",{})};raw["agent"]=merged
        config = ProjectConfig.model_validate(raw)
    except (yaml.YAMLError, ValidationError) as exc:
        raise ValueError(f"Invalid project config {path}: {exc}") from exc
    if config.name != name:
        raise ValueError(f"Project config {path} declares name={config.name!r}, expected {name!r}")
    return config
