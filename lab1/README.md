# №1 — Prolog, варіант 6 «Грип»

[Повний звіт із кодом, даними та результатами](REPORT.md).

З кореня репозиторію:

```bash
swipl -q -s lab1/influenza.pl
swipl -q -g run_tests -t halt lab1/test_influenza.pl
```

Запити у Prolog:

```prolog
diagnostic_result(alina, R).
diagnostic_result(boris, R).
diagnostic_result(vira, R).
diagnostic_result(Patient, Result).
evidence_pattern(alina, Pattern).
severity(alina, Severity).
```

Спостереження завантажуються з `observations.pl`. Нові приклади додаються
фактами `temperature/2`, `fever_duration/2`, `observation/2` у цьому файлі.
Висновки демонстрацій: відповідність моделі, легка картина, недостатньо даних.
Правила навчальні та використовують припущення, описані у звіті.
