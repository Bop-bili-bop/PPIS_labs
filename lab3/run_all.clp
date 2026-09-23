; Run with: clips -f2 lab3/run_all.clp
(load "lab3/influenza.clp")
(watch rules)
(run-scenario strong)
(run-scenario mild)
(run-scenario insufficient)
(unwatch rules)
(exit)
