import copy
import io
import json
from pathlib import Path
import shutil
import socket
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch
import urllib.error
import urllib.request
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import Pipeline, Refused, PublicFetcher, TEMPLATE, analyze, sha, verify_template
from server import Server, handler_for

CLAIM = 'This fixture retains the exact phrase "evidence first".'
INTAKE = {"framework": "Q67 fixture specimen", "operator": "CODEX builder fixture",
    "project_id": "Q67-LOCAL-FIXTURE", "funding": "Builder test compute; no sale or price quoted",
    "funder": "Declared builder fixture", "arrangement": "No external commercial arrangement",
    "public_surfaces": ["https://example.org/framework"],
    "claims": [{"text": CLAIM, "lives_at": "https://example.org/framework",
                "receipted_by": "https://example.org/receipt", "replay": "https://example.org/replay"},
               {"text": "UNSUPPORTED-CLAIM-NEGATIVE-CONTROL"}]}


def fixture_fetch(url):
    bodies = {"https://example.org/framework": CLAIM.encode(),
              "https://example.org/receipt": b'{"grade":"FIXTURE_RECEIPT_ONLY"}',
              "https://example.org/replay": b'{"grade":"FIXTURE_REPLAY_ONLY"}'}
    if url not in bodies:
        raise OSError("fixture unknown")
    data = bodies[url]
    return {"url": url, "status": 200, "body": data, "sha256": sha(data), "bytes": len(data)}


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.pipeline = Pipeline(self.temp.name, fixture_fetch)

    def tearDown(self):
        self.temp.cleanup()

    def test_canonical_template_and_tamper_fail_before_derivation(self):
        self.assertEqual(len(verify_template()["components"]), 9)
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "template"
            shutil.copytree(TEMPLATE, target)
            with (target / "instantiate.py").open("ab") as f:
                f.write(b"# changed")
            with self.assertRaises(Refused):
                verify_template(target)
            pipeline = self.pipeline
            receipt = pipeline.intake(INTAKE)
            with patch("pipeline.TEMPLATE", target), patch("pipeline.run_python") as runner:
                with self.assertRaises(Refused):
                    pipeline.run(receipt["id"])
                runner.assert_not_called()
            self.assertFalse((pipeline.directory_for(receipt["id"]) / "suite.zip").exists())

    def test_bundle_canonical_proof_claim_guard_and_idempotence(self):
        receipt = self.pipeline.intake(INTAKE)
        result = self.pipeline.run(receipt["id"])
        self.assertEqual(result, self.pipeline.run(receipt["id"]))
        self.assertEqual(result["conformance"]["verdict"], "CONFORMANT")
        self.assertEqual((result["analysis"]["located"], result["analysis"]["evidence_not_found"]), (1, 1))
        self.assertEqual(result["state"], "SPECIMEN_ONLY")
        self.assertEqual(result["connection"]["registration"], "NOT_PERFORMED")
        self.assertEqual(result["analysis"]["claims"][0]["submitted_claim"], INTAKE["claims"][0])
        folder = self.pipeline.directory_for(receipt["id"])
        with zipfile.ZipFile(folder / "suite.zip") as z:
            self.assertIsNone(z.testzip())
            claims = json.loads(z.read("suite/CLAIMS__01.json"))
            self.assertNotIn("UNSUPPORTED-CLAIM-NEGATIVE-CONTROL", json.dumps(claims))
            self.assertIn("UNSUPPORTED-CLAIM-NEGATIVE-CONTROL", z.read("suite/GAPS__01.json").decode())
            manifest = json.loads(z.read("suite/PACKAGE__MANIFEST__01.json"))
            for member in manifest["members"]:
                data = z.read("suite/" + member["file"])
                self.assertEqual((len(data), sha(data)), (member["bytes"], member["sha256"]))
            self.assertEqual(z.read("suite/self_check.py"), (TEMPLATE / "self_check.py.tmpl").read_bytes())
            self.assertEqual(set(z.namelist()), {"suite/PACKAGE__MANIFEST__01.json"} | {"suite/" + m["file"] for m in manifest["members"]})
            self.assertNotIn("TODO", "".join(z.read(n).decode() for n in z.namelist() if n.endswith(".md")))
        self.assertFalse(list(folder.glob("*.pending")))

    def test_missing_triple_and_nonverbatim_claim_never_located(self):
        data = copy.deepcopy(INTAKE)
        for field in ("lives_at", "receipted_by", "replay"):
            claim = copy.deepcopy(INTAKE["claims"][0])
            claim.pop(field)
            data["claims"] = [claim]
            self.assertEqual(analyze(data, fixture_fetch)["located"], 0)
        data["claims"] = [dict(INTAKE["claims"][0], text="unsupported paraphrase")]
        self.assertEqual(analyze(data, fixture_fetch)["located"], 0)
        data = copy.deepcopy(INTAKE)
        data["public_surfaces"] = ["https://unrelated.example.org/framework"]
        self.assertEqual(analyze(data, fixture_fetch)["located"], 0)

    def test_ssrf_private_dns_and_url_controls(self):
        for ip in ["127.0.0.1", "10.0.0.1", "169.254.169.254", "::1", "fc00::1"]:
            fake = [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, 443))]
            with patch("socket.getaddrinfo", return_value=fake), patch("socket.socket") as sock:
                with self.assertRaises(Refused):
                    PublicFetcher()("https://example.org/evidence")
                sock.assert_not_called()
        for url in ["http://example.org", "https://user:secret@example.org", "https://example.org:8443", "file:///etc/passwd"]:
            with self.assertRaises(Refused):
                PublicFetcher()(url)

    def test_receipt_path_traversal_refused(self):
        with self.assertRaises(FileNotFoundError):
            self.pipeline.directory_for("../../etc/passwd")

    def test_api_account_free_receipt_download_and_origin(self):
        server = Server(("127.0.0.1", 0), handler_for(self.pipeline))
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        base = "http://127.0.0.1:" + str(server.server_port)
        def post(path, data, headers=None):
            return urllib.request.urlopen(urllib.request.Request(base + path, json.dumps(data).encode(),
                {"Content-Type": "application/json", **(headers or {})}), timeout=20)
        try:
            with post("/api/intakes", INTAKE) as r:
                self.assertEqual(r.status, 201)
                receipt = json.load(r)
            with post("/api/intakes/" + receipt["id"] + "/build", {}) as r:
                result = json.load(r)
            with urllib.request.urlopen(base + result["download"]) as r:
                self.assertEqual(r.headers["Content-Type"], "application/zip")
                self.assertEqual(sha(r.read()), result["bundle_sha256"])
            with self.assertRaises(urllib.error.HTTPError) as error:
                post("/api/intakes", INTAKE, {"Origin": "https://attacker.example"})
            self.assertEqual(error.exception.code, 403)
            with urllib.request.urlopen(base + "/api/status") as r:
                self.assertFalse(json.load(r)["full_pipeline_offered"])
            with self.assertRaises(urllib.error.HTTPError) as error:
                urllib.request.urlopen(base + "/api/specimen")
            self.assertEqual(error.exception.code, 503)
        finally:
            server.shutdown(); server.server_close(); worker.join()


if __name__ == "__main__":
    unittest.main()
