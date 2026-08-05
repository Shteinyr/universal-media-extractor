from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_doc(name: str) -> str:
    return (ROOT / "docs" / name).read_text(encoding="utf-8")


def test_lemon_squeezy_preapproval_doc_keeps_checkout_out_of_scope() -> None:
    text = read_doc("LEMON_SQUEEZY_PREAPPROVAL_REQUEST.md")

    assert "Universal Media Extractor" in text
    assert "does not bypass DRM" in text
    assert "does not store user passwords, cookies, or tokens" in text
    assert "Udemy Course Mode" in text
    assert "hidden from public commercial builds" in text


def test_stripe_fallback_review_names_ip_and_cyberlocker_risks() -> None:
    text = read_doc("STRIPE_FALLBACK_RISK_REVIEW.md")

    assert "Stripe is a fallback path only" in text
    assert "Intellectual property facilitation" in text
    assert "Cyberlocker" in text
    assert "Do not integrate Stripe checkout" in text


def test_licensing_model_covers_required_entitlement_rules() -> None:
    text = read_doc("LICENSING_MODEL_DRAFT.md")

    assert "3 active devices" in text
    assert "Offline Entitlement" in text
    assert "30 days grace" in text
    assert "Deactivate Device" in text
    assert "last eligible version" in text
    assert "No license server" in text


def test_user_decisions_doc_blocks_real_payment_integration() -> None:
    text = read_doc("PAYMENT_LICENSING_USER_DECISIONS.md")

    assert "Provider Decisions" in text
    assert "Business Details Needed" in text
    assert "Do not implement checkout" in text
    assert "provider approval" in text


def test_block_12_summary_links_payment_and_licensing_docs() -> None:
    text = read_doc("COMMERCIAL_BLOCK_12_PAYMENT_LICENSING_PREP.md")

    assert "#22" in text
    assert "#23" in text
    assert "LEMON_SQUEEZY_PREAPPROVAL_REQUEST.md" in text
    assert "STRIPE_FALLBACK_RISK_REVIEW.md" in text
    assert "LICENSING_MODEL_DRAFT.md" in text
    assert "No checkout" in text
