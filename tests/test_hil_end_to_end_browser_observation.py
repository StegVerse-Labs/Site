from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegos-node" / "hil-end-to-end-observation.html"


def test_hil_observation_probe_preserves_authentic_observation_contract():
    text = PAGE.read_text(encoding="utf-8")
    required = [
        'openExisting(2500)',
        'stegos-web-bootstrap-v1',
        'stegos.web_bootstrap_evidence_bundle.v1',
        'existing_node_reused:true',
        'new_node_identity_minted:false',
        'AUTHENTIC_ESTABLISHED_STEGVERSE_WEB_NODE',
        'HIL-END-TO-END-OBSERVATION-001',
        '/api/hil/submissions',
        'HIL-RESPONSE-PROVENANCE-v1.1',
        'HIL-RECEIVER-RECEIPT-v2',
        'stegverse.universal-intr-transport/v1',
        'DEVICE_SYSTEM',
        'STEGOS_ECOSYSTEM',
        'HIL:Ingress',
        'HIL:Custody',
        'TVC:HIL-Lifecycle',
        'EXACT_BYTES_PERSISTED',
        'RECORDED',
        'HIL_CUSTODY_TVC_INTERLOCK_ADMISSION',
        'stegos.web_task_claim_receipt.v1',
        'stegos.web_task_terminal_receipt.v1',
        'stegos.web_task_reconstruction_receipt.v1',
        'stegverse.hil.canonical-observation-evidence/v1',
        'state:"OBSERVED"',
        'exact_byte_reconstruction:"PASS"',
        'tvc_receiving_receipt_observed:false',
        'receiver_restart_reconstruction_observed:false',
        'participant_research_submission:false',
        'runtime_activation_claimed:false',
    ]
    for marker in required:
        assert marker in text, marker


def test_hil_observation_probe_is_non_authorizing_and_credential_free():
    text = PAGE.read_text(encoding="utf-8")
    for marker in [
        "GITHUB_TOKEN",
        "GH_TOKEN",
        "HF_TOKEN",
        "HUGGINGFACE_TOKEN",
        "Authorization: Bearer",
    ]:
        assert marker not in text, marker
    assert 'credential_authority:"TV/TVC"' in text
    assert 'global_workercoordinator_authority:false' in text
    assert 'carrier_granted_authority:false' in text
    assert 'authority_effect:"NONE"' in text


def test_hil_observation_probe_requires_real_receiver_and_retrieval_evidence():
    text = PAGE.read_text(encoding="utf-8")
    assert 'fetch(INGRESS,{method:"POST"' in text
    assert 'if(!response.ok)throw Error' in text
    assert 'receipt.submitted_file_sha256!==digest' in text
    assert 'fetch("/api/hil/submissions/"+encodeURIComponent(receipt.submission_id)+"/content"' in text
    assert 'if(returnedDigest!==digest)throw Error("exact byte reconstruction mismatch")' in text
    assert 'status.textContent="NOT OBSERVED — "+e.message' in text
