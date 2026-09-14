from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRAPPER = ROOT / "intr-service-worker.js"
BASE = ROOT / "intr-service-worker-base-v1.js"
EXTENSION = ROOT / "intr-canonical-work-extension.js"
LAUNCHER = ROOT / "stegos-bootstrap" / "canonical-work-runtime-consumption.js"
PROFILE_BRIDGE = ROOT / "stegos-bootstrap" / "canonical-work-root-profile-bridge.js"
PAGE = ROOT / "stegos-bootstrap" / "canonical-work-runtime-consumption.html"
HANDOFF = ROOT / "docs" / "STEGBROWSER_RUNTIME_CONSUMPTION_SAME_DEVICE_INTR_MIRROR_HANDOFF.md"

TASK = "STEG-BROWSER-RUNTIME-CONSUMPTION-001"
COSV = "40000100100000"
REGISTRY_COMMIT = "f1a55fa4022e19b41f2a9f604978b08ece22f64c"


def test_root_intr_worker_is_same_scope_modular_extension_not_parallel_runtime():
    wrapper = WRAPPER.read_text(encoding="utf-8")
    base = BASE.read_text(encoding="utf-8")
    assert 'importScripts("/intr-service-worker-base-v1.js")' in wrapper
    assert 'importScripts("/intr-canonical-work-extension.js")' in wrapper
    assert 'u.pathname==="/intr/materialization"' in base
    assert 'runtime_surface:"CURRENT_USER_IPHONE_SERVICE_WORKER"' in base
    assert 'self.addEventListener("fetch"' in base
    assert wrapper.count("importScripts") == 2


def test_canonical_work_extension_is_exact_task_bound_and_non_authorizing():
    text = EXTENSION.read_text(encoding="utf-8")
    for expected in (
        TASK,
        COSV,
        REGISTRY_COMMIT,
        'REGISTRY_GENERATION = 19',
        'SELECTED_SUBSTRATE = "ADMITTED-EPHEMERAL-STEGOS-NODE"',
        'CANONICAL_WORK_OWNER = "STEGVERSE-CANONICAL-WORK-COORDINATION-001"',
        'CANONICAL_WORK_INGRESS_SCHEMA = "stegverse.canonical-work-intr-materialization-ingress/v1"',
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
    assert "GITHUB_TOKEN" not in text
    assert "ACTIONS_RUNTIME_TOKEN" not in text
    assert "authorization" not in text.lower()


def test_launcher_uses_registered_node_write_once_outbox_and_root_intr_message():
    text = LAUNCHER.read_text(encoding="utf-8")
    for expected in (
        TASK,
        COSV,
        REGISTRY_COMMIT,
        'NODE_DB = "stegos-node-v1"',
        'NODE_OUTBOX = "intr_outbox"',
        'LOCAL_OUTBOX_PENDING_NETWORK_DELIVERY',
        'STEGVERSE_INTR_LOCAL_TRIGGER',
        'navigator.serviceWorker.register("/intr-service-worker.js", { scope: "/" })',
        'CanonicalWork:Ingress',
        'INGRESS_ADMITTED',
        'current-iPhone ingress not observed',
        'workercoordinator_claim_pending: true',
        'repository_mutation_claimed: false',
        'self_build_completion_claimed: false',
    ):
        assert expected in text


def test_root_profile_probe_bypasses_nested_bootstrap_worker_scope_by_direct_message():
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


def test_user_surface_requires_runtime_evidence_before_self_build_started():
    text = PAGE.read_text(encoding="utf-8")
    assert "Start StegVerse Building StegVerse" in text
    assert "No runtime claim yet." in text
    assert 'result.state==="CANONICAL_WORK_INGRESS_ADMITTED_LOCAL_BUILD_ANALYSIS_EXECUTED"' in text
    assert 'state.textContent="STEGVERSE_SELF_BUILD_STARTED"' in text
    assert 'state.textContent="FAIL_CLOSED"' in text
    assert 'get("autostart")==="1"' in text


def test_handoff_keeps_workercoordinator_as_claim_fence_authority():
    text = HANDOFF.read_text(encoding="utf-8")
    assert TASK in text
    assert COSV in text
    assert "WorkerCoordinator remains the sole claim/fence authority" in text
    assert "Source, merge, GitHub Pages publication, or service-worker installation do not prove admission" in text
    assert "root InTr profile HTTP 404" in text
    assert "STEGVERSE_INTR_PROFILE_QUERY" in text
