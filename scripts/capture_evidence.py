"""Screenshot the saved run logs and a live Flask server. Requires playwright.

These are browser screenshots of a transcript viewer, not fabricated terminals.
Run verify_all.py first. Source logs remain alongside every screenshot.
"""
from html import escape
from pathlib import Path
import subprocess
import sys
import time
from fixture_server import fixture_server
from urllib.request import urlopen
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]


def main():
    with sync_playwright() as p:
        # Set CHROME_PATH to use an installed browser; otherwise use Playwright's.
        import os
        options = {'headless': True}
        if os.getenv('CHROME_PATH'):
            options['executable_path'] = os.environ['CHROME_PATH']
        browser = p.chromium.launch(**options)
        page = browser.new_page(viewport={'width': 1440, 'height': 1000}, device_scale_factor=1)
        for folder, names in [('lab1', ['demo', 'tests']),
                              ('lab2', ['demo', 'interactive']),
                              ('lab3', ['demo', 'cross-model']),
                              ('lab-4', ['demo', 'tests', 'missing-key']),
                              ('lab-5', ['demo', 'scraper', 'scraper-fixture', 'tests'])]:
            out = ROOT/folder/'screenshots'
            out.mkdir(exist_ok=True)
            for name in names:
                log = (ROOT/folder/'results'/f'{name}.txt').read_text()
                page.set_content('<meta charset="utf-8"><style>'
                    'body{margin:36px;background:#101827;color:#e5eefb;font:18px monospace}'
                    'h1{font:26px sans-serif;color:#80c8ff}'
                    'p{font:17px sans-serif;color:#a8b6cc}'
                    'pre{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.5}'
                    '</style>' + f'<h1>ПІІС · {escape(folder)} · {escape(name)}</h1>'
                    '<p>Фактичний журнал виконання · 12.11.2026 · перегляд збереженого stdout/stderr</p>'
                    f'<pre>{escape(log)}</pre>')
                page.screenshot(path=str(out/f'{name}.png'), full_page=True)
        server = subprocess.Popen([sys.executable, '-m', 'flask', '--app', 'src.app',
                                   'run', '--host', '127.0.0.1', '--port', '5055'],
                                  cwd=ROOT/'lab-5', stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL)
        try:
            for _ in range(60):
                try:
                    with urlopen('http://127.0.0.1:5055', timeout=1) as response:
                        assert response.status == 200
                    break
                except OSError:
                    time.sleep(.2)
            else:
                raise RuntimeError('Flask server did not start')
            page.goto('http://127.0.0.1:5055')
            page.get_by_role('button', name='Обчислити середню ціну').click()
            page.get_by_text('Рядків: 3; середня ціна: 526.67').wait_for()
            page.screenshot(path=str(ROOT/'lab-5/screenshots/flask-analysis.png'), full_page=True)
            with fixture_server() as url:
                page.get_by_label('Абсолютна HTTP(S)-адреса').fill(url)
                page.get_by_role('button', name='Отримати заголовки').click()
                page.get_by_text('ПІІС: навчальний парсер', exact=False).wait_for()
                page.screenshot(path=str(ROOT/'lab-5/screenshots/flask-scraper.png'), full_page=True)
                (ROOT/'lab-5/results/http.txt').write_text(
                    'Real HTTP server: http://127.0.0.1:5055\n'
                    'GET / -> 200\nPOST /analyze category=A -> 200; 3 rows; mean 526.67\n'
                    f'POST /scrape {url} -> 200; 3 headings from local HTTP fixture\n')
        finally:
            server.terminate()
            server.wait(timeout=10)
        browser.close()
    print('PASS: transcript screenshots and live Flask screenshots saved.')


if __name__ == '__main__':
    main()
