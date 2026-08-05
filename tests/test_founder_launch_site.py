from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE_DIR = ROOT / "site"


def read_site_file(name: str) -> str:
    return (SITE_DIR / name).read_text()


def test_landing_page_has_required_public_positioning():
    html = read_site_file("index.html")

    assert "Local Media Downloader & Organizer" in html
    assert "Save media locally. Keep it organized." in html
    assert "No source media upload is required" in html
    assert "macOS" in html
    assert "Windows" in html


def test_landing_page_links_required_public_pages():
    html = read_site_file("index.html")

    for href in ["privacy.html", "eula.html", "refund.html", "limitations.html", "support.html"]:
        assert f'href="./{href}"' in html


def test_landing_page_has_visible_beta_download_ctas_without_checkout():
    html = read_site_file("index.html")

    assert "Join the beta" in html
    assert "Check releases" in html
    assert "Follow progress" in html
    assert "Checkout and license activation are not connected yet." in html
    assert "checkout" not in html.lower().replace("checkout and license activation are not connected yet.", "")


def test_landing_page_has_required_limitations_and_no_udemy_claim():
    html = read_site_file("index.html")

    assert "Source support is best-effort" in html
    assert "does not bypass" in html
    for risky_claim in ["downloads everything", "works with every website", "download any paid course", "Udemy"]:
        assert risky_claim not in html


def test_public_subpages_exist_with_core_copy():
    expected = {
        "privacy.html": "Local-first by design.",
        "eula.html": "Use only media you have rights to process.",
        "refund.html": "A simple beta refund policy.",
        "limitations.html": "Best-effort source support.",
        "support.html": "Help without exposing private data.",
    }

    for name, text in expected.items():
        assert (SITE_DIR / name).is_file()
        assert text in read_site_file(name)


def test_commercial_block_11_docs_exist():
    docs = [
        "COMMERCIAL_BLOCK_11_FOUNDER_LAUNCH_SURFACE.md",
        "FOUNDER_LAUNCH_SITE_COPY.md",
        "BETA_ONBOARDING_COPY.md",
        "PRICING_AND_PLANS.md",
        "SUPPORT_PAGE_DRAFT.md",
    ]

    for doc in docs:
        assert (ROOT / "docs" / doc).is_file()
