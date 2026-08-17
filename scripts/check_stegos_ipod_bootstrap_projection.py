#!/usr/bin/env python3
"""Validate the exact StegOS browser-bootstrap + admitted-inference projection on Site."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "stegos_ipod_bootstrap_projection.report.json"
UPSTREAM_REPO = "StegVerse-Labs/StegOS"
UPSTREAM_COMMIT = "441b72a467753a753f3cb9ac1dbced99f10de884"
EXPECTED = {
    "stegos-bootstrap/index.html": "018c97360e7064bf677944b79c1a3ba72dc64f51",
    "stegos-bootstrap/stegos-bootstrap.js": "15343c398c168f3d5f8fe6933aaf3073e89dd5c0",
    "stegos-bootstrap/admitted-inference.js": "7f4773757a8d1a81ad2a29e0dbed8662e5b89194",
    "stegos-bootstrap/service-worker.js": "00de0178f5bfc881b5d3e729734d519035de9901",
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

    bootstrap = (ROOT / "stegos-bootstrap/stegos-bootstrap.js").read_text(encoding="utf-8") if (ROOT / "stegos-bootstrap/stegos-bootstrap.js").exists() else ""
    inference = (ROOT / "stegos-bootstrap/admitted-inference.js").read_text(encoding="utf-8") if (ROOT / "stegos-bootstrap/admitted-inference.js").exists() else ""
    html = (ROOT / "stegos-bootstrap/index.html").read_text(encoding="utf-8") if (ROOT / "stegos-bootstrap/index.html").exists() else ""
    service_worker = (ROOT / "stegos-bootstrap/service-worker.js").read_text(encoding="utf-8") if (ROOT / "stegos-bootstrap/service-worker.js").exists() else ""
    combined = "\n".join((bootstrap, inference, html, service_worker))

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
        "operational_probe": "probeOperationalReadiness",
        "visible_node_action": 'id="node-action-state"',
        "touch_activation": 'addEventListener("touchend", requestEstablish',
        "canonical_model_owner": 'LOCAL_MODEL_SOURCE = "StegVerse-002/micro-node-runtime"',
        "canonical_model_id": 'LOCAL_MODEL_ID = "stegverse-reference-lm-v1"',
        "canonical_tvc_owner": 'TVC_SOURCE = "StegVerse-Labs/TVC"',
        "canonical_tvc_task": 'TVC_TASK = "TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002"',
        "raw_tvc_receipt": 'TVC_ROUTE_SCHEMA = "stegverse.tvc.sovereign-local-model-route-receipt.v1"',
        "protected_material_rejection": "protected credential material is not admissible",
        "credential_free_fetch": 'credentials: "omit"',
        "measured_usage": "FAIL_CLOSED: model usage proof missing",
        "model_output_no_authority": 'model_output_authority: "NONE"',
        "admitted_receipt": 'schema: "stegos.web_admitted_inference_receipt.v1"',
        "ui_evidence_admission": 'id="canonical-evidence"',
        "ui_run_inference": 'id="run-inference"',
        "offline_inference_consumer": '"./admitted-inference.js"',
    }
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
        "Authorization: Bearer",
    ]
    for marker in prohibited:
        if marker in combined:
            failures.append(f"prohibited credential/runtime marker projected: {marker}")

    report = {
        "schema_version": "1.2.0",
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
        "physical_activation_owner": "StegVerse-Labs/StegOS#15",
        "model_runtime_owner": "StegVerse-002/micro-node-runtime",
        "route_authority_owner": "StegVerse-Labs/TVC",
        "control_revision": "ADMITTED_INFERENCE_EXACT_PROJECTION",
        "failures": failures,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"STEGOS_IPOD_BOOTSTRAP_PROJECTION_{report['status']}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
