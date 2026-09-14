from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "stegos-bootstrap"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_erl_profile_reuses_existing_resident_task_surface_and_canonical_assets():
    sw = read(BOOT / "service-worker.js")
    erl = read(BOOT / "erl-active-research-resident-task-extension.js")
    generated = read(ROOT / "assets/generated/site-browser-intr-connectors.js")
    package = read(BOOT / "workercoordinator-portable-device-kv.json")

    assert 'importScripts("./service-worker-v13-runtime.js")' in sw
    assert 'importScripts("./hil-portable-state-bridge.js")' in sw
    assert 'importScripts("../assets/generated/site-browser-intr-connectors.js")' in sw
    assert 'importScripts("./erl-active-research-resident-task-extension.js")' in sw
    assert './workercoordinator-portable-device-kv.json' in sw

    assert 'PROFILE_ID = "ERL_ACTIVE_RESEARCH_INTR_SAME_DEVICE_V1"' in erl
    assert 'PARENT_TASK_ID = "SS-ERL-ACTIVE-RESEARCH-INTR-RUNTIME-BINDING-001"' in erl
    assert 'COSV = "40000100100000"' in erl
    assert 'root.StegOSExternalResidentTask.execute = function' in erl
    assert 'StegVerseGeneratedInTr.buildReceipt' in erl
    assert 'portableStateStoreForPackage' in erl
    assert 'KV_STORE = "kv_files"' in erl
    assert 'exact_payload_bytes_transported: true' in erl
    assert 'durable_payload_readback_verified: kv.exact_readback_verified === true' in erl
    assert 'master_records_custody_observed: false' in erl
    assert 'provider_operation_attempted: false' in erl
    assert 'device_confirmation_performed: false' in erl
    assert 'device_discovery_performed: false' in erl
    assert 'device_presence_probe_performed: false' in erl

    assert 'StegVerseGeneratedInTr' in generated
    assert '"task_id": "SHWP-DEVICE-KV-INTR-OBSERVATION-001"' in package
    assert '"execution_surface": "CURRENT_USER_IPHONE"' in package


def test_erl_projection_adds_no_new_fetch_listener_or_device_gate():
    erl = read(BOOT / "erl-active-research-resident-task-extension.js")
    assert 'addEventListener("fetch"' not in erl
    assert "navigator" not in erl
    assert "userAgent" not in erl
    assert "Remote Desktop" not in erl
    assert 'external_non_stegverse_machine_required !== false' in erl
    assert 'second_user_device_required: false' in erl
