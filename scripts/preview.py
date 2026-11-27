"""Serve the static build in content/_build/html locally."""

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HTML_DIR = Path(__file__).resolve().parent.parent / "content" / "_build" / "html"
PORT = 8000


class PreviewHandler(SimpleHTTPRequestHandler):
    # The Windows registry can map .mjs to text/plain, which browsers won't import
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".mjs": "text/javascript",
    }

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


def main() -> None:
    handler = partial(PreviewHandler, directory=HTML_DIR)

    with ThreadingHTTPServer(("127.0.0.1", PORT), handler) as server:
        print(f"Serving {HTML_DIR} at http://localhost:{PORT}")
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()