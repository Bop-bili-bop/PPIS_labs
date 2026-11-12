"""Submit the saved LCS prompt to OpenAI; never execute generated code."""
from pathlib import Path
from .openai_client import create_client, generate_text


def main() -> int:
    prompt = (Path(__file__).resolve().parents[1] / "prompts" /
              "algorithm-generation-prompt.txt").read_text(encoding="utf-8")
    try:
        client, model = create_client()
        with client:
            print(generate_text(prompt, client=client, model=model))
    except (ValueError, RuntimeError) as exc:
        print(exc)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
