#!/usr/bin/env python3
"""Q-67 account-free specimen service; integrate on the existing host only."""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import threading
from urllib.parse import urlsplit

from pipeline import Pipeline, ROOT, Refused, encoded, nonallow


def handler_for(pipeline):
    class Handler(BaseHTTPRequestHandler):
        server_version = "Q67/1"
        def log_message(self, *args):
            pass  # URLs carry unguessable receipt capabilities; do not log them.

        def reply(self, code, body, mime="application/json", download=False):
            if not isinstance(body, bytes):
                body = encoded(body)
            self.send_response(code)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; img-src 'self'; frame-ancestors 'none'; base-uri 'none'; form-action 'self'")
            if download:
                self.send_header("Content-Disposition", 'attachment; filename="framework-suite.zip"')
            self.end_headers()
            self.wfile.write(body)

        def parts(self):
            return urlsplit(self.path).path.strip("/").split("/")

        def do_GET(self):
            parts = self.parts()
            if parts in ([""], ["index.html"]):
                return self.reply(200, (ROOT / "index.html").read_bytes(), "text/html; charset=utf-8")
            if parts in (["app.js"], ["style.css"], ["protocol.html"]):
                mime = {"app.js": "text/javascript", "style.css": "text/css", "protocol.html": "text/html"}[parts[0]]
                return self.reply(200, (ROOT / parts[0]).read_bytes(), mime + "; charset=utf-8")
            if parts == ["api", "status"]:
                return self.reply(200, pipeline.status())
            if parts == ["api", "specimen"]:
                pointer = pipeline.storage / "public-specimen.json"
                if pointer.exists():
                    return self.reply(200, json.loads(pointer.read_bytes()))
                return self.reply(503, nonallow("PUBLIC_SPECIMEN_NOT_PUBLISHED", "public specimen installed", "Existing host owner must publish a labeled specimen through this page, then set its receipt pointer."))
            if len(parts) == 4 and parts[:2] == ["api", "intakes"]:
                try:
                    folder = pipeline.directory_for(parts[2])
                    resource = {"receipt": "receipt.json", "analysis": "analysis.json", "result": "result.json", "bundle": "suite.zip"}.get(parts[3])
                    if resource and (folder / resource).exists():
                        return self.reply(200, (folder / resource).read_bytes(),
                                          "application/zip" if resource == "suite.zip" else "application/json", resource == "suite.zip")
                except FileNotFoundError:
                    pass
            self.reply(404, nonallow("RESOURCE_NOT_FOUND", "resource exists", "Use the retained receipt identifier."))

        def do_POST(self):
            if self.headers.get("Transfer-Encoding"):
                self.close_connection = True
                return self.reply(400, nonallow("INTAKE_INVALID", "bounded Content-Length", "Send bounded JSON with Content-Length."))
            origin = self.headers.get("Origin")
            if origin and urlsplit(origin).netloc != self.headers.get("Host"):
                self.close_connection = True
                return self.reply(403, nonallow("ORIGIN_MISMATCH", "same-origin submission", "Submit through this page or a direct account-free JSON client."))
            if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                self.close_connection = True
                return self.reply(415, nonallow("INTAKE_INVALID", "application/json", "Submit application/json."))
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 65536:
                    self.close_connection = True
                    return self.reply(413, nonallow("INTAKE_TOO_LARGE", "1..65536 bytes", "Reduce the intake to 64 KiB."))
                body = json.loads(self.rfile.read(length))
                parts = self.parts()
                if parts == ["api", "intakes"]:
                    return self.reply(201, pipeline.intake(body))
                if len(parts) == 4 and parts[:2] == ["api", "intakes"] and parts[3] == "build":
                    if not self.server.build_slots.acquire(blocking=False):
                        return self.reply(429, nonallow("CAPACITY_UNAVAILABLE", "build slot available", "Retry this same receipt; no second intake is needed."))
                    try:
                        return self.reply(200, pipeline.run(parts[2]))
                    finally:
                        self.server.build_slots.release()
                return self.reply(404, nonallow("RESOURCE_NOT_FOUND", "route exists", "Use the published API routes."))
            except Refused as error:
                return self.reply(422, error.disposition)
            except FileNotFoundError:
                return self.reply(404, nonallow("RESOURCE_NOT_FOUND", "receipt exists", "Use a retained intake receipt."))
            except (ValueError, TypeError, UnicodeError):
                return self.reply(400, nonallow("INTAKE_INVALID", "valid bounded JSON", "Submit a valid JSON intake."))
            except Exception:
                return self.reply(503, nonallow("BUILD_UNAVAILABLE", "successful bounded build", "Retain your receipt; existing runtime owner must inspect the exact build failure and retry the same receipt."))
    return Handler


class Server(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, address, handler):
        super().__init__(address, handler)
        self.build_slots = threading.BoundedSemaphore(2)
        self.connection_slots = threading.BoundedSemaphore(32)

    def process_request(self, request, address):
        request.settimeout(10)
        if not self.connection_slots.acquire(blocking=False):
            self.shutdown_request(request)
            return
        try:
            super().process_request(request, address)
        except Exception:
            self.connection_slots.release()
            raise

    def process_request_thread(self, request, address):
        try:
            super().process_request_thread(request, address)
        finally:
            self.connection_slots.release()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bind", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8810)
    parser.add_argument("--storage", required=True)
    args = parser.parse_args()
    server = Server((args.bind, args.port), handler_for(Pipeline(Path(args.storage).resolve())))
    print("Q-67 SPECIMEN_ONLY listening on", server.server_address, flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
