from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_stegos_node_projection_contract() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
    sw = (ROOT / "stegos-node" / "service-worker.js").read_text(encoding="utf-8")

    assert index.count('id="register-device"') == 1
    assert "Register Device" in index
    assert "Last StegOS Network Sync" in index
    assert "Last Personal KV Sync" in index
    assert "Local Receipt Head" in index
    assert "Device History" in index
    assert 'id="registration-actions"' in index
    assert 'id="registered-device-actions"' in index
    assert 'id="check-current-registration"' in index
    assert "Check Current Registration" in index
    assert "registrationActions.hidden = !unregistered" in index
    assert "registeredDeviceActions.hidden = !registered" in index
    assert "Canonical Receipt #1 detected. This device is already registered." in index
    assert 'validatedHistory().then(function (history)' in index
    assert 'Registration confirmed · " + history.registration.node_id + " · Receipt #1"' in index

    for marker in (
        'stegos.node_handoff_receipt.v1',
        'receipt_number: 1',
        'transition: "NODE_REGISTERED"',
        'prior_state: "UNREGISTERED"',
        'resulting_state: "REGISTERED"',
        'continuity_parent: "GENESIS"',
        'credential_authority: "TV/TVC"',
        'hardware_attestation_claimed: false',
        'last_personal_kv_sync',
        'last_stegos_network_sync',
        'section_views_are_filtered_projections: true',
        'competing_logs_allowed: false',
        'current_network_required: false',
    ):
        assert marker in js

    for marker in ("navigator.userAgent", "serialNumber", "GITHUB_TOKEN", "RENDER_API"):
        assert marker not in js

    assert './index.html' in sw
    assert './stegos-node.js' in sw
    assert './kv-readiness-snapshot.json' in sw
    assert './manifest.webmanifest' in sw


def test_live_observer_is_exact_https_and_non_authorizing() -> None:
    observer = (ROOT / "scripts" / "check_stegos_node_projection.py").read_text(encoding="utf-8")
    assert '--live-url' in observer
    assert '--require-offline-proof' in observer
    assert 'parsed.scheme != "https"' in observer
    assert 'urljoin(base_url, "stegos-node.js")' in observer
    assert 'urljoin(base_url, "service-worker.js")' in observer
    assert 'urljoin(base_url, "manifest.webmanifest")' in observer
    assert 'urljoin(base_url, "kv-readiness-snapshot.json")' in observer
    assert 'STEGOS_NODE_OFFLINE_PROOF_SOURCE_PASS' in observer
    assert 'STEGOS_NODE_OFFLINE_PROOF_PUBLIC_OBSERVATION_PASS' in observer
    assert 'AUTHORITY_EFFECT=NONE' in observer
    assert 'PHYSICAL_NODE_ACTIVATION_CLAIMED=false' in observer
    assert 'NETWORK_ACTIVATION_CLAIMED=false' in observer


def test_hosted_live_url_task_invokes_exact_stegos_node_observer() -> None:
    runner = (ROOT / "scripts" / "run_site_task.py").read_text(encoding="utf-8")
    assert '"scripts/check_stegos_node_projection.py"' in runner
    assert '"--live-url"' in runner
    assert '"https://stegverse.org/stegos-node/"' in runner
    assert runner.index('"scripts/check_stegos_node_projection.py"') > runner.index("def live_url()")


def test_independent_public_observer_stages_source_then_deployed_capability() -> None:
    workflow = (ROOT / ".github" / "workflows" / "stegos-node-public-observation.yml").read_text(encoding="utf-8")
    assert "github.event_name == 'pull_request'" in workflow
    assert "github.event_name != 'pull_request'" in workflow
    assert "python scripts/check_stegos_node_projection.py | tee" in workflow
    assert "https://stegverse.org/stegos-node/" in workflow
    assert "--require-offline-proof" in workflow
    assert "for attempt in $(seq 1 12)" in workflow
    assert "stegos.node_public_observation_receipt.v1" in workflow
    assert "source_validation_passed" in workflow
    assert "offline_proof_capability_required" in workflow
    assert "observation_passed" in workflow
    assert "STEGOS_NODE_KV_INTR_BROWSER_APPLY_SOURCE_PASS" in workflow
    assert "STEGOS_NODE_KV_INTR_BROWSER_APPLY_PUBLIC_OBSERVATION_PASS" in workflow
    assert "kv_intr_browser_apply_required': True" in workflow
    assert "kv_intr_browser_apply_source_passed" in workflow
    assert "kv_intr_browser_apply_public_observation_passed" in workflow
    assert "docs/STEGOS_KV_INTR_BROWSER_APPLY_RECONCILIATION_MIRROR_HANDOFF.md" in workflow
    assert "data/session-work-claims.d/site-stegos-kv-intr-browser-apply-549.json" in workflow
    assert "authority_effect': 'NONE'" in workflow
    assert "physical_node_activation_claimed': False" in workflow
    assert "network_activation_claimed': False" in workflow
    assert "credential_requirement': 'NONE'" in workflow
    assert "actions/upload-artifact@v4" in workflow
    assert "secrets." not in workflow


