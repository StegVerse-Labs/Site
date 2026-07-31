#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

PDF_LINK_RE = re.compile(r"https://(?:github\.com/user-attachments/assets|private-user-images\.githubusercontent\.com)/[^\s)>]+")


def fail(message: str) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(1)


def download(url: str, token: str) -> bytes:
    request = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/octet-stream",
        "User-Agent": "StegVerse-HIL-Submission-Worker/1.0",
    })
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read()


def main() -> None:
    event_path = Path(os.environ["GITHUB_EVENT_PATH"])
    event = json.loads(event_path.read_text(encoding="utf-8"))
    issue = event.get("issue") or {}
    issue_number = int(issue.get("number") or 0)
    issue_body = str(issue.get("body") or "")
    issue_title = str(issue.get("title") or "")
    token = os.environ.get("GITHUB_TOKEN", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "unknown")
    run_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")

    if not issue_number:
        fail("missing issue number")
    if not issue_title.startswith("[HIL RESPONSE PACKET]"):
        fail("not a HIL response-packet issue")

    links = PDF_LINK_RE.findall(issue_body)
    if len(links) != 1:
        fail(f"expected exactly one GitHub attachment URL, found {len(links)}")

    pdf = download(links[0], token)
    if len(pdf) < 5 or pdf[:5] != b"%PDF-":
        fail("attached source object is not a valid PDF")
    if len(pdf) > 10 * 1024 * 1024:
        fail("response PDF exceeds 10 MiB")

    response_sha256 = hashlib.sha256(pdf).hexdigest()
    submission_id = f"HIL-SUBMISSION-{uuid.uuid4()}"
    receipt_id = f"HIL-RECEIPT-{uuid.uuid4()}"
    received_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # GitHub issue-form sections are retained verbatim as participant-supplied evidence.
    display_name = "Anonymous"
    match = re.search(r"### Display name\s*\n\s*(.+?)(?:\n###|\Z)", issue_body, re.S)
    if match:
        candidate = match.group(1).strip()
        if candidate and candidate != "_No response_":
            display_name = candidate[:100]

    receipt = {
        "schema_version": "HIL-GITHUB-WORKER-RECEIPT-v1",
        "submission_id": submission_id,
        "receipt_id": receipt_id,
        "received_at": received_at,
        "response_sha256": response_sha256,
        "size_bytes": len(pdf),
        "source_issue_number": issue_number,
        "source_attachment_url": links[0],
        "display_name": display_name,
        "worker_run_id": run_id,
        "worker_run_attempt": run_attempt,
        "processing_isolation_key": f"issue-{issue_number}-run-{run_id}-attempt-{run_attempt}",
        "state": "RECEIVED_BY_GITHUB_WORKER",
        "review_state": "PENDING",
        "publication_state": "NOT_AUTHORIZED",
    }
    receipt_bytes = (json.dumps(receipt, indent=2, sort_keys=True) + "\n").encode()
    receipt["receipt_sha256"] = hashlib.sha256(receipt_bytes).hexdigest()

    out = Path("hil-worker-output") / submission_id
    out.mkdir(parents=True, exist_ok=False)
    (out / "response.pdf").write_bytes(pdf)
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "source-issue-body.md").write_text(issue_body, encoding="utf-8")

    github_output = Path(os.environ["GITHUB_OUTPUT"])
    with github_output.open("a", encoding="utf-8") as handle:
        handle.write(f"submission_id={submission_id}\n")
        handle.write(f"receipt_id={receipt_id}\n")
        handle.write(f"response_sha256={response_sha256}\n")
        handle.write(f"output_dir={out.as_posix()}\n")
        handle.write(f"branch=hil/submission-{issue_number}-{run_id}-{run_attempt}\n")


if __name__ == "__main__":
    main()
