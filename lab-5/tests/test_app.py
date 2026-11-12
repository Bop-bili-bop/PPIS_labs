from src.app import app


def test_index_works_without_openai_key(monkeypatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    app.config.update(TESTING=True)
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert "Лабораторна №5" in response.get_data(as_text=True)
    assert "OpenAI не налаштовано" in response.get_data(as_text=True)


def test_analysis_route() -> None:
    app.config.update(TESTING=True)
    response = app.test_client().post("/analyze", data={"category": "A"})
    assert response.status_code == 200
    assert "526.67" in response.get_data(as_text=True)


def test_analysis_unknown_category():
    response = app.test_client().post('/analyze', data={'category': 'missing'})
    assert response.status_code == 400
    assert 'No rows' in response.get_data(as_text=True)


def test_scrape_route_uses_parser(monkeypatch):
    from src import app as module
    monkeypatch.setattr(module, 'get_headings', lambda url: [
        {'level': 'h1', 'text': '<script>alert(1)</script>'}])
    response = app.test_client().post('/scrape', data={'url': 'https://example.com'})
    assert response.status_code == 200
    text = response.get_data(as_text=True)
    assert '&lt;script&gt;' in text and '<script>alert' not in text


def test_scrape_invalid_url():
    response = app.test_client().post('/scrape', data={'url': 'file:///etc/passwd'})
    assert response.status_code == 400
