#!/usr/bin/env python3
# Capture-side listener: logs method/path/headers/body from any OpenAI SDK client
# redirected via OPENAI_BASE_URL. Returns a minimal valid chat.completion.
import json, sys, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

LOG = sys.argv[1] if len(sys.argv) > 1 else "listener.log"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8899

class H(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    def _handle(self):
        n = int(self.headers.get("Content-Length", "0") or 0)
        body = self.rfile.read(n) if n else b""
        rec = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "from": f"{self.client_address[0]}:{self.client_address[1]}",
            "method": self.command,
            "path": self.path,
            "authorization": self.headers.get("Authorization", ""),
            "user_agent": self.headers.get("User-Agent", ""),
            "body": body.decode("utf-8", "replace")[:4000],
        }
        with open(LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
        resp = json.dumps({
            "id": "chatcmpl-x", "object": "chat.completion", "created": 0,
            "model": "gpt-4o",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "{}"},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)
    do_GET = _handle
    do_POST = _handle
    def log_message(self, *a): pass

ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
