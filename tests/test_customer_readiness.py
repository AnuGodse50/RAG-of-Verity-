"""Security and customer-context checks for the Verity service profile."""
import pytest
from fastapi import HTTPException

from api.security import require_admin_key, require_query_key, validate_production_secrets
from core.config import load_project_config
from core.pipeline import Pipeline


def _profile_pipeline() -> Pipeline:
    pipe = Pipeline.__new__(Pipeline)
    pipe.config = load_project_config("verity")
    return pipe


def test_sarthi_requires_matching_case_market_and_step_before_action_guidance():
    pipe = _profile_pipeline()
    question = "What document should I upload?"
    assert pipe.guard_question(question, {}) == "Are you completing individual KYC or business KYB?"
    assert pipe.guard_question(question, {"case_type": "individual KYC"}) == "Which country or market applies to your verification?"
    assert pipe.guard_question(question, {"case_type": "individual KYC", "market": "India"}) == "Which section are you currently on in your KYC/KYB application?"
    context = {"case_type": "individual KYC", "market": "India", "current_onboarding_step": "address verification"}
    assert pipe.guard_question(question, context) is None


def test_sarthi_never_claims_status_without_trusted_status_context():
    pipe = _profile_pipeline()
    assert pipe.guard_question("Is my KYC done?", {}) == pipe.config.agent.fallback_response


def test_sarthi_blocks_unrelated_college_question():
    pipe = _profile_pipeline()
    assert pipe.guard_question("what is the clg name ?", {}) == pipe.config.agent.out_of_scope_response


def test_sarthi_blocks_otp_requests_and_unapproved_source_files():
    pipe = _profile_pipeline()
    assert pipe.guard_question("Can you give me the OTP?", {}) == pipe.config.agent.sensitive_input_response
    with pytest.raises(ValueError, match="not allowlisted"):
        pipe.ingest(r"C:\private\Verity System Process and Architecture Blueprint.md")


def test_verity_embedding_uses_cached_local_files():
    config = load_project_config("verity")
    assert config.embedding.model == "intfloat/multilingual-e5-small"
    assert config.embedding.local_files_only is True


def test_private_api_requires_separate_query_and_admin_keys(monkeypatch):
    monkeypatch.setenv("RAG_ENV", "development")
    monkeypatch.setenv("RAG_API_KEY", "q" * 32)
    monkeypatch.setenv("RAG_ADMIN_API_KEY", "a" * 32)
    require_query_key("q" * 32)
    require_admin_key("a" * 32)
    with pytest.raises(HTTPException) as query_error:
        require_query_key("a" * 32)
    with pytest.raises(HTTPException) as admin_error:
        require_admin_key("q" * 32)
    assert query_error.value.status_code == admin_error.value.status_code == 401


def test_production_startup_fails_fast_without_hosted_generation_key(monkeypatch):
    monkeypatch.setenv("RAG_ENV", "production")
    monkeypatch.setenv("RAG_API_KEY", "q" * 40)
    monkeypatch.setenv("RAG_ADMIN_API_KEY", "a" * 40)
    monkeypatch.delenv("RAG_LLM_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="requires model credentials"):
        validate_production_secrets()


def test_production_startup_accepts_configured_gemini_key(monkeypatch):
    monkeypatch.setenv("RAG_ENV", "production")
    monkeypatch.setenv("RAG_API_KEY", "q" * 40)
    monkeypatch.setenv("RAG_ADMIN_API_KEY", "a" * 40)
    monkeypatch.setenv("GEMINI_API_KEY", "test-gemini-key")
    validate_production_secrets()
