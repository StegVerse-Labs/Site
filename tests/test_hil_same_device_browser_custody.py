from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "stegos-bootstrap"
GENERATED = ROOT / "assets" / "generated"


def test_generated_browser_connector_carries_canonical_hil_downstream_profiles():
    manifest = json.loads((GENERATED / "site-browser-intr-connectors.manifest.json").read_text(encoding="utf-8"))
    artifact = (GENERATED / "site-browser-intr-connectors.js").read_bytes()
    assert manifest["registry_sha256"] == "sha256:831b5aa69cfc78cfff3d631949f7dfe0667511d618129f50a077b5ac222a047b"
    assert manifest["artifact_sha256"] == "sha256:" + hashlib.sha256(artifact).hexdigest()
    assert manifest["profile_sha256"]["hil-ingress-custody"] == "sha256:cf16fa7145364561b20e580cc8de621b9beb556137d0338f5eb757ba4079d165"
    assert manifest["profile_sha256"]["hil-tvc-lifecycle"] == "sha256:9b6c26c1ef9588b3522740b9fcea547ae7cac637fa8dca42ca0d1e5fca8548bd"
    source = artifact.decode("utf-8")
    assert '"hil-ingress-custody"' in source
    assert '"hil-tvc-lifecycle"' in source
    assert "buildReceipt" in source
    assert "validateComplete" in source


def test_custody_successor_is_same_device_fail_closed_and_preserves_g25():
    src = (BOOT / "hil-browser-custody.js").read_text(encoding="utf-8")
    assert 'var ROUTE_PATH = "/stegos-bootstrap/portable-workercoordinator/hil-custody-v1"' in src
    assert 'var PROTOCOL = "HIL_BROWSER_CUSTODY_V1"' in src
    assert 'var LEASE_ID = "HIL-BROWSER-ESRL-7bafde4a280e847758da157e"' in src
    assert 'var CLAIM_ID = "SHWP-SHWP-HIL-SOVEREIGN-RECEIVER-001-G25"' in src
    assert "var FENCING_TOKEN = 25" in src
    assert 'lease.custody_observed !== false' in src
    assert 'lease.post_restart_exact_byte_proof_observed !== false' in src
    assert 'lease.tvc_lifecycle_receipt_observed !== false' in src
    assert 'lease.requires_other_machine !== false' in src
    assert 'lease.second_claim_minted !== false' in src
    assert 'github_token_runtime_authority: "NONE"' in src
    assert 'credential_authority: "TV/TVC"' in src


def test_custody_successor_reuses_exact_staged_packet_and_canonical_intr_chain():
    src = (BOOT / "hil-browser-custody.js").read_text(encoding="utf-8")
    assert 'var STAGING_DB = "stegverse-hil-v3"' in src
    assert 'var STAGING_STORE = "response_files"' in src
    assert '"hil-submission", bindingBytes, "SUBMIT"' in src
    assert '"hil-ingress-custody", verified.bindingBytes, "ACCEPT_CUSTODY"' in src
    assert '"hil-tvc-lifecycle", verified.bindingBytes, "ADMIT_LIFECYCLE"' in src
    assert "intr.buildMaterializationRequest(" in src
    assert 'fail("staged exact-byte SHA-256 mismatch")' in src
    assert 'fail("staged canonical ingress intent mismatch")' in src
    assert 'fail("staged materialization request hash/binding mismatch")' in src
    assert 'next_required_transition: "HIL_CUSTODY_TVC_INTERLOCK_ADMISSION"' in src


def test_custody_assertion_occurs_only_after_separate_write_and_readback():
    src = (BOOT / "hil-browser-custody.js").read_text(encoding="utf-8")
    object_write = src.index("idbAdd(db, CUSTODY_OBJECTS")
    object_readback = src.index("idbGet(db, CUSTODY_OBJECTS, objectKey)", object_write)
    exact_assertion = src.index('custody_state: "EXACT_BYTES_PERSISTED"')
    receipt_write = src.index("idbAdd(db, CUSTODY_RECEIPTS", exact_assertion)
    receipt_readback = src.index("idbGet(db, CUSTODY_RECEIPTS, objectKey)", receipt_write)
    assert object_write < object_readback < exact_assertion < receipt_write < receipt_readback
    assert 'fail("custody exact-byte readback hash mismatch")' in src
    assert 'fail("custody registry receipt readback mismatch")' in src
    assert 'tvc_admission_completed: false' in src
    assert 'post_restart_exact_byte_proof_observed: false' in src
    assert 'broader_hil_lifecycle_complete: false' in src


def test_existing_portable_bridge_loads_generated_intr_and_custody_without_second_runtime():
    bridge = (BOOT / "hil-portable-state-bridge.js").read_text(encoding="utf-8")
    worker = (BOOT / "service-worker.js").read_text(encoding="utf-8")
    assert 'importScripts("../assets/generated/site-browser-intr-connectors.js")' in bridge
    assert 'importScripts("./hil-browser-receiver.js")' in bridge
    assert 'importScripts("./hil-browser-esrl-lease.js")' in bridge
    assert 'importScripts("./hil-browser-custody.js")' in bridge
    assert 'CACHE_NAME = "stegos-web-bootstrap-v16"' in worker
    assert (BOOT / "hil-custody-activate.html").is_file()
    assert "indexedDB.deleteDatabase" not in worker


def test_custody_page_auto_continues_only_from_exact_retained_esrl_and_pending_packet():
    page = (BOOT / "hil-custody-activate.html").read_text(encoding="utf-8")
    assert 'var LEASE_KEY="stegos-hil-esrl-last-success-v1"' in page
    assert 'var RECORD_KEY="stegverse.hil.submissions.v1"' in page
    assert 'var RESULT_KEY="stegos-hil-custody-last-success-v1"' in page
    assert 'row.state==="INTR_TRANSPORT_PENDING"' in page
    assert 'row.local_pretransport_staged===true' in page
    assert 'row.response_storage_verified===true' in page
    assert 'if(!restoreResult()){setTimeout(execute,0);}' in page
    assert 'value.custody_state!=="EXACT_BYTES_PERSISTED"' in page
    assert 'value.tvc_admission_completed!==false' in page
    assert 'value.post_restart_exact_byte_proof_observed!==false' in page
    assert 'Copy evidence JSON' in page
    assert 'Download evidence JSON' in page


def test_custody_page_canonicalizes_http_to_https_before_any_retained_state_read():
    page = (BOOT / "hil-custody-activate.html").read_text(encoding="utf-8")
    guard = page.index('if(canonicalizeSecureOrigin()){return;}')
    first_state_read = page.index('localStorage.getItem(key)')
    assert 'location.protocol==="http:"&&location.hostname==="stegverse.org"' in page
    assert 'location.replace("https://stegverse.org"+location.pathname+location.search+location.hash);' in page
    assert guard < first_state_read
