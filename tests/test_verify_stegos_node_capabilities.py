import importlib.util
from email.message import Message
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("observer", ROOT / "scripts/verify_stegos_node_capabilities.py")
observer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(observer)


class Response:
    def __init__(self, request, mode):
        self.url = request.full_url
        path = self.url.removeprefix("https://stegverse.org/")
        self.body = (ROOT / path).read_bytes()
        self.status = 200
        self.headers = Message()
        self.headers["Content-Type"] = "application/json" if path.endswith(".json") else "text/plain"
        if mode == "stale":
            self.body += b"\n"
        elif mode == "html":
            self.headers.replace_header("Content-Type", "text/html")
        elif mode == "redirect":
            self.url = "https://example.invalid/copy"

    def read(self, limit):
        return self.body[:limit]

    def geturl(self):
        return self.url

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


class PublicationObserverTests(unittest.TestCase):
    def run_mode(self, mode):
        def opener(request, timeout):
            self.assertEqual(request.get_method(), "GET")
            self.assertIsNone(request.data)
            return Response(request, mode)
        return observer.observe("https://stegverse.org/", opener=opener)

    def test_exact_bytes_pass_without_claiming_runtime(self):
        report = self.run_mode("exact")
        self.assertEqual(report["result"], "PASS")
        self.assertFalse(report["runtime_health_verified"])
        self.assertFalse(report["node_registration_performed"])

    def test_stale_bytes_html_and_redirects_fail(self):
        for mode in ("stale", "html", "redirect"):
            with self.subTest(mode=mode):
                self.assertEqual(self.run_mode(mode)["result"], "FAIL")

    def test_unavailable_route_fails(self):
        def unavailable(*args, **kwargs):
            raise OSError("route unavailable")
        report = observer.observe("https://stegverse.org/", opener=unavailable)
        self.assertEqual(report["result"], "FAIL")
        self.assertTrue(all(not row["match"] for row in report["routes"]))


if __name__ == "__main__":
    unittest.main()
