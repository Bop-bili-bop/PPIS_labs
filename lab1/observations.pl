% Observations loaded from disk; replace these facts for another data set.
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

