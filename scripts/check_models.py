"""Compare all three real language runtimes over an exhaustive input grid."""
from __future__ import annotations
import itertools
import os
from pathlib import Path
import subprocess
import tempfile

import clips

ROOT = Path(__file__).resolve().parents[1]
SYMPTOMS = ['acute_onset', 'chills', 'general_weakness', 'muscle_pain',
            'joint_pain', 'body_aches', 'headache', 'frontal_headache',
            'pain_behind_eyes', 'headache_worse_with_eye_movement']
TEMPERATURES = [37.0, 37.1, 37.99, 38.0, 39.49, 39.5]
PROLOG_LABELS = ['insufficient_evidence', 'mild_influenza_like_presentation',
                 'symptoms_consistent_with_influenza_model']
CLIPS_LABELS = ['insufficient-evidence', 'mild-influenza-like-presentation',
                'consistent-with-influenza-model']
LISP_LABELS = ['INSUFFICIENT', 'MILD', 'CONSISTENT']


def expected(temp, signs):
    s = set(signs)
    if 'acute_onset' not in s or temp < 37.1 or 'general_weakness' not in s:
        return 0
    if ('chills' in s and s.intersection({'muscle_pain', 'joint_pain', 'body_aches'})
        or 'headache_worse_with_eye_movement' in s
        and s.intersection({'frontal_headache', 'pain_behind_eyes'})):
        return 2
    return int(temp < 38.0 and bool(s.intersection({'headache', 'body_aches'})))


def run(command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stdout + result.stderr)
    return result.stdout.splitlines()


def main():
    cases = [(temp, [s for s, yes in zip(SYMPTOMS, flags) if yes])
             for temp in TEMPERATURES
             for flags in itertools.product([False, True], repeat=len(SYMPTOMS))]
    want = [expected(temp, signs) for temp, signs in cases]
    with tempfile.TemporaryDirectory() as tmp:
        prolog = Path(tmp) / 'cases.pl'
        # A single patient per case avoids O(number_of_cases^2) enumeration.
        prolog.write_text(":- use_module('" + (ROOT/'lab1/influenza.pl').as_posix() + "').\n"
            + ":- use_module(library(lists)).\ncase(T, S) :- retractall(influenza:observation(p, _)), "
              "retractall(influenza:temperature(p, _)), "
              "assertz(influenza:temperature(p, T)), "
              "forall(member(X,S),assertz(influenza:observation(p,X))), "
              "findall(R,diagnostic_result(p,R),[Result]), writeln(Result).\n"
            + ":- initialization(main, main).\nmain :-\n"
            + ',\n'.join(f"case({temp}, [{','.join(signs)}])" for temp, signs in cases)
            + '.\n')
        actual = run([os.getenv('SWIPL', 'swipl'), '-q', '-s', str(prolog)])
        assert actual == [PROLOG_LABELS[i] for i in want], 'Prolog mismatch'
        lisp = Path(tmp) / 'cases.lisp'
        lines = ['(load "lab2/influenza_tree.lisp")']
        for temp, signs in cases:
            answers = {':acute-onset': 'acute_onset' in signs,
                       ':elevated-temperature': temp >= 37.1,
                       ':subfebrile': 37.1 <= temp < 38,
                       ':general-weakness': 'general_weakness' in signs,
                       ':chills': 'chills' in signs,
                       ':aches': bool(set(signs) & {'muscle_pain','joint_pain','body_aches'}),
                       ':body-aches': 'body_aches' in signs,
                       ':headache': 'headache' in signs,
                       ':frontal-headache': 'frontal_headache' in signs,
                       ':pain-behind-eyes': 'pain_behind_eyes' in signs,
                       ':eye-movement': 'headache_worse_with_eye_movement' in signs}
            alist = ' '.join(f'({key} . {"t" if value else "nil"})'
                             for key, value in answers.items())
            lines.append('(format t "~A~%" (influenza-tree::conclusion-id '
                         f"(influenza-tree:diagnose-with-answers '({alist}))))")
        lisp.write_text('\n'.join(lines))
        command = [os.getenv('SBCL', 'sbcl')]
        if os.getenv('SBCL_CORE'):
            command += ['--core', os.environ['SBCL_CORE']]
        actual = run(command + ['--script', str(lisp)])
        assert actual == [LISP_LABELS[i] for i in want], 'Lisp mismatch'
    env = clips.Environment()
    env.load(str(ROOT/'lab3/influenza.clp'))
    for index, (temp, signs) in enumerate(cases):
        env.reset()
        env.assert_string('(patient (id p))')
        env.assert_string(f'(temperature (patient p) (degrees {temp}))')
        for sign in signs:
            name = sign.replace('_', '-')
            if sign == 'headache_worse_with_eye_movement':
                name = 'eye-movement-worsens-headache'
            env.assert_string(f'(symptom (patient p) (name {name}))')
        env.run()
        labels = [str(f['conclusion']) for f in env.facts()
                  if f.template.name == 'diagnostic-result']
        assert labels == [CLIPS_LABELS[want[index]]], (temp, signs, labels)
    print(f'PASS: {len(cases)} input cases x 3 runtimes = {len(cases)*3} conclusions.')
    print('Includes 37.0 / 37.1 / 37.99 / 38.0 / 39.49 / 39.5 C boundaries.')


if __name__ == '__main__':
    main()
