from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOT = ROOT / "stegos-bootstrap"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_invoker_reuses_existing_resident_task_and_has_no_device_or_claim_gate():
    source = read(BOOT / "erl-active-research-run.js")
    assert 'ENDPOINT = "./resident-task"' in source
    assert 'profile_id: PROFILE_ID' in source
    assert 'task_id: TASK_ID' in source
    assert 'component_task_id: COMPONENT_TASK_ID' in source
    assert 'cosv_task_vector: COSV' in source
    assert 'credential_authority: "TV/TVC"' in source
    assert 'github_token_runtime_authority: "NONE"' in source
    assert 'heartbeat_granted_authority: false' in source
    assert 'provider_operation_reexecution_authorized: false' in source
    assert 'external_non_stegverse_machine_required: false' in source
    assert 'device_id' not in source
    assert 'node_id' not in source
    assert 'execution_surface' not in source
    assert 'claim_id' not in source
    assert 'fencing_token' not in source


def test_invoker_refuses_blind_consequence_resubmission():
    source = read(BOOT / "erl-active-research-run.js")
    assert 'stegverse.erl.same-device-portable-execution-receipt/v1' in source
    assert 'ALREADY_OBSERVED_NO_RESUBMISSION' in source
    assert 'runtime_submission_performed: false' in source
    assert 'complete_three_hop_chain_verified !== true' in source
    assert 'durable_payload_readback_verified !== true' in source
    assert 'retainedExecution().then' in source


def test_master_records_projection_uses_authentic_retained_chain_only():
    source = read(BOOT / "erl-active-research-run.js")
    assert 'stegverse.master-records.universal-intr-receipt-chain-evidence/v1' in source
    assert 'boundary_path: ["EXTERNAL_SYSTEM", "STEGOS_ECOSYSTEM", "DEVICE_SYSTEM", "KV"]' in source
    assert 'receipts: receipt.hop_receipts' in source
    assert 'readback_hash: receipt.kv_payload_readback_sha256' in source
    assert 'exact_bytes_readback_verified: receipt.durable_payload_readback_verified === true' in source
    assert 'provider_proof_binding: receipt.provider_proof_binding' in source
    assert 'synthetic_evidence: false' in source


def test_runner_is_machine_owned_auto_materialization_not_human_authority_control():
    page = read(BOOT / "erl-active-research-run.html")
    assert 'StegOSERLActiveResearchInvoker.submit()' in page
    assert 'DOMContentLoaded' in page
    assert 'EXECUTING_MACHINE_GOVERNED_TRANSITION' in page
    assert 'does not discover or verify a device and does not mint authority' in page
    assert 'Copy custody input' in page
    assert 'Run ERL' not in page
