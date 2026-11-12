# №3 — CLIPS, варіант 6 «Грип»

[Повний звіт із полем знань, ієрархією, правилами та трасуванням](REPORT.md).

З кореня репозиторію:

```bash
python -m pip install -r requirements.txt
python lab3/run.py
python scripts/check_models.py
```

`clipspy` завантажує справжній рушій CLIPS і виконує `influenza.clp`.
У консолі CLIPS можна використати `clips -f2 lab3/run_all.clp`.

Для власних даних виконайте reset, додайте факти patient/temperature/symptom
та запустіть run. Приклад:

```clips
(load "lab3/influenza.clp")
(reset)
(assert (patient (id example)))
(assert (temperature (patient example) (degrees 37.6)))
(assert (symptom (patient example) (name acute-onset)))
(assert (symptom (patient example) (name general-weakness)))
(assert (symptom (patient example) (name headache)))
(watch rules)
(run)
(show-result)
```

Результат: `mild-influenza-like-presentation`. Дані сценаріїв розділено
через reset. Правила свідчень виконуються перед правилами остаточного висновку.
