#!/usr/bin/env python3
"""Validate the exact StegOS browser-bootstrap projection on Site."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "stegos_ipod_bootstrap_projection.report.json"
UPSTREAM_REPO = "StegVerse-Labs/StegOS"
UPSTREAM_COMMIT = "799e0f3fd2766a32cbf0720384db11f066d8e9b8"
EXPECTED = {
    "stegos-bootstrap/index.html": "0b3ca0df4f1c2e115f1a7040ab981ff5c7b67db0",
    "stegos-bootstrap/stegos-bootstrap.js": "0f58bf5b8dd7b5de02c4113aebf798005f2e5808",
    "stegos-bootstrap/service-worker.js": "d489341a69185a33e36c517177a2049a0b160ead",
    "stegos-bootstrap/manifest.webmanifest": "a223ec9454f46d0e9b91d4862f11de701792144a",
}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def main() -> int:
    failures: list[str] = []
    observed: dict[str, str] = {}
    for relative, expected_sha in EXPECTED.items():
        path = ROOT / relative
        if not path.exists():
            failures.append(f"missing projected file: {relative}")
            continue
        sha = git_blob_sha(path.read_bytes())
        observed[relative] = sha
        if sha != expected_sha:
            failures.append(f"blob mismatch {relative}: {sha} != {expected_sha}")

    js = (ROOT / "stegos-bootstrap/stegos-bootstrap.js").read_text(encoding="utf-8") if (ROOT / "stegos-bootstrap/stegos-bootstrap.js").exists() else ""
    html = (ROOT / "stegos-bootstrap/index.html").read_text(encoding="utf-8") if (ROOT / "stegos-bootstrap/index.html").exists() else ""
    required_markers = {
        "activation_authority_plane": 'var AUTHORITY_PLANE = "STEGVERSE"',
        "credential_authority": 'var CREDENTIAL_AUTHORITY = "TV/TVC"',
        "no_external_machine": "requires_external_non_stegverse_machine: false",
        "no_hosted_ci_authority": 'hosted_ci_activation_authority: "NONE"',
        "ecosystem_chat": 'var SERVICE_CHAT = "stegverse.ecosystem-chat"',
        "local_node_prerequisite": "local_node_runtime_ready: true",
        "local_journal_prerequisite": "local_receipt_journal_ready: true",
        "inference_fail_closed": 'inference_actions_state: "FAIL_CLOSED_UNTIL_STEGVERSE_MODEL_EVIDENCE"',
        "site_visible_no_second_machine": "Second non-StegVerse machine required",
    }
    combined = js + "\n" + html
    for label, marker in required_markers.items():
        if marker not in combined:
            failures.append(f"missing authority/activation marker {label}: {marker}")

    prohibited = [
        "CLOUDFLARE_API_TOKEN",
        "RENDER_API_KEY",
        "VERCEL_TOKEN",
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "APP_STORE_CONNECT",
        "APPLE_ID_PASSWORD",
        "PRIVATE_KEY",
    ]
    for marker in prohibited:
        if marker in combined:
            failures.append(f"prohibited credential/runtime marker projected: {marker}")

    report = {
        "schema_version": "1.0.0",
        "status": "FAIL" if failures else "PASS",
        "source_repository": UPSTREAM_REPO,
        "source_commit": UPSTREAM_COMMIT,
        "expected_git_blobs": EXPECTED,
        "observed_git_blobs": observed,
        "exact_projection": not failures and observed == EXPECTED,
        "credential_authority": "TV/TVC",
        "non_tv_tvc_secret_or_token_used": False,
        "render_production_authority": False,
        "github_token_runtime_authority": False,
        "hosted_ci_activation_authority": False,
        "site_authority_effect": "TRANSPORT_MATERIALIZATION_ONLY",
        "physical_activation_owner": "StegVerse-Labs/StegOS#13",
        "failures": failures,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"STEGOS_IPOD_BOOTSTRAP_PROJECTION_{report['status']}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
