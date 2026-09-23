import http.server, json, sys, os, time
OUT = sys.argv[2]
class H(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get('content-length', 0))
        body = self.rfile.read(n)
        fn = os.path.join(OUT, f"req-{time.time():.6f}.json")
        open(fn, 'wb').write(body)
        with open(os.path.join(OUT, "paths.log"), "a") as f: f.write(self.path + "\n")
        msg = json.dumps({"type":"error","error":{"type":"invalid_request_error","message":"captured by lane B"}}).encode()
        self.send_response(400); self.send_header('content-type','application/json'); self.send_header('content-length', str(len(msg))); self.end_headers(); self.wfile.write(msg)
    def do_GET(self):
        with open(os.path.join(OUT, "paths.log"), "a") as f: f.write("GET " + self.path + "\n")
        msg = b"{}"
        self.send_response(404); self.send_header('content-length', str(len(msg))); self.end_headers(); self.wfile.write(msg)
    def log_message(self, *a): pass
http.server.HTTPServer(('127.0.0.1', int(sys.argv[1])), H).serve_forever()
