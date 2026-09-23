# Лабораторная работа 1 — Prolog

**Вариант 6: «Грип»**

`influenza.pl` — небольшая учебная база знаний на совместимом с SWI-Prolog
синтаксисе. Она не является медицинским диагностическим средством. Модель
ограничена признаками из задания: острым началом, температурой, ознобом,
характерной головной болью, слабостью, ломотой и глазными проявлениями.

## Структура модели

- `symptom/1` и `symptom_group/2` задают словарь и отношения предметной области;
- `observation/2`, `temperature/2`, `fever_duration/2` содержат исходные данные;
- `finding/2` выводит температурные категории и обычный период лихорадки;
- `evidence_pattern/2` распознаёт несколько независимых сочетаний признаков;
- `severity/2` отделяет лёгкую, выраженную и тяжёлую картину;
- `diagnostic_result/2` возвращает одно из трёх **учебных** заключений.

В примерах `alina` имеет сильное соответствие модели, `boris` — лёгкую
гриппоподобную картину, а для `vira` данных недостаточно. Отсутствующий факт не
означает клиническое отрицание; лишь резервное правило использует принятое в
Prolog предположение о замкнутом мире.

## Запуск и запросы

```bash
swipl -q -s lab1/influenza.pl
```

Примеры запросов в интерактивной консоли:

```prolog
?- diagnostic_result(alina, Result).
Result = symptoms_consistent_with_influenza_model ; ...

?- diagnostic_result(boris, Result).
Result = mild_influenza_like_presentation.

?- diagnostic_result(vira, Result).
Result = insufficient_evidence.

?- evidence_pattern(alina, Pattern).
Pattern = characteristic_headache_frontal ;
Pattern = fever_with_chills ;
Pattern = fever_headache_weakness ;
Pattern = systemic_aches.

?- severity(alina, Severity).
Severity = pronounced.
```

Последний запрос к `evidence_pattern/2` демонстрирует поиск с возвратом. Нового
пациента можно добавить фактами `observation/2`, `temperature/2` и, при наличии
данных, `fever_duration/2`.

Автоматическая проверка:

```bash
swipl -q -g run_tests -t halt lab1/test_influenza.pl
```
