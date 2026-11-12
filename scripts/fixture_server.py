"""A local HTTP fixture for reproducible parser demonstrations."""
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass


@contextmanager
def fixture_server():
    directory = Path(__file__).resolve().parents[1]/'lab-4-5/data'
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=directory))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}/sample_page.html'
    finally:
        server.shutdown()
        server.server_close()
        thread.join()
