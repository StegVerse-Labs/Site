from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegos-node" / "sv-dn1-resident-observation-v3.html"

def test_nonblocking_continuity_recovery_contract():
    text = PAGE.read_text(encoding="utf-8")
    required = [
        'type="file"',
        'openExisting(2500)',
        'IndexedDB probe timed out',
        'stegos-web-bootstrap-v1',
        'stegos.web_bootstrap_evidence_bundle.v1',
        'existing_node_reused:true',
        'new_node_identity_minted:false',
        'AUTHENTIC_ESTABLISHED_STEGVERSE_WEB_NODE',
        'https://huggingface.co/api/models/Qwen/Qwen3-8B',
        'STEGVERSE-UNIVERSAL-INTR-TRANSPORT-001',
        'EXTERNAL_SYSTEM',
        'STEGOS_ECOSYSTEM',
        'stegos.web_task_reconstruction_receipt.v1',
        'state:"OBSERVED"',
    ]
    for marker in required:
        assert marker in text, marker


def test_no_provider_or_github_credentials_embedded():
    text = PAGE.read_text(encoding="utf-8")
    for marker in ["HF_TOKEN", "HUGGINGFACE_TOKEN", "GITHUB_TOKEN", "GH_TOKEN", "Authorization: Bearer"]:
        assert marker not in text, marker
