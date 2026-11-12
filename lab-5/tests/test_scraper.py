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


def test_http_download_and_timeout(monkeypatch):
    from src import web_scraper
    from unittest.mock import Mock
    response = Mock(text=HTML, content=HTML.encode(), headers={})
    get = Mock(return_value=response)
    monkeypatch.setattr(web_scraper.requests, 'get', get)
    assert len(web_scraper.get_headings('https://example.com', timeout=2)) == 3
    response.raise_for_status.assert_called_once()
    assert get.call_args.kwargs['timeout'] == 2


def test_network_failure_is_controlled(monkeypatch):
    from src import web_scraper
    from unittest.mock import Mock
    monkeypatch.setattr(web_scraper.requests, 'get', Mock(
        side_effect=web_scraper.requests.Timeout('timed out')))
    with pytest.raises(web_scraper.ScraperError, match='Could not retrieve'):
        web_scraper.get_headings('https://example.com')


def test_utf8_html_meta_charset_survives_download(monkeypatch):
    from src import web_scraper
    from unittest.mock import Mock
    html = '<meta charset="utf-8"><h1>ПІІС: навчальний парсер</h1>'
    response = Mock(text=html.encode().decode('latin1'), content=html.encode(), headers={})
    monkeypatch.setattr(web_scraper.requests, 'get', Mock(return_value=response))
    assert web_scraper.get_headings('https://example.com') == [
        {'level': 'h1', 'text': 'ПІІС: навчальний парсер'}]
