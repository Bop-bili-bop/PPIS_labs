:- begin_tests(influenza).

:- use_module(influenza).

test(strong_example, [nondet]) :-
    diagnostic_result(alina, symptoms_consistent_with_influenza_model).

test(mild_example, [nondet]) :-
    diagnostic_result(boris, mild_influenza_like_presentation).

test(insufficient_example, [nondet]) :-
    diagnostic_result(vira, insufficient_evidence).

test(high_temperature_is_inferred, [nondet]) :-
    finding(alina, very_high_temperature).

test(fever_duration_in_assignment_range) :-
    finding(alina, usual_fever_period).

test(backtracking_over_patterns, true(Patterns ==
     [characteristic_headache_frontal, fever_with_chills,
      fever_headache_weakness, systemic_aches])) :-
    findall(Pattern, evidence_pattern(alina, Pattern), Patterns).

test(no_false_strong_conclusion, [fail]) :-
    diagnostic_result(vira, symptoms_consistent_with_influenza_model).

:- end_tests(influenza).
