from core.pipeline import _customer_safe_text, _safe_context
from core.config import AgentConfig, ProjectConfig
from core.pipeline import Pipeline
PRIVATE=[r"\brisk\s*score\b",r"\bsanctions?\b",r"\bPEP\b",r"\breviewer notes?\b",r"\binternal overrides?\b"]

def test_customer_context_keeps_only_approved_fields_and_redacts_internal_values():
    context=_safe_context({"market":"India","current_onboarding_step":"Address verification","reviewer_notes":"do not share","failed_checks":["Clear photo required","PEP match"],"internal_override":"yes"},["market","current_onboarding_step","failed_checks"],PRIVATE)
    assert context=={"market":"India","current_onboarding_step":"Address verification","failed_checks":["Clear photo required"]}

def test_retrieved_internal_lines_are_removed_before_generation_and_citations():
    safe=_customer_safe_text("Upload a clear utility bill.\nInternal reviewer notes: risk score elevated.\nSubmit for verification.",PRIVATE)
    assert "utility bill" in safe and "Submit for verification" in safe
    assert "risk score" not in safe and "reviewer notes" not in safe

def test_sarthi_guard_handles_bypass_sensitive_and_out_of_scope_requests():
    cfg=ProjectConfig(name="test",collection="test",agent=AgentConfig(
        name="sarthi",fallback_response="contact support",bypass_question_patterns=[r"\bbypass\b"],
        bypass_response="complete verification",sensitive_input_patterns=[r"\bOTP\b\s*=\s*\S+"],
        sensitive_input_response="do not share codes",out_of_scope_patterns=[r"\bpolitics\b"],out_of_scope_response="KYC only"))
    pipe=Pipeline.__new__(Pipeline);pipe.config=cfg
    assert pipe.guard_question("How do I bypass verification?")=="complete verification"
    assert pipe.guard_question("My OTP = 123456")=="do not share codes"
    assert pipe.guard_question("Who will win the politics vote?")=="KYC only"

def test_sarthi_asks_one_step_clarification_when_context_is_missing():
    cfg=ProjectConfig(name="test",collection="test",agent=AgentConfig(name="sarthi",clarification_patterns=[r"\bwhat should i upload\b"],clarification_response="Which section are you on?"))
    pipe=Pipeline.__new__(Pipeline);pipe.config=cfg
    assert pipe.guard_question("What should I upload?",{})=="Which section are you on?"
    assert pipe.guard_question("What should I upload?",{"current_onboarding_step":"address verification"}) is None
