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
    assert './manifest.webmanifest' in sw


def test_live_observer_is_exact_https_and_non_authorizing() -> None:
    observer = (ROOT / "scripts" / "check_stegos_node_projection.py").read_text(encoding="utf-8")
    assert '--live-url' in observer
    assert '--require-offline-proof' in observer
    assert 'parsed.scheme != "https"' in observer
    assert 'urljoin(base_url, "stegos-node.js")' in observer
    assert 'urljoin(base_url, "service-worker.js")' in observer
    assert 'urljoin(base_url, "manifest.webmanifest")' in observer
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
    assert 'stegos-node-shell-v2-kv-capabilities' in sw

    assert 'STEGOS_NODE_KV_CAPABILITY_SHELL_SOURCE_PASS' in observer
    assert 'STEGOS_NODE_KV_CAPABILITY_SHELL_PUBLIC_OBSERVATION_PASS' in observer
    assert 'AUTHORITY_EFFECT=NONE' in observer
    assert 'PHYSICAL_NODE_ACTIVATION_CLAIMED=false' in observer
    assert 'NETWORK_ACTIVATION_CLAIMED=false' in observer
