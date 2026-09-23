# Лабораторна робота №5 — парсинг, pandas і Flask

## Встановлення (Python 3.11+)

```bash
cd lab-5
python -m venv .venv
```

macOS/Linux: `source .venv/bin/activate`  
Windows PowerShell: `.venv\Scripts\Activate.ps1`

```bash
python -m pip install -r requirements.txt
```

## Запуск прикладів

```bash
python -m src.web_scraper https://example.com
python -m src.data_analysis
pytest -q
python -m src.app
```

Остання команда запускає сторінку `http://127.0.0.1:5000`. Альтернатива:

```bash
flask --app src.app run --debug
```

`web_scraper` приймає лише абсолютні HTTP(S) URL, використовує User-Agent,
тайм-аут і перевірку HTTP-статусу. Мережа не потрібна тестам: HTML передається
безпосередньо в `parse_headings`.

## Gemini

Методика використовує OpenAI, але в репозиторії обрано Gemini. Ця робота
показує стан налаштування `GEMINI_API_KEY`; її основні можливості не потребують
ключа. За потреби скопіюйте `.env.example` у `.env` та додайте свій ключ.
Локальний `.env` ігнорується Git.
