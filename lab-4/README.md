# Лабораторна робота №4 — Python, Gemini API та LCS

Робота використовує офіційний пакет `google-genai`, а не OpenAI. Ключ ніколи
не записується в код або Git.

## Встановлення (Python 3.11+)

```bash
cd lab-4
python -m venv .venv
```

macOS/Linux: `source .venv/bin/activate`  
Windows PowerShell: `.venv\Scripts\Activate.ps1`

```bash
python -m pip install -r requirements.txt
```

## Gemini та чат-бот

```bash
cp .env.example .env       # Windows: copy .env.example .env
# Відредагуйте .env і замініть лише значення GEMINI_API_KEY
python -m src.chatbot
```

Без ключа програма пояснює налаштування і завершується без traceback. Модель
за замовчуванням задається змінною `GEMINI_MODEL=gemini-2.5-flash`.

## LCS і тести

```bash
python -m src.lcs ABCBDAB BDCABA
pytest -q
```

LCS може мати декілька правильних відповідей однакової довжини. Тести
перевіряють довжину та належність підпослідовності обом вхідним рядкам.
Підготовлений запит до Gemini є в `prompts/algorithm-generation-prompt.txt`;
збережених вигаданих відповідей API немає.
