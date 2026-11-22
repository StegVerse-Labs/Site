"""Builder smoke test THROUGH THE PAGE. Fixture evidence only; not V2 acceptance.
Playwright is a development test tool, not an on-ramp runtime dependency.
"""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import zipfile

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_pipeline import INTAKE, fixture_fetch, Pipeline, Server, handler_for, sha, TEMPLATE

OUT = Path(__file__).resolve().parents[1] / "evidence"


def main():
    OUT.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        service = Pipeline(Path(temp) / "state", fixture_fetch)
        server = Server(("127.0.0.1", 0), handler_for(service))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        url = "http://127.0.0.1:" + str(server.server_port)
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, executable_path=shutil.which("chromium"), args=["--no-sandbox"])
                page = browser.new_page(viewport={"width": 390, "height": 844})
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.goto(url)
                page.wait_for_function("document.querySelector('#status').textContent.includes('S1-INTAKE')")
                for field in ("framework", "operator", "project_id", "funding", "funder", "arrangement"):
                    page.locator('[name="' + field + '"]').fill(INTAKE[field])
                page.locator('[name="public_surfaces"]').fill("\n".join(INTAKE["public_surfaces"]))
                page.locator('[name="claims"]').fill(json.dumps(INTAKE["claims"]))
                page.get_by_role("checkbox").check()
                page.get_by_role("button", name="Receive intake receipt").click()
                page.wait_for_function("!document.querySelector('#download').hidden")
                assert "1 LOCATED" in page.locator("#progress").inner_text()
                assert "1 EVIDENCE_NOT_FOUND" in page.locator("#progress").inner_text()
                assert "CONFORMANT" in page.locator("#progress").inner_text()
                assert "IN_BUILD" in page.locator("#progress").inner_text()
                receipt_text = page.locator("#receipt").inner_text()
                identifier = receipt_text.split(": ", 1)[1].split(" ·", 1)[0]
                with page.expect_download() as info:
                    page.locator("#download").click()
                bundle = OUT / "local-page-specimen.zip"
                info.value.save_as(bundle)
                assert not errors, errors
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
                # Publish a test-only pointer only after the actual page submission.
                (service.storage / "public-specimen.json").write_text(json.dumps({"id": identifier, "grade": "LOCAL_FIXTURE_ONLY"}))
                page.reload()
                page.wait_for_function("document.querySelector('#specimen').textContent.includes('Download public specimen')")
                page.screenshot(path=str(Path(temp) / "mobile.png"), full_page=True)
                shutil.copy(Path(temp) / "mobile.png", "/workspace/scratch/0d5b4b61ddcf/q67-mobile.png")
                browser.close()
            unpack = Path(temp) / "unpack"
            with zipfile.ZipFile(bundle) as z:
                z.extractall(unpack)
            result = service.run(identifier)
            check = subprocess.run([sys.executable, "-B", str(unpack / "suite/self_check.py")], capture_output=True, text=True, check=True)
            proof = subprocess.run([sys.executable, "-B", str(TEMPLATE / "prove_conformance.py"), str(unpack / "suite")], capture_output=True, text=True, check=True)
            report = {"grade": "BUILDER_LOCAL_PAGE_FIXTURE_ONLY", "production_acceptance": "NOT_PERFORMED",
                "entry": "HTML form clicked in Chromium at 390x844; no direct backend build used for submission",
                "intake_receipt": identifier, "located": 1, "evidence_not_found": 1,
                "manifest_sha256": result["manifest_sha256"], "bundle_sha256": sha(bundle.read_bytes()),
                "conformance_stdout": proof.stdout, "self_check_stdout": check.stdout,
                "connection": result["connection"], "page_errors": errors,
                "source_limit": "example.org resource bodies supplied by deterministic test transport; no external-framework or production crossing represented",
                "public_specimen": "test-only pointer successfully resolved after page run"}
            (OUT / "local-page-report.json").write_text(json.dumps(report, indent=2) + "\n")
            print(json.dumps(report, indent=2))
        finally:
            server.shutdown(); server.server_close(); thread.join()


if __name__ == "__main__":
    main()
