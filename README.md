# ПІІС — лабораторні роботи №1, №2, №3, №4–5

Варіант №6 **«Грип»** для №1–3. Для №4–5 збережено алгоритм **LCS** з
початкового репозиторію та прикладу методички: окремий список варіантів №4–5
у наданому PDF відсутній. Реалізації — навчальні моделі за текстом завдання.

| № | Реалізація | Звіт |
|---|---|---|
| 1 | [Prolog: база знань](lab1/README.md), зовнішні дані | [REPORT](lab1/REPORT.md) |
| 2 | [Common Lisp: двійкове дерево](lab2/README.md), [схема](lab2/influenza_tree.svg) | [REPORT](lab2/REPORT.md) |
| 3 | [CLIPS: продукційні правила](lab3/README.md), трасування активацій | [REPORT](lab3/REPORT.md) |
| 4–5 | [Python: OpenAI, LCS, парсинг, pandas і Flask](lab-4-5/README.md) | [Єдиний звіт](lab-4-5/REPORT.md) |

Кожен звіт містить завдання, пояснення, текст програм, результати та висновки.
Скріншоти журналів знаходяться в `screenshots/`, початкові журнали — у
`results/`. У №4–5 додано скріншоти справжнього Flask-застосунку в Chromium.

## Встановлення

Потрібні Python 3.11+, SWI-Prolog і SBCL. На Ubuntu/Debian:

```bash
sudo apt-get install python3-venv swi-prolog-nox sbcl graphviz
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

CLIPS запускається через **clipspy**, який використовує справжній C engine
CLIPS; окремий консольний `clips` не потрібний. Його також можна використати
для `lab3/run_all.clp`.

## Запуск усіх робіт і тестів

Команди з кореня репозиторію:

```bash
python scripts/verify_all.py
```

Скрипт зупиняється при помилці та зберігає stdout/stderr кожного запуску.
Скрипт не виконує платних AI-запитів. `--skip-network` пропускає публічний HTTP-запит. Публічний запит до example.com потребує
мережі; додатковий локальний HTTP-приклад парсера працює незалежно від сайту.
Для нестандартного встановлення можна задати `SWIPL`, `SBCL`, `SBCL_CORE`.

Окремі команди:

```bash
swipl -q -g run_tests -t halt lab1/test_influenza.pl
sbcl --noinform --non-interactive --load lab2/influenza_tree.lisp --eval '(influenza-tree:run-test-scenarios)'
python lab3/run.py
python scripts/check_models.py
(cd lab-4-5 && python -m pytest -q)
(cd lab-4-5 && python -m src.app)
```

Лабораторна №4–5 має один пакет `src`, один набір залежностей та спільний запуск pytest.

## Перевірені результати — 12.11.2026

- Prolog: **9 тестів**.
- Lisp: **3 сценарії** та інтерактивний обхід з повтором некоректного вводу.
- CLIPS: **3 сценарії**, вихідні факти та трасування `FIRE`.
- Спільна модель: **6144 набори × 3 середовища = 18432 узгоджених висновки**.
- Python: **30 тестів єдиної лабораторної №4–5**.
- LCS `ABCBDAB` / `BDCABA`: довжина **4**.
- CSV категорії A: **3 рядки**, середня ціна **526.67**.
- Flask: запуск сервера й обох форм через реальні HTTP-запити в Chromium.

## OpenAI API

У №4–5 реалізовано OpenAI Responses API відповідно до методички. Ключ та
модель задаються в `lab-4-5/.env` або змінних `OPENAI_API_KEY`, `OPENAI_MODEL`.
Інструкції: [лабораторна №4–5](lab-4-5/README.md).

**Живий OpenAI API-запит і створення ключа не виконано:** облікові дані не
надавалися. Тести з підміною API перевіряють код, але не доступ до сервісу.
Звіти прямо відображають цю межу; вигаданих API-відповідей немає.
Початковий `gemini_client.py` залишено як додатковий приклад; він не потрібний
для виконання робіт, його залежності — у `lab-4-5/requirements-gemini.txt`.

## Оновлення зображень

```bash
python -m pip install -r requirements-evidence.txt
python -m playwright install chromium
python scripts/capture_evidence.py
```

За наявності системного Chrome можна задати `CHROME_PATH` замість завантаження
Chromium. Спочатку виконайте `verify_all.py`. Для схеми Lisp:

```bash
sbcl --noinform --non-interactive --load lab2/influenza_tree.lisp --eval '(influenza-tree::export-dot)'
dot -Tsvg lab2/influenza_tree.dot -o lab2/influenza_tree.svg
```
