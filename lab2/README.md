# №2 — Common Lisp, варіант 6 «Грип»

[Повний звіт](REPORT.md) · [Двійкове дерево SVG](influenza_tree.svg).

Інтерактивний запуск із кореня репозиторію:

```bash
sbcl --load lab2/influenza_tree.lisp --eval '(influenza-tree:diagnose-interactively)'
```

Сценарії та графічний експорт:

```bash
sbcl --noinform --non-interactive --load lab2/influenza_tree.lisp --eval '(influenza-tree:run-test-scenarios)'
sbcl --noinform --non-interactive --load lab2/influenza_tree.lisp --eval '(influenza-tree::export-dot)'
dot -Tsvg lab2/influenza_tree.dot -o lab2/influenza_tree.svg
```

Детермінований виклик у Lisp:

```lisp
(influenza-tree:diagnose-with-answers
 '((:acute-onset . t) (:elevated-temperature . t)
   (:general-weakness . t) (:chills . t) (:aches . t)))
```

Потрібні відповіді лише для досягнутих вузлів. Відповідь — T або NIL;
відсутні дані викликають помилку. При роботі з консоллю приймаються yes/y/no/n.
Рішення відповідають тим самим формулам, що у Prolog і CLIPS.
