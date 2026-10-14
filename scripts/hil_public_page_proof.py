#!/usr/bin/env python3
"""One-attempt proof that GitHub Pages serves the HIL participant surfaces exactly as committed.

The proof is bound to a state transition, the completion of a Pages deployment of a commit, and
makes exactly one request per surface: it never waits for, polls or retries another machine. The
served bytes must equal the bytes of the same file at the deployed commit (the Site is published
with .nojekyll, so Pages serves files verbatim). Every attempt ends in one disposition:

* PASS          served bytes equal the deployed source bytes for every surface
* NO_TRANSITION the surfaces are unchanged since a recorded PASS for the same source bytes
* FAIL_CLOSED   a surface was not served or differs; the record carries the failed predicate and
                its retry edge (the next Pages deployment, or a manual dispatch of the workflow)

Exit status is 0 for PASS and NO_TRANSITION, 1 for FAIL_CLOSED.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "data" / "hil-public-page-proof-latest.json"
BASE_URL = "https://stegverse.org/"
SURFACES = ("humans-as-interoperability-layer.html", "stegos-bootstrap/hil-resume.html")
WORKFLOW = ".github/workflows/hil-public-page-proof.yml"
OWNING_GOAL = "SHWP-HIL-SOVEREIGN-RECEIVER-001"
SCHEMA = "HIL-PUBLIC-PAGE-PROOF-v2"

Fetch = Callable[[str], "tuple[int, bytes]"]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def source_bytes(commit: str, path: str) -> bytes | None:
    done = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT, capture_output=True, check=False)
    return done.stdout if done.returncode == 0 else None


def fetch(url: str) -> tuple[int, bytes]:
    request = urllib.request.Request(url, headers={"Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, b""
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, b""


def load_previous(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def prove(commit: str, previous: dict, get: Fetch = fetch, read: Callable[[str, str], bytes | None] = source_bytes) -> dict:
    sources = {path: read(commit, path) for path in SURFACES}
    source_hashes = {path: sha256(data) if data is not None else None for path, data in sources.items()}
    if previous.get("result") == "PASS" and previous.get("source_sha256") == source_hashes:
        return {**previous, "result": "NO_TRANSITION", "deployed_commit": commit}

    surfaces = []
    failed = None
    for path in SURFACES:
        status, served = get(f"{BASE_URL}{path}?proof={commit}")
        entry = {
            "path": path,
            "url": f"{BASE_URL}{path}",
            "http_status": status,
            "source_sha256": source_hashes[path],
            "served_sha256": sha256(served) if served else None,
        }
        entry["served_bytes_match_source"] = bool(served) and entry["served_sha256"] == entry["source_sha256"]
        surfaces.append(entry)
        if failed is None:
            if source_hashes[path] is None:
                failed = ("HIL_PUBLIC_SURFACE_SOURCE_MISSING", f"{path} exists at the deployed commit")
            elif status != 200:
                failed = ("HIL_PUBLIC_SURFACE_NOT_SERVED", f"{path} is served with HTTP 200")
            elif not entry["served_bytes_match_source"]:
                failed = ("HIL_PUBLIC_SURFACE_BYTES_DIFFER", f"{path} is served byte-identical to the deployed commit")

    record = {
        "schema_version": SCHEMA,
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "deployed_commit": commit,
        "source_sha256": source_hashes,
        "surfaces": surfaces,
        "attempts": 1,
        "result": "PASS" if failed is None else "FAIL_CLOSED",
        "runtime_evidence_claimed": False,
        "authority_effect": False,
    }
    if failed is not None:
        record.update(
            {
                "failure_code": failed[0],
                "failed_predicate": failed[1],
                "required_evidence_or_repair": "a Pages deployment of this commit that serves every HIL surface byte-identical to its source",
                "retry_entrypoint": WORKFLOW,
                "owning_existing_goal": OWNING_GOAL,
                "next_attempt": "the next completed Pages deployment, or a manual dispatch of the proof workflow for the deployed commit",
            }
        )
    return record


def same_outcome(previous: dict, record: dict) -> bool:
    keys = ("result", "source_sha256", "failure_code", "surfaces")
    return all(previous.get(key) == record.get(key) for key in keys)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--commit", required=True, help="commit the Pages deployment published")
    parser.add_argument("--record", type=Path, default=RECORD)
    args = parser.parse_args(argv)

    previous = load_previous(args.record)
    record = prove(args.commit, previous)
    if record["result"] != "NO_TRANSITION" and not same_outcome(previous, record):
        args.record.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"HIL_PUBLIC_PAGE_PROOF={record['result']}" + (f":{record['failure_code']}" if "failure_code" in record else ""))
    return 1 if record["result"] == "FAIL_CLOSED" else 0


if __name__ == "__main__":
    sys.exit(main())
