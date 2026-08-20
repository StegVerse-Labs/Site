#!/usr/bin/env python3
"""Validate the exact current StegOS device-local admitted-inference projection on Site."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "stegos_ipod_bootstrap_projection.report.json"
UPSTREAM_REPO = "StegVerse-Labs/StegOS"
UPSTREAM_COMMIT = "f52ca9e1fac332a0ff6e79fb4a00579d1bbc95a9"
EXPECTED = {
    "stegos-bootstrap/index.html": "561e21d38df310aee838716ab9f2a4a6175485d5",
    "stegos-bootstrap/stegos-bootstrap.js": "15343c398c168f3d5f8fe6933aaf3073e89dd5c0",
    "stegos-bootstrap/admitted-inference.js": "1cac8bc4d5a13a6596cd7f68b01e3a93be7536f0",
    "stegos-bootstrap/device-local-autostart.js": "d2aaffa033003cb6b031dbf30312c6104de989b2",
    "stegos-bootstrap/service-worker.js": "3cba6ca48c8b093d0f0baa48aff000a544e93cc6",
    "stegos-bootstrap/stegverse-reference-model.js": "bd8e7553b61425386f6cf65db4766b952c148ed4",
    "stegos-bootstrap/tvc-sovereign-local-model-route.js": "3ca841310b904c2e09390512043f30f301976b1d",
    "stegos-bootstrap/manifest.webmanifest": "a223ec9454f46d0e9b91d4862f11de701792144a",
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def read(relative: str) -> str:
    path = ROOT / relative
    return path.read_text(encoding="utf-8") if path.exists() else ""


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

    bootstrap = read("stegos-bootstrap/stegos-bootstrap.js")
    inference = read("stegos-bootstrap/admitted-inference.js")
    autostart = read("stegos-bootstrap/device-local-autostart.js")
    html = read("stegos-bootstrap/index.html")
    service_worker = read("stegos-bootstrap/service-worker.js")
    model = read("stegos-bootstrap/stegverse-reference-model.js")
    route = read("stegos-bootstrap/tvc-sovereign-local-model-route.js")
    combined = "\n".join((bootstrap, inference, autostart, html, service_worker, model, route))

    required_markers = {
        "activation_authority_plane": 'var AUTHORITY_PLANE = "STEGVERSE"',
        "credential_authority": 'var CREDENTIAL_AUTHORITY = "TV/TVC"',
        "no_external_machine": "requires_external_non_stegverse_machine: false",
        "canonical_model_owner": 'LOCAL_MODEL_SOURCE = "StegVerse-002/micro-node-runtime"',
        "canonical_model_id": 'LOCAL_MODEL_ID = "stegverse-reference-lm-v1"',
        "canonical_model_hash": 'EXPECTED_MODEL_HASH = "5c1a425a40cd63cf5f4bb4cc28c3eebaad9713a42cfdcfb85e025d3371013a4d"',
        "canonical_tvc_owner": 'TVC_SOURCE = "StegVerse-Labs/TVC"',
        "canonical_tvc_task": 'TVC_TASK = "TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002"',
        "device_endpoint": 'https://stegverse.org/stegos-bootstrap/local-model',
        "local_transport": 'SERVICE_WORKER_LOCAL_INTERCEPT',
        "local_completion_path": '"/v1/chat/completions"',
        "local_evidence_path": '"/canonical-evidence"',
        "no_network_egress": "network_egress_required: false",
        "automatic_admission": "bootstrapDeviceLocalInferenceEvidence()",
        "bounded_autostart": "MAX_ATTEMPTS = 120",
        "worker_update": "registration.update()",
        "protected_material_rejection": "protected credential material is not admissible",
        "credential_free_fetch": 'credentials: "omit"',
        "measured_usage": "FAIL_CLOSED: model usage proof missing",
        "model_output_no_authority": 'model_output_authority: "NONE"',
        "admitted_receipt": 'schema: "stegos.web_admitted_inference_receipt.v1"',
        "autostart_asset": 'src="./device-local-autostart.js"',
        "copy_evidence_button": 'id="copy-evidence"',
        "copy_evidence_clipboard": "navigator.clipboard.writeText",
        "copy_evidence_fallback": 'document.execCommand("copy")',
        "device_task_scope": 'TASK_SCOPE = "DEVICE_LOCAL_INFERENCE_ONLY"',
        "device_task_claim": 'schema: "stegos.web_task_claim_receipt.v1"',
        "device_task_terminal": 'schema: "stegos.web_task_terminal_receipt.v1"',
        "device_task_reconstruction": 'schema: "stegos.web_task_reconstruction_receipt.v1"',
        "device_task_replay": 'reconstruction_state: "PASS"',
    }
    for label, marker in required_markers.items():
        if marker not in combined:
            failures.append(f"missing authority/activation marker {label}: {marker}")

    local_branch = ""
    if 'url.pathname === LOCAL_PATH' in service_worker:
        local_branch = service_worker.split('url.pathname === LOCAL_PATH', 1)[1].split('if (event.request.method !== "GET")', 1)[0]
    if "event.respondWith(handleLocalModel" not in local_branch:
        failures.append("service worker does not own local model branch")
    if "fetch(event.request)" in local_branch:
        failures.append("device-local model branch may escape to network")

    prohibited = [
        "CLOUDFLARE_API_TOKEN",
        "RENDER_API_KEY",
        "VERCEL_TOKEN",
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "APP_STORE_CONNECT",
        "APPLE_ID_PASSWORD",
        "Authorization: Bearer",
    ]
    for marker in prohibited:
        if marker in combined:
            failures.append(f"prohibited credential/runtime marker projected: {marker}")

    report = {
        "schema_version": "1.5.0",
        "status": "FAIL" if failures else "PASS",
        "source_repository": UPSTREAM_REPO,
        "source_commit": UPSTREAM_COMMIT,
        "expected_git_blobs": EXPECTED,
        "observed_git_blobs": observed,
        "exact_projection": not failures and observed == EXPECTED,
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "non_tv_tvc_secret_or_token_used": False,
        "second_non_stegverse_machine_required": False,
        "network_egress_required_for_device_model": False,
        "render_production_authority": False,
        "github_token_runtime_authority": False,
        "hosted_ci_activation_authority": False,
        "site_authority_effect": "TRANSPORT_MATERIALIZATION_ONLY",
        "physical_activation_owner": "StegVerse-Labs/StegOS#15",
        "model_runtime_owner": "StegVerse-002/micro-node-runtime",
        "route_authority_owner": "StegVerse-Labs/TVC",
        "control_revision": "DEVICE_LOCAL_FENCED_TASK_PLUS_COPY_TEXT_EXACT_PROJECTION",
        "failures": failures,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"STEGOS_IPOD_BOOTSTRAP_PROJECTION_{report['status']}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
