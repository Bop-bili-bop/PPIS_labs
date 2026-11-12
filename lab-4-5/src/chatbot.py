"""Console ChatGPT/OpenAI chatbot with conversation history."""
from __future__ import annotations

try:
    from .openai_client import OpenAIConfigurationError, create_client, generate_text
except ImportError:  # python src/chatbot.py
    from openai_client import OpenAIConfigurationError, create_client, generate_text


def main() -> int:
    print("OpenAI chatbot. Type 'exit' or 'quit' to finish.")
    try:
        client, model = create_client()
    except OpenAIConfigurationError as exc:
        print(exc)
        return 1
    history: list[dict[str, str]] = []
    with client:
        while True:
            try:
                message = input("\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nGoodbye!")
                return 0
            if message.lower() in {"exit", "quit"}:
                print("Goodbye!")
                return 0
            if not message:
                print("Please enter a message.")
                continue
            try:
                print("Assistant:", generate_text(message, client=client,
                                                   model=model, history=history))
            except (ValueError, RuntimeError) as exc:
                print(exc)


if __name__ == "__main__":
    raise SystemExit(main())
