"""Reproduce every lab run and save real stdout/stderr (no live AI request)."""
import argparse
from pathlib import Path
import os
import subprocess
import sys
from fixture_server import fixture_server

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def execute(folder, name, command, *, cwd=ROOT, expected=0, env=None, input=None):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True,
                            env=env, input=input)
    transcript = '$ ' + ' '.join(command) + '\n' + result.stdout + result.stderr
    transcript += f'\nExit code: {result.returncode}\n'
    path = ROOT / folder / 'results' / f'{name}.txt'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(transcript, encoding='utf-8')
    print(f'{folder}/{name}: exit {result.returncode}', flush=True)
    if result.returncode != expected:
        raise RuntimeError(transcript)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-network', action='store_true',
                        help='Skip the optional public example.com HTTP request')
    args = parser.parse_args()
    swipl = os.getenv('SWIPL', 'swipl')
    sbcl = [os.getenv('SBCL', 'sbcl')]
    if os.getenv('SBCL_CORE'):
        sbcl += ['--core', os.environ['SBCL_CORE']]
    execute('lab1', 'tests', [swipl, '-q', '-g', 'run_tests', '-t', 'halt',
                              'lab1/test_influenza.pl'])
    execute('lab1', 'demo', [swipl, '-q', '-s', 'lab1/influenza.pl', '-g',
            'forall(diagnostic_result(P,R),format("~w: ~w~n",[P,R]))', '-t', 'halt'])
    execute('lab2', 'demo', sbcl + ['--noinform', '--non-interactive', '--load',
            'lab2/influenza_tree.lisp', '--eval', '(influenza-tree:run-test-scenarios)'])
    execute('lab2', 'interactive', sbcl + ['--noinform', '--non-interactive', '--load',
            'lab2/influenza_tree.lisp', '--eval', '(influenza-tree:diagnose-interactively)'],
            input='invalid\nyes\nyes\nyes\nyes\nyes\n')
    execute('lab3', 'demo', [PYTHON, 'lab3/run.py'])
    execute('lab3', 'cross-model', [PYTHON, 'scripts/check_models.py'])
    for folder in ('lab-4', 'lab-5'):
        execute(folder, 'tests', [PYTHON, '-m', 'pytest', '-q'], cwd=ROOT/folder)
    execute('lab-4', 'demo', [PYTHON, '-m', 'src.lcs', 'ABCBDAB', 'BDCABA'],
            cwd=ROOT/'lab-4')
    env = dict(os.environ, OPENAI_API_KEY='', OPENAI_MODEL='', PYTHON_DOTENV_DISABLED='1')
    execute('lab-4', 'missing-key', [PYTHON, '-m', 'src.chatbot'],
            cwd=ROOT/'lab-4', expected=1, env=env)
    execute('lab-5', 'demo', [PYTHON, '-m', 'src.data_analysis'], cwd=ROOT/'lab-5')
    if not args.skip_network:
        execute('lab-5', 'scraper', [PYTHON, '-m', 'src.web_scraper', 'https://example.com'],
                cwd=ROOT/'lab-5')
    with fixture_server() as url:
        execute('lab-5', 'scraper-fixture', [PYTHON, '-m', 'src.web_scraper', url],
                cwd=ROOT/'lab-5')
    print('PASS: all lab checks. Live OpenAI API: NOT RUN (no credentials supplied).')


if __name__ == '__main__':
    main()
