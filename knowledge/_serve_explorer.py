#!/usr/bin/env python3
"""_serve_explorer.py — SERVE THE REPO SO THE EXPLORER CAN OPEN ITS ARTEFACTS.

  python3 knowledge/_serve_explorer.py

⛔ THE DEFECT THIS EXISTS TO KILL (s280-D2). `notes/_KG-EXPLORER.html` opened by
DOUBLE-CLICKING it runs on the `file://` scheme, and a `file://` page may not read
the file sitting next to it — the browser refuses the scheme, not the path. So the
one thing Dave asked the explorer for — "I want to see any artifact that exists
here, including a render of the actual component snippet" — is impossible from the
disk, for every artefact, forever. The page therefore has a SERVED mode, and a
served mode with no command to run is a instruction to invent one. This is the
command. The explorer's own `file://` banner names this file by name.

WHAT IT DOES, and nothing else:
  * serves the REPO ROOT (the parent of knowledge/) read-only over HTTP,
  * binds 127.0.0.1 ONLY — never a LAN interface,
  * takes a free port from the OS (or --port),
  * prints the explorer's URL and waits. Ctrl-C stops it.

WHAT IT DOES NOT DO, deliberately:
  * it opens NO browser (a lane driving this headless does not want a window, and
    a webbrowser.open() on a headless box writes an error nobody can act on),
  * it has NO dependencies — stdlib only, so it runs wherever python3 does,
  * it WRITES NOTHING: GET and HEAD only; every other method is refused 405.

CONSUMER (named, because an instrument without a consumer is a zombie):
Dave, opening the explorer; and every lane driver that inspects an artefact.
"""
import argparse
import contextlib
import functools
import http.server
import os
import socket
import socketserver
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = 'notes/_KG-EXPLORER.html'


class Handler(http.server.SimpleHTTPRequestHandler):
    """SimpleHTTPRequestHandler, read-only and quiet-ish, rooted at the repo."""

    def do_POST(self): self.send_error(405, "this server reads; it does not write")
    def do_PUT(self): self.send_error(405, "this server reads; it does not write")
    def do_DELETE(self): self.send_error(405, "this server reads; it does not write")

    def end_headers(self):
        # the explorer fetches its artefacts with cache:'no-store'; say the same here
        # so a rebuilt page is never read out of a stale cache.
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, fmt, *args):
        if os.environ.get('SERVE_EXPLORER_QUIET'):
            return
        sys.stderr.write("  %s\n" % (fmt % args))


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def free_port():
    with contextlib.closing(socket.socket()) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--port', type=int, default=0,
                    help="a port to bind (default: one the OS says is free)")
    ap.add_argument('--print-url-only', action='store_true',
                    help="print the URL and exit — for a driver that starts the "
                         "server itself; nothing is served")
    a = ap.parse_args(argv)

    port = a.port or free_port()
    url = 'http://127.0.0.1:%d/%s' % (port, PAGE)
    if a.print_url_only:
        print(url)
        return 0

    if not os.path.exists(os.path.join(ROOT, PAGE)):
        sys.stderr.write("⛔ %s is not in this repo — build it with "
                         "`python3 knowledge/_build_kg_explorer.py` first.\n" % PAGE)
        return 2

    handler = functools.partial(Handler, directory=ROOT)
    try:
        httpd = Server(('127.0.0.1', port), handler)
    except OSError as e:
        sys.stderr.write("⛔ could not bind 127.0.0.1:%d — %s\n"
                         "   run it again without --port and the OS picks a free one.\n"
                         % (port, e))
        return 2

    print("KG EXPLORER — served from %s" % ROOT)
    print("")
    print("    %s" % url)
    print("")
    print("Open that in a browser. Served like this, INSPECT opens the artefact itself —")
    print("a component's snippet renders, a guideline's markdown reads, an icon draws.")
    print("Ctrl-C stops the server. It binds 127.0.0.1 only and never writes.")
    sys.stdout.flush()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped.")
    finally:
        httpd.server_close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