def test_offline_reload_proof_is_local_bounded_evidence() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")

    assert 'id="offline-reload-proof"' in index
    assert 'offline_reload_proof: history.offline_reload_proof || null' in index
    assert 'network_activation_claimed: false' in index

    for marker in (
        'OFFLINE_PROOF_KEY = "offline-reload-proof"',
        'stegos.node_offline_reload_proof.v1',
        'navigator.serviceWorker && navigator.serviceWorker.controller',
        'navigator.onLine === false',
        'service_worker_controlled: true',
        'offline_observed: true',
        'current_network_required: false',
        'network_topology_claimed: false',
        'heartbeat_interlock_observation_verified: false',
        'physical_activation_claimed: false',
        'network_activation_claimed: false',
        'credential_authority: "TV/TVC"',
        'authority_effect: "NONE"',
        'proof_sha256',
        'validateOfflineReloadProof',
        'recordOfflineReloadProof',
    ):
        assert marker in js

    assert 'network_topology_claimed: true' not in js
    assert 'physical_activation_claimed: true' not in js
    assert 'network_activation_claimed: true' not in js


def test_node_evidence_export_is_bounded_and_non_authorizing() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")
    assert 'id="export-node-evidence"' in index
    assert 'stegos.node_physical_evidence_export.v1' in index
    assert 'window.StegOSNodeProjection.historyProjection()' in index
    assert 'window.StegOSNodeProjection.validateOfflineReloadProof' in index
    assert 'offline_reload_proof: history.offline_reload_proof || null' in index
    assert 'raw_registration_random_bytes_included: false' in index
    assert 'hardware_attestation_claimed: false' in index
    assert 'physical_activation_claimed: false' in index
    assert 'network_activation_claimed: false' in index
    assert 'authority_effect: "NONE"' in index
    assert 'credential_authority: "TV/TVC"' in index
    assert 'heartbeat_authority: "StegVerse-Labs/.github"' in index
    assert 'Receipt #1 is required before evidence export' in index
    assert 'new Blob' in index
    assert 'link.download = "stegos-node-evidence-"' in index


def test_kv_capability_shell_projection_is_read_only_and_fail_closed() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
    sw = (ROOT / "stegos-node" / "service-worker.js").read_text(encoding="utf-8")
    observer = (ROOT / "scripts" / "check_stegos_node_projection.py").read_text(encoding="utf-8")

    for marker in (
        'id="kv-capability-shell"',
        "KnowledgeVault Capabilities",
        'id="kv-capability-local-ready"',
        'id="kv-capability-local-blocked"',
        'id="kv-capability-governed-ready"',
        'id="kv-capability-governed-blocked"',
        'id="kv-available-modules"',
        'id="kv-available-services"',
        'id="kv-blocked-modules"',
        'id="kv-blocked-services"',
    ):
        assert marker in index

    for marker in (
        'stegos.site.kv_capability_shell_projection.v1',
        '"source_stegos_view_schema": "stegos.kv_capability_shell_view.v1"',
        '"source_stegos_merge": "4dad89be44e472eb4a5db10bfd294ded803d1456"',
        '"entry_count": 46',
        '"local_ready": 45',
        '"local_blocked": 1',
        '"governed_ready": 0',
        '"governed_blocked": 46',
        'BLOCKED_CURRENT_IDENTITY',
        '"activation_control_present": false',
        '"kv_state_mutation_available": false',
        '"provider_execution_available": false',
        '"activation_performed": false',
        'authority_effect: "NONE"',
        'renderKvCapabilityShell',
        'disabled governed control must expose blockers',
    ):
        assert marker in js

    assert js.count('"entry_type":') == 46
    assert js.count('"entry_id":') == 46
    assert js.count('"install_state": "INSTALLED_INACTIVE"') == 46
    assert js.count('"enabled": false') == 46
    assert '"enabled": true' not in js
    assert 'stegos-node-shell-v5-hil-intr-local-outbox' in sw
    assert './kv-readiness-snapshot.json' in sw

    assert 'STEGOS_NODE_KV_CAPABILITY_SHELL_SOURCE_PASS' in observer
    assert 'STEGOS_NODE_KV_CAPABILITY_SHELL_PUBLIC_OBSERVATION_PASS' in observer
    assert 'STEGOS_NODE_KV_READINESS_BROWSER_STATE_SOURCE_PASS' in observer
    assert 'STEGOS_NODE_KV_READINESS_BROWSER_STATE_PUBLIC_OBSERVATION_PASS' in observer
    assert 'AUTHORITY_EFFECT=NONE' in observer
    assert 'PHYSICAL_NODE_ACTIVATION_CLAIMED=false' in observer
    assert 'NETWORK_ACTIVATION_CLAIMED=false' in observer



