from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "stegos-node" / "sv-dn1-resident-observation.html"


def test_sv_dn1_browser_resident_observation_contract():
    text = PAGE.read_text(encoding="utf-8")
    required = [
        "Receipt #1 is required",
        "https://huggingface.co/api/models/Qwen/Qwen3-8B",
        "stegverse.sv-dn1.source-capture/v1",
        "stegverse.sv-dn1.interlock-exchange/v1",
        "stegverse.sv-dn1.intr-runtime-receipt/v1",
        "STEGVERSE-UNIVERSAL-INTR-TRANSPORT-001",
        "stegverse.universal-intr.adjacent-hop/v1",
        "EXTERNAL_SYSTEM",
        "STEGOS_ECOSYSTEM",
        "SV_DN1_RESIDENT_SOURCE_CAPTURE_COMPLETE",
        "AUTHENTIC_REGISTERED_BROWSER_NODE",
        "runtime_activation_claimed:false",
        "production_interlock_runtime_activated:false",
        "sdk_admitted:false",
        "github_token_used:false",
        "repository_writeback_performed:false",
        "Export evidence bundle",
    ]
    for marker in required:
        assert marker in text, marker


def test_browser_lane_does_not_embed_provider_or_github_credentials():
    text = PAGE.read_text(encoding="utf-8")
    forbidden = ["HF_TOKEN", "HUGGINGFACE_TOKEN", "GITHUB_TOKEN", "GH_TOKEN", "Authorization: Bearer"]
    for marker in forbidden:
        assert marker not in text, marker
