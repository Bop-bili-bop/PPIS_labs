from src.app import app


def test_index_works_without_gemini_key(monkeypatch) -> None:
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    app.config.update(TESTING=True)
    response = app.test_client().get("/")
    assert response.status_code == 200
    assert "Лабораторна №5" in response.get_data(as_text=True)
    assert "Gemini не налаштовано" in response.get_data(as_text=True)


def test_analysis_route() -> None:
    app.config.update(TESTING=True)
    response = app.test_client().post("/analyze", data={"category": "A"})
    assert response.status_code == 200
    assert "526.67" in response.get_data(as_text=True)