def test_kv_readiness_browser_state_is_persisted_fail_closed_and_offline_cached() -> None:
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
    sw = (ROOT / "stegos-node" / "service-worker.js").read_text(encoding="utf-8")
    snapshot_text = (ROOT / "stegos-node" / "kv-readiness-snapshot.json").read_text(encoding="utf-8")
    import json
    snapshot = json.loads(snapshot_text)

    assert snapshot["schema"] == "stegverse.kv.activation-readiness-snapshot/v1"
    assert snapshot["entry_count"] == 46
    assert len(snapshot["entries"]) == 46
    assert snapshot["module_count"] == 13
    assert snapshot["service_count"] == 33
    assert snapshot["summary"] == {
        "local_ready": 45,
        "local_blocked": 1,
        "governed_ready": 0,
        "governed_blocked": 46,
    }
    assert snapshot["production_interlock_runtime_activated"] is False
    assert snapshot["activation_performed"] is False
    assert snapshot["authority_effect"] == "NONE"

    for marker in (
        'KV_READINESS_STATE_KEY = "kv-readiness-device-state"',
        'KV_READINESS_SNAPSHOT_URL = "./kv-readiness-snapshot.json"',
        'stegos.site.kv_device_readiness_state.v1',
        'stegos.kv_readiness_update_envelope.v1',
        'validateKvReadinessSnapshot',
        'siteProjectionFromKvReadinessSnapshot',
        'initializeKvReadinessBrowserState',
        'applyKvReadinessUpdate',
        'validateKvReadinessBrowserState',
        'stale or replayed KV readiness update',
        'KV readiness envelope prior digest mismatch',
        'KV readiness envelope successor digest mismatch',
        'transport_delivery_performed: false',
        'interlock_delivery_admission_observed: false',
        'kv_mutation_performed: false',
        'provider_operation_authorized: false',
        'execution_authority: "NONE"',
        'authority_effect: "NONE"',
    ):
        assert marker in js

    assert 'stegos-node-shell-v5-hil-intr-local-outbox' in sw
    assert './kv-readiness-snapshot.json' in sw


def test_browser_readiness_update_preserves_local_transport_neutrality_and_authority_boundary() -> None:
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")

    local_start = js.index("function buildKvReadinessBrowserState")
    local_end = js.index("function validateKvReadinessBrowserState")
    local_state_builder = js[local_start:local_end]
    assert "transport_delivery_performed: false" in local_state_builder
    assert "interlock_delivery_admission_observed: false" in local_state_builder
    assert "transport_delivery_performed: true" not in local_state_builder
    assert "interlock_delivery_admission_observed: true" not in local_state_builder

    for prohibited in (
        'kv_mutation_performed: true',
        'activation_performed: true',
        'provider_operation_authorized: true',
        'execution_authority: "ALLOW"',
    ):
        assert prohibited not in js

    assert 'KV readiness update may not claim transport delivery' in js
    assert 'KV readiness update may not claim Interlock delivery' in js
    assert 'KV readiness update may not perform activation' in js
    assert 'KV readiness update may not mutate KV' in js
    assert 'KV readiness update may not authorize provider operation' in js
    assert 'KV readiness update execution authority must be NONE' in js
    assert 'KV readiness update authority_effect must be NONE' in js


