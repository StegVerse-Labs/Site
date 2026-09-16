from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "intr-service-worker.js"
BASE = ROOT / "intr-service-worker-base-v1.js"
EXTENSION = ROOT / "intr-canonical-work-extension.js"
LAUNCHER = ROOT / "stegos-bootstrap" / "canonical-work-runtime-consumption.js"
PROFILE_BRIDGE = ROOT / "stegos-bootstrap" / "canonical-work-root-profile-bridge.js"
PAGE = ROOT / "stegos-bootstrap" / "canonical-work-runtime-consumption.html"

GOAL = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001"
PARENT = "STEG-BROWSER-RUNTIME-MATERIALIZATION-REMEDIATION-001"
COSV = "40000100100000"
NONCE = "STEG-BROWSER-MANIFEST-INTR-INGRESS-EXECUTION-001-20260915T142500Z"
MANIFEST_SHA256 = "fcde63451bf612df8f3b2b62fa6766670dc880f2fcb66605680a2af6f2096f74"
DEST = "StegBrowser:ManifestInvocation"


def test_root_intr_worker_is_same_scope_modular_extension_not_parallel_runtime():
    wrapper = WRAPPER.read_text(encoding="utf-8")
    base = BASE.read_text(encoding="utf-8")
    assert 'importScripts("/intr-service-worker-base-v1.js")' in wrapper
    assert 'importScripts("/intr-canonical-work-extension.js")' in wrapper
    assert 'u.pathname==="/intr/materialization"' in base
    assert 'runtime_surface:"CURRENT_USER_IPHONE_SERVICE_WORKER"' in base
    assert 'self.addEventListener("fetch"' in base
    assert wrapper.count("importScripts") == 2


def test_existing_extension_is_rebound_to_active_manifest_invocation_only():
    text = EXTENSION.read_text(encoding="utf-8")
    for expected in (
        GOAL,
        PARENT,
        COSV,
        NONCE,
        MANIFEST_SHA256,
        DEST,
        'DOWNSTREAM_OWNER = "StegVerse-Labs/.github#1952"',
        'INGRESS_SCHEMA = "stegverse.stegbrowser-intr-materialization-ingress/v1"',
        'BINDING_SCHEMA = "stegverse.stegbrowser-universal-intr-invocation-binding/v1"',
        'current_device_ingress_observed: true',
        'runtime_surface: "CURRENT_USER_IPHONE_SERVICE_WORKER"',
        'claim_or_fence_minted: false',
        'workercoordinator_claim_observed: false',
        'workercoordinator_fence_observed: false',
        'credential_authority: "TV/TVC"',
        'github_token_runtime_authority: "NONE"',
        'authority_effect: "NONE_INGRESS_ONLY"',
    ):
        assert expected in text
    assert 'profiles.splice(retired, 1)' in text
    assert 'profiles.push("StegBrowser:ManifestInvocation")' in text
    assert "GITHUB_TOKEN" not in text
    assert "ACTIONS_RUNTIME_TOKEN" not in text
    assert "authorization" not in text.lower()


def test_launcher_preserves_immutable_nonce_and_registered_node_write_once_outbox():
    text = LAUNCHER.read_text(encoding="utf-8")
    for expected in (
        GOAL,
        PARENT,
        COSV,
        NONCE,
        MANIFEST_SHA256,
        DEST,
        'NODE_DB = "stegos-node-v1"',
        'NODE_OUTBOX = "intr_outbox"',
        'LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY',
        'STEGVERSE_INTR_LOCAL_TRIGGER',
        'navigator.serviceWorker.register("/intr-service-worker.js", { scope: "/" })',
        'stegverse.stegbrowser-universal-intr-invocation-binding/v1',
        'stegverse.universal-intr-materialization-request/v1',
        'stegverse.stegbrowser-intr-materialization-ingress/v1',
        'INGRESS_ADMITTED',
        'current-iPhone StegBrowser ingress not observed',
        'workercoordinator_claim_pending: true',
        'event_ephemeral_runtime_pending: true',
        'a4_ingress_pending: true',
        'round_trip_1_started: false',
        'repository_mutation_claimed: false',
        'completion_claimed: false',
    ):
        assert expected in text
    assert 'randomHex' not in text
    assert 'sha256HexText(NONCE)' in text
    assert 'materializationId = "STBR-MAT-" + nonceHash.slice(0, 24)' in text
    assert 'resident_request_sweep_required: false' in text
    assert 'control_plane_source_package_required: false' in text


def test_root_profile_probe_still_uses_same_root_worker_scope():
    wrapper = WRAPPER.read_text(encoding="utf-8")
    bridge = PROFILE_BRIDGE.read_text(encoding="utf-8")
    page = PAGE.read_text(encoding="utf-8")
    assert 'data.type !== "STEGVERSE_INTR_PROFILE_QUERY"' in wrapper
    assert 'profile: profile()' in wrapper
    assert 'navigator.serviceWorker.getRegistration("/")' in bridge
    assert 'worker.postMessage({ type: "STEGVERSE_INTR_PROFILE_QUERY" }' in bridge
    assert 'url.pathname === "/intr/profile"' in bridge
    assert 'canonical-work-root-profile-bridge.js' in page
    assert page.index('canonical-work-root-profile-bridge.js') < page.index('canonical-work-runtime-consumption.js')
    assert 'fetch("/intr/profile"' in LAUNCHER.read_text(encoding="utf-8")


def test_user_surface_promotes_only_a1_a2_ingress_evidence():
    text = PAGE.read_text(encoding="utf-8")
    assert GOAL in text
    assert NONCE in text
    assert "Execute / observe unchanged invocation" in text
    assert "No runtime predicate promoted." in text
    assert 'result.state==="INGRESS_ADMITTED"' in text
    assert 'state.textContent="A1_A2_INGRESS_ADMITTED_A3_A4_PENDING"' in text
    assert 'state.textContent="FAIL_CLOSED"' in text
    assert 'get("autostart")==="1"' in text
