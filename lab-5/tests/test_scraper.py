import pytest

from src.web_scraper import parse_headings, validate_url

HTML = """
<html><body>
<h1> Main title </h1><p>Text</p>
<h2>Section <span>one</span></h2><h3>Details</h3>
</body></html>
"""


def test_expected_headings_are_extracted_from_static_html() -> None:
    assert parse_headings(HTML) == [
        {"level": "h1", "text": "Main title"},
        {"level": "h2", "text": "Section one"},
        {"level": "h3", "text": "Details"},
    ]


def test_page_without_headings_returns_empty_list() -> None:
    assert parse_headings("<html><p>No headings</p></html>") == []


@pytest.mark.parametrize("url", ["example.com", "ftp://example.com", "", "/local"])
def test_invalid_url_is_rejected(url: str) -> None:
    with pytest.raises(ValueError, match="absolute"):
        validate_url(url)
