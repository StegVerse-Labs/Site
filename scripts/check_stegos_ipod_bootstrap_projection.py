#!/usr/bin/env python3
"""Validate the exact current StegOS device-local admitted-inference projection on Site."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "stegos_ipod_bootstrap_projection.report.json"
UPSTREAM_REPO = "StegVerse-Labs/StegOS"
UPSTREAM_COMMIT = "145fe88376f28eab26cdcd60df45a7e74ed0b9c1"
EXPECTED = {
    "stegos-bootstrap/index.html": "f2e9aa2a994acb9b259388b7b876be5ec5487c92",
    "stegos-bootstrap/stegos-bootstrap.js": "15343c398c168f3d5f8fe6933aaf3073e89dd5c0",
    "stegos-bootstrap/admitted-inference.js": "493cf77a64479efe816cb2d89e38e4255bca121b",
    "stegos-bootstrap/device-local-autostart.js": "3927e2aa650f3267c53af73f3ef8bea2379805b9",
    "stegos-bootstrap/service-worker.js": "0bf8c8df1ae678bc73170978f6c6fdae7b9341f1",
    "stegos-bootstrap/external-resident-task.js": "87dbfdf156224df80ab5f24ae263ed13cb7577c9",
    "stegos-bootstrap/stegverse-reference-model.js": "bd8e7553b61425386f6cf65db4766b952c148ed4",
    "stegos-bootstrap/tvc-sovereign-local-model-route.js": "3ca841310b904c2e09390512043f30f301976b1d",
    "stegos-bootstrap/manifest.webmanifest": "a223ec9454f46d0e9b91d4862f11de701792144a",
}

ALLOWED_SUCCESSORS = {
    "stegos-bootstrap/index.html": {"f2e9aa2a994acb9b259388b7b876be5ec5487c92", "b2c6f72c6947d09be0d7128e4a7df5d237a3b2d5"},
    "stegos-bootstrap/stegos-bootstrap.js": {"15343c398c168f3d5f8fe6933aaf3073e89dd5c0", "d1ae2940d16f757b4bb5964f36dab75fc48bf9c5"},
    "stegos-bootstrap/admitted-inference.js": {"493cf77a64479efe816cb2d89e38e4255bca121b", "5619540b9a953b58f2a859b5776241809aad1932"},
    "stegos-bootstrap/service-worker.js": {"0bf8c8df1ae678bc73170978f6c6fdae7b9341f1", "7c5d62d5fba1fcde13b3a47c3b9b561d03b77087"},
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
        allowed = ALLOWED_SUCCESSORS.get(relative, {expected_sha})
        if sha not in allowed:
            failures.append(f"blob mismatch {relative}: {sha} not in {sorted(allowed)}")

    bootstrap = read("stegos-bootstrap/stegos-bootstrap.js")
    inference = read("stegos-bootstrap/admitted-inference.js")
    autostart = read("stegos-bootstrap/device-local-autostart.js")
    html = read("stegos-bootstrap/index.html")
    service_worker = read("stegos-bootstrap/service-worker.js")
    model = read("stegos-bootstrap/stegverse-reference-model.js")
    route = read("stegos-bootstrap/tvc-sovereign-local-model-route.js")
    resident_task = read("stegos-bootstrap/external-resident-task.js")
    combined = "\n".join((bootstrap, inference, autostart, html, service_worker, model, route, resident_task))

    required_markers = {
        "activation_authority_plane": 'var AUTHORITY_PLANE = "STEGVERSE"',
        "credential_authority": 'var CREDENTIAL_AUTHORITY = "TV/TVC"',
        "canonical_model_owner": 'LOCAL_MODEL_SOURCE = "StegVerse-002/micro-node-runtime"',
        "canonical_model_id": 'LOCAL_MODEL_ID = "stegverse-reference-lm-v1"',
        "canonical_tvc_owner": 'TVC_SOURCE = "StegVerse-Labs/TVC"',
        "canonical_tvc_task": 'TVC_TASK = "TVC-SOVEREIGN-LOCAL-MODEL-ROUTE-002"',
        "device_endpoint": 'https://stegverse.org/stegos-bootstrap/local-model',
        "local_transport": 'SERVICE_WORKER_LOCAL_INTERCEPT',
        "automatic_admission": "bootstrapDeviceLocalInferenceEvidence()",
        "bounded_autostart": "MAX_ATTEMPTS = 120",
        "credential_free_fetch": 'credentials: "omit"',
        "measured_usage": "FAIL_CLOSED: model usage proof missing",
        "copy_evidence_button": 'id="copy-evidence"',
        "copy_evidence_clipboard": "navigator.clipboard.writeText",
        "device_task_scope": 'TASK_SCOPE = "DEVICE_LOCAL_INFERENCE_ONLY"',
        "device_continuity_key": 'DEVICE_ROOT_KEY = "device-continuity-root"',
        "device_continuity_schema": 'schema: "stegos.web_device_continuity_root.v1"',
        "device_continuity_id": 'device_continuity_id: "stegdevice-"',
        "node_binding_receipt": 'schema: "stegos.web_device_node_binding_receipt.v1"',
        "separate_unsynced_chains": "different_unsynced_device_continuity_roots_are_separate_chains: true",
        "no_implicit_cross_root": "implicit_cross_root_continuation_allowed: false",
        "governed_transfer_required": "governed_transfer_required_for_cross_root_continuation: true",
        "no_browser_hardware_attestation": 'hardware_attestation: "UNAVAILABLE_TO_BROWSER"',
        "evidence_root_export": "bundle.device_continuity_id = continuity.device_continuity_id",
        "evidence_node_export": "bundle.node_instance_id = bundle.node && bundle.node.node_id",
        "cross_context_create_if_absent": "function addMetaIfAbsent(db, key, value)",
        "indexeddb_atomic_add": 'objectStore(META_STORE).add({ key: key, value: value })',
        "lost_race_constraint": 'req.error.name === "ConstraintError"',
        "winning_context_gate": "then(function (wonCreate)",
        "lost_race_reuses_winner": "device continuity root race lost without persisted winner",
        "resident_task_profile": "STEGVERSE001_BOUNDED_CONTINUITY_AUDIT_V1",
        "resident_task_transition": "SV001_BOUNDED_AUTONOMY_CYCLE_COMPLETED",
        "resident_task_endpoint": 'RESIDENT_TASK_PATH = "/stegos-bootstrap/resident-task"',
        "resident_external_claim_not_promoted": "external_claim_promoted_to_browser_authority: false",
        "resident_global_worker_authority_false": "global_workercoordinator_authority: false",
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
        "CLOUDFLARE_API_TOKEN", "RENDER_API_KEY", "VERCEL_TOKEN", "GITHUB_TOKEN", "GH_TOKEN",
        "APP_STORE_CONNECT", "APPLE_ID_PASSWORD", "Authorization: Bearer",
    ]
    for marker in prohibited:
        if marker in combined:
            failures.append(f"prohibited credential/runtime marker projected: {marker}")

    report = {
        "schema_version": "1.7.0",
        "status": "FAIL" if failures else "PASS",
        "source_repository": UPSTREAM_REPO,
        "source_commit": UPSTREAM_COMMIT,
        "expected_git_blobs": EXPECTED,
        "observed_git_blobs": observed,
        "exact_projection": not failures and all(observed.get(path) in ALLOWED_SUCCESSORS.get(path, {expected}) for path, expected in EXPECTED.items()),
        "allowed_exact_successor_blobs": {k: sorted(v) for k, v in ALLOWED_SUCCESSORS.items()},
        "credential_authority": "TV/TVC",
        "credential_requirement": "NONE",
        "non_tv_tvc_secret_or_token_used": False,
        "second_non_stegverse_machine_required": False,
        "network_egress_required_for_device_model": False,
        "render_production_authority": False,
        "github_token_runtime_authority": False,
        "hosted_ci_activation_authority": False,
        "site_authority_effect": "TRANSPORT_MATERIALIZATION_ONLY",
        "device_continuity_identity_distinct_from_node_identity": True,
        "different_unsynced_roots_are_separate_chains": True,
        "implicit_cross_root_continuation_allowed": False,
        "governed_transfer_required_for_cross_root_continuation": True,
        "hardware_attestation_claimed_by_browser": False,
        "cross_context_device_root_creation_atomic": True,
        "duplicate_root_receipt_on_lost_race_allowed": False,
        "resident_task_source_commit": "835372a69af23dc73b6f75591ced6281c43ffa8d",
        "resident_task_execution_surface": "CURRENT_USER_IPHONE",
        "resident_task_global_workercoordinator_authority": False,
        "resident_task_external_claim_promoted_to_browser_authority": False,
        "control_revision": "DEVICE_CONTINUITY_ROOT_PLUS_EXTERNAL_RESIDENT_TASK_EXACT_PROJECTION_WITH_CURRENT_IPHONE_SUCCESSORS",
        "failures": failures,
    }
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"STEGOS_IPOD_BOOTSTRAP_PROJECTION_{report['status']}")
    for failure in failures:
        print(failure)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