def test_admitted_intr_readiness_browser_apply_is_separate_fail_closed_path() -> None:
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
    observer = (ROOT / "scripts" / "check_stegos_node_projection.py").read_text(encoding="utf-8")
    sw = (ROOT / "stegos-node" / "service-worker.js").read_text(encoding="utf-8")

    for marker in (
        'stegverse.intr.hop_receipt/v1',
        'stegos.kv_readiness_intr_delivery_admission.v1',
        'stegos.site.kv_readiness_admitted_device_apply.v1',
        'validateKvReadinessIntrReceipt',
        'validateKvReadinessIntrDeliveryAdmission',
        'applyAdmittedKvReadinessDelivery',
        'KV readiness InTr hop must be KV->DEVICE',
        'KV readiness InTr direction must be FORWARD',
        'KV readiness InTr hop_index must be 1',
        'KV readiness InTr boundary must be VERIFIED',
        'KV readiness InTr transition must be RECEIVED',
        'KV readiness InTr payload does not bind exact envelope',
        'KV readiness InTr receipt canonical field mismatch',
        'KV readiness delivery admission canonical field mismatch',
        'stale or replayed admitted KV readiness delivery',
        'browser readiness state must remain transport-neutral',
        'transport_delivery_performed: true',
        'interlock_delivery_admission_observed: true',
        'local_state_refresh_performed: true',
        'kv_mutation_performed: false',
        'activation_performed: false',
        'provider_operation_authorized: false',
        'execution_authority: "NONE"',
        'authority_effect: "NONE"',
    ):
        assert marker in js

    assert "applyKvReadinessUpdate: applyKvReadinessUpdate" in js
    assert "applyAdmittedKvReadinessDelivery: applyAdmittedKvReadinessDelivery" in js
    assert "STEGOS_NODE_KV_INTR_BROWSER_APPLY_SOURCE_PASS" in observer
    assert "STEGOS_NODE_KV_INTR_BROWSER_APPLY_PUBLIC_OBSERVATION_PASS" in observer
    assert "stegos-node-shell-v5-hil-intr-local-outbox" in sw


def test_hil_intr_local_outbox_is_registered_write_once_and_non_delivery() -> None:
    index = (ROOT / "stegos-node" / "index.html").read_text(encoding="utf-8")
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
    sw = (ROOT / "stegos-node" / "service-worker.js").read_text(encoding="utf-8")
    observer = (ROOT / "scripts" / "check_stegos_node_projection.py").read_text(encoding="utf-8")

    assert 'id="hil-intr-outbox"' in index
    assert "HIL InTr Local Outbox" in index
    assert "do not advance the Network Sync marker" in index

    for marker in (
        'DB_VERSION = 2',
        'INTR_OUTBOX = "intr_outbox"',
        'HIL_DB_NAME = "stegverse-hil-v3"',
        'HIL_STORE_NAME = "response_files"',
        'HIL_RECORD_KEY = "stegverse.hil.submissions.v1"',
        'stegverse.universal-intr-materialization-request/v1',
        'stegos.node_intr_outbox_entry.v1',
        'LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY',
        'pendingHilMaterializationIds',
        'validateHilMaterializationRequest',
        'getIntrOutbox',
        'putIntrOutbox',
        'importPendingHilIntrToNodeOutbox',
        'reconcilePendingHilIntrOutbox',
        'Receipt #1 is required before HIL InTr outbox admission',
        'HIL materialization request hash mismatch',
        'HIL transport intent hash mismatch',
        'HIL payload binding mismatch',
        'HIL materialization identity mismatch',
        'HIL materialization payload_ref mismatch',
        'StegOS InTr outbox write-once collision',
        'network_delivery_observed: false',
        'runtime_materialization_observed: false',
        'receiver_receipt_observed: false',
        'tvc_receipt_observed: false',
        'request_grants_execution_authority: false',
        'claim_or_fence_minted: false',
        'credential_authority: "TV/TVC"',
        'GITHUB_RUNTIME_AUTHORITY_FIELD = "github" + "_token_runtime_authority"',
        'authority_effect: "NONE_LOCAL_CONTINUITY_ONLY"',
    ):
        assert marker in js

    importer_start = js.index("function importPendingHilIntrToNodeOutbox")
    importer_end = js.index("function validateGenesis")
    importer = js[importer_start:importer_end]
    assert "putMeta(NETWORK_SYNC_KEY" not in importer
    assert "network_delivery_observed: true" not in importer
    assert "runtime_materialization_observed: true" not in importer
    assert "receiver_receipt_observed: true" not in importer
    assert "tvc_receipt_observed: true" not in importer
    assert "claim_or_fence_minted: true" not in importer
    assert "request_grants_execution_authority: true" not in importer

    assert 'stegos-node-shell-v5-hil-intr-local-outbox' in sw
    assert "STEGOS_NODE_HIL_INTR_LOCAL_OUTBOX_SOURCE_PASS" in observer
    assert "STEGOS_NODE_HIL_INTR_LOCAL_OUTBOX_PUBLIC_SOURCE_PASS" in observer


def test_hil_intr_outbox_imports_only_explicitly_pending_participant_records() -> None:
    js = (ROOT / "stegos-node" / "stegos-node.js").read_text(encoding="utf-8")
    start = js.index("function pendingHilMaterializationIds")
    end = js.index("function getHilStagedPackets")
    selector = js[start:end]
    assert 'record.intr_materialization_state === "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION"' in selector
    assert 'request.state === "QUEUED_FOR_EVENT_EPHEMERAL_MATERIALIZATION"' in selector
    assert "SATISFIED_BY_DIRECT_RECEIVER_RECEIPT" not in selector
