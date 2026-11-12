"""Run actual CLIPS rules through clipspy (the CLIPS C engine)."""
from pathlib import Path
import clips


def main():
    env = clips.Environment()
    env.load(str(Path(__file__).with_name('influenza.clp')))
    env.eval('(watch rules)')
    for name in ('strong', 'mild', 'insufficient'):
        env.eval(f'(run-scenario {name})')
        results = [f for f in env.facts() if f.template.name == 'diagnostic-result']
        assert len(results) == 1
        expected = {'strong': 'consistent-with-influenza-model',
                    'mild': 'mild-influenza-like-presentation',
                    'insufficient': 'insufficient-evidence'}[name]
        assert str(results[0]['conclusion']) == expected
    print('PASS: 3 CLIPS demonstration scenarios', flush=True)


if __name__ == '__main__':
    main()
