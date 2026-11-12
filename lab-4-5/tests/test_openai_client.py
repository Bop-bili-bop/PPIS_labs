from types import SimpleNamespace
from unittest.mock import Mock

import pytest
from openai import OpenAIError
from src import openai_client
from src import chatbot


def fake_client(text="answer"):
    client = Mock()
    client.responses.create.return_value = SimpleNamespace(output_text=text)
    return client


def test_history_and_responses_request():
    client = fake_client()
    history = []
    assert openai_client.generate_text("first", client=client, model="test-model",
                                       history=history) == "answer"
    assert len(history) == 2
    openai_client.generate_text("second", client=client, model="test-model", history=history)
    assert client.responses.create.call_args.kwargs == {
        "model": "test-model", "store": False,
        "input": [{"role": "user", "content": "first"},
                  {"role": "assistant", "content": "answer"},
                  {"role": "user", "content": "second"}],
    }
    assert len(history) == 4


def test_failed_turn_does_not_change_history_or_expose_secret():
    client = fake_client()
    client.responses.create.side_effect = OpenAIError("secret-key-do-not-show")
    history = []
    with pytest.raises(RuntimeError) as error:
        openai_client.generate_text("hello", client=client, model="test", history=history)
    assert "secret-key" not in str(error.value)
    assert history == []


@pytest.mark.parametrize("text", ["", "   "])
def test_empty_response(text):
    with pytest.raises(RuntimeError, match="empty"):
        openai_client.generate_text("hello", client=fake_client(text), model="test")


def test_empty_prompt_never_calls_api():
    client = fake_client()
    with pytest.raises(ValueError, match="empty"):
        openai_client.generate_text("  ", client=client, model="test")
    client.responses.create.assert_not_called()


def test_missing_settings(monkeypatch):
    monkeypatch.setattr(openai_client, "load_dotenv", lambda *_: None)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)
    with pytest.raises(openai_client.OpenAIConfigurationError):
        openai_client.create_client()


def test_chat_loop_retries_and_exits(monkeypatch, capsys):
    client = Mock()
    client.__enter__ = Mock(return_value=client)
    client.__exit__ = Mock(return_value=False)
    monkeypatch.setattr(chatbot, "create_client", lambda: (client, "test"))
    generate = Mock(side_effect=[RuntimeError("temporary failure"), "OK"])
    monkeypatch.setattr(chatbot, "generate_text", generate)
    answers = iter(["", "first", "second", "quit"])
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    assert chatbot.main() == 0
    output = capsys.readouterr().out
    assert "temporary failure" in output and "OK" in output and "Goodbye" in output
    assert generate.call_count == 2
