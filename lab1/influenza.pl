/** <module> Educational influenza knowledge base (Variant 6).

This program models only the symptom description supplied for the laboratory
assignment.  Its conclusions are labels in a teaching example, not medical
diagnoses.  Missing observations are treated as unknown (and, for the final
fallback conclusion, as absent under Prolog's closed-world assumption).
*/

:- module(influenza,
          [ observation/2,
            symptom/1,
            symptom_group/2,
            temperature/2,
            fever_duration/2,
            finding/2,
            evidence_pattern/2,
            severity/2,
            diagnostic_result/2
          ]).

:- discontiguous observation/2, temperature/2, fever_duration/2.

% Domain vocabulary: these facts make the modeled relationships explicit.
symptom(acute_onset).
symptom(elevated_temperature).
symptom(very_high_temperature).
symptom(chills).
symptom(headache).
symptom(frontal_headache).
symptom(pain_behind_eyes).
symptom(headache_worse_with_eye_movement).
symptom(general_weakness).
symptom(increased_sweating).
symptom(muscle_pain).
symptom(joint_pain).
symptom(body_aches).
symptom(photophobia).
symptom(conjunctivitis).
symptom(tearing).
symptom(vomiting).
symptom(sleep_disorder).
symptom(hallucinations).
symptom(nervous_system_symptom).
symptom(seizures).

symptom_group(acute_onset, onset).
symptom_group(elevated_temperature, fever).
symptom_group(very_high_temperature, fever).
symptom_group(chills, fever).
symptom_group(headache, headache).
symptom_group(frontal_headache, headache).
symptom_group(pain_behind_eyes, headache).
symptom_group(headache_worse_with_eye_movement, headache).
symptom_group(general_weakness, systemic).
symptom_group(increased_sweating, systemic).
symptom_group(muscle_pain, systemic).
symptom_group(joint_pain, systemic).
symptom_group(body_aches, systemic).
symptom_group(photophobia, ocular).
symptom_group(conjunctivitis, ocular).
symptom_group(tearing, ocular).
symptom_group(vomiting, severe).
symptom_group(sleep_disorder, severe).
symptom_group(hallucinations, severe).
symptom_group(nervous_system_symptom, severe).
symptom_group(seizures, severe).

% Example 1: a symptom combination strongly matching the model.
temperature(alina, 39.8).
fever_duration(alina, 4).
observation(alina, acute_onset).
observation(alina, chills).
observation(alina, frontal_headache).
observation(alina, headache_worse_with_eye_movement).
observation(alina, general_weakness).
observation(alina, muscle_pain).
observation(alina, body_aches).
observation(alina, photophobia).

% Example 2: a mild influenza-like presentation with subfebrile temperature.
temperature(boris, 37.6).
fever_duration(boris, 2).
observation(boris, acute_onset).
observation(boris, headache).
observation(boris, general_weakness).
observation(boris, body_aches).

% Example 3: too few findings to match an influenza pattern.
temperature(vira, 36.7).
observation(vira, tearing).
observation(vira, headache).

% Derived findings demonstrate variables, arithmetic comparison and inference.
finding(Patient, Symptom) :-
    observation(Patient, Symptom),
    symptom(Symptom).
finding(Patient, elevated_temperature) :-
    temperature(Patient, Celsius),
    Celsius >= 37.1.
finding(Patient, subfebrile_temperature) :-
    temperature(Patient, Celsius),
    Celsius >= 37.1,
    Celsius < 38.0.
finding(Patient, very_high_temperature) :-
    temperature(Patient, Celsius),
    Celsius >= 39.5.
finding(Patient, usual_fever_period) :-
    fever_duration(Patient, Days),
    between(2, 6, Days).

% A characteristic headache can be established by either of two combinations;
% asking for Pattern also exposes both alternatives through backtracking.
evidence_pattern(Patient, characteristic_headache_frontal) :-
    finding(Patient, frontal_headache),
    finding(Patient, headache_worse_with_eye_movement).
evidence_pattern(Patient, characteristic_headache_retro_orbital) :-
    finding(Patient, pain_behind_eyes),
    finding(Patient, headache_worse_with_eye_movement).

evidence_pattern(Patient, fever_with_chills) :-
    finding(Patient, elevated_temperature),
    finding(Patient, chills).
evidence_pattern(Patient, fever_headache_weakness) :-
    finding(Patient, elevated_temperature),
    ( finding(Patient, headache)
    ; finding(Patient, frontal_headache)
    ; finding(Patient, pain_behind_eyes)
    ),
    finding(Patient, general_weakness).
evidence_pattern(Patient, systemic_aches) :-
    finding(Patient, general_weakness),
    once(( finding(Patient, muscle_pain)
         ; finding(Patient, joint_pain)
         ; finding(Patient, body_aches)
         )).

% Severity is inferred separately from the diagnostic label.
severity(Patient, severe) :-
    finding(Patient, very_high_temperature),
    ( finding(Patient, vomiting)
    ; finding(Patient, hallucinations)
    ; finding(Patient, nervous_system_symptom)
    ; finding(Patient, seizures)
    ).
severity(Patient, pronounced) :-
    finding(Patient, very_high_temperature),
    evidence_pattern(Patient, systemic_aches),
    \+ severity(Patient, severe).
severity(Patient, mild) :-
    finding(Patient, subfebrile_temperature),
    \+ severity(Patient, pronounced),
    \+ severity(Patient, severe).

% Several independently reusable patterns contribute to the strong conclusion.
strong_influenza_evidence(Patient) :-
    finding(Patient, acute_onset),
    evidence_pattern(Patient, fever_with_chills),
    evidence_pattern(Patient, systemic_aches).
strong_influenza_evidence(Patient) :-
    finding(Patient, acute_onset),
    evidence_pattern(Patient, fever_headache_weakness),
    evidence_pattern(Patient, characteristic_headache_frontal).

mild_influenza_evidence(Patient) :-
    finding(Patient, acute_onset),
    finding(Patient, subfebrile_temperature),
    finding(Patient, general_weakness),
    ( finding(Patient, headache)
    ; finding(Patient, body_aches)
    ).

diagnostic_result(Patient, symptoms_consistent_with_influenza_model) :-
    once(strong_influenza_evidence(Patient)).
diagnostic_result(Patient, mild_influenza_like_presentation) :-
    once(mild_influenza_evidence(Patient)),
    \+ strong_influenza_evidence(Patient).
diagnostic_result(Patient, insufficient_evidence) :-
    known_patient(Patient),
    \+ strong_influenza_evidence(Patient),
    \+ mild_influenza_evidence(Patient).

known_patient(Patient) :- observation(Patient, _).
known_patient(Patient) :- temperature(Patient, _).
