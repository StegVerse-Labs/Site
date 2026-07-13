#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE_URL = os.getenv("STEGVERSE_SITE_BASE_URL", "https://stegverse-labs.github.io/Site").rstrip("/")
PAGE_URL = f"{BASE_URL}/governed-transitions.html"
INDEX_URL = f"{BASE_URL}/data/governed-transition-index.json"
STATUS_URL = f"{BASE_URL}/data/governed-transition-index-import-status.json"
EXECUTOR_URL = f"{BASE_URL}/data/governed-executor-status.json"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return "\n".join(self.parts)


def fetch(url: str) -> tuple[int | None, bytes]:
    request = Request(url, headers={"User-Agent": "StegVerse-Transition-Observatory-Verification/1.1"})
    with urlopen(request, timeout=30) as response:
        return getattr(response, "status", None), response.read()


def main() -> int:
    errors: list[str] = []
    try:
        page_status, page_body = fetch(PAGE_URL)
        index_status, index_body = fetch(INDEX_URL)
        import_status_code, import_body = fetch(STATUS_URL)
        executor_status_code, executor_body = fetch(EXECUTOR_URL)
    except HTTPError as exc:
        print(f"GOVERNED TRANSITION LIVE URLS: FAIL - http_{exc.code}:{exc.url}")
        return 1
    except URLError as exc:
        print(f"GOVERNED TRANSITION LIVE URLS: FAIL - url_error:{exc.reason}")
        return 1

    for label, status in [
        ("page", page_status),
        ("index", index_status),
        ("import_status", import_status_code),
        ("executor_status", executor_status_code),
    ]:
        if status != 200:
            errors.append(f"{label}_status:{status}")

    parser = TextExtractor()
    parser.feed(page_body.decode("utf-8", errors="replace"))
    text = parser.text()
    for marker in [
        "Governed Ecosystem Transitions",
        "derived public projection",
        "Native executor activation",
        "Admissible Automated Transitions",
    ]:
        if marker not in text:
            errors.append(f"page_missing:{marker}")

    try:
        index = json.loads(index_body.decode("utf-8"))
        import_status = json.loads(import_body.decode("utf-8"))
        executor = json.loads(executor_body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"invalid_json:{exc}")
    else:
        if index.get("projection_type") != "governed_transition_index":
            errors.append("index_projection_type")
        if not isinstance(index.get("records"), list):
            errors.append("index_records")
        if import_status.get("status_type") != "governed_transition_index_import_status":
            errors.append("import_status_type")
        if import_status.get("state") not in {"LOCAL_FALLBACK_ACTIVE", "RECEIPTED_EXPORT_IMPORTED"}:
            errors.append("import_state")
        if import_status.get("state") == "LOCAL_FALLBACK_ACTIVE":
            if import_status.get("hash_verified") is not False or import_status.get("live_orchestration_feed") is not False:
                errors.append("fallback_overclaim")
        if import_status.get("state") == "RECEIPTED_EXPORT_IMPORTED" and import_status.get("hash_verified") is not True:
            errors.append("receipted_import_unverified")

        if executor.get("projection_type") != "governed_executor_status":
            errors.append("executor_projection_type")
        if executor.get("from_executor", {}).get("status") != "FALLBACK_ONLY":
            errors.append("bootstrap_executor_not_fallback_only")
        if executor.get("to_executor", {}).get("status") != "ACTIVE":
            errors.append("native_executor_not_active")
        activation = executor.get("activation", {})
        if activation.get("state") != "ACTIVE":
            errors.append("executor_activation_not_active")
        if not activation.get("activation_receipt_id"):
            errors.append("executor_activation_receipt_missing")
        boundary = executor.get("authority_boundary", {})
        for key in [
            "projection_grants_execution_authority",
            "projection_grants_publication_authority",
            "projection_grants_admissibility",
            "projection_is_master_records_custody",
            "activation_is_per_transition_authority",
        ]:
            if boundary.get(key) is not False:
                errors.append(f"executor_boundary_overclaim:{key}")

    if errors:
        print("GOVERNED TRANSITION LIVE URLS: FAIL - " + ", ".join(errors))
        return 1
    print(f"GOVERNED TRANSITION LIVE URLS: PASS - {PAGE_URL} executor={EXECUTOR_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
