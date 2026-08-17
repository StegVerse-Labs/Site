import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "stegos_projection", ROOT / "scripts" / "check_stegos_ipod_bootstrap_projection.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


def test_exact_projected_blob_identity():
    for relative, expected in module.EXPECTED.items():
        assert module.git_blob_sha((ROOT / relative).read_bytes()) == expected


def test_projection_validator_passes(tmp_path, monkeypatch):
    report = tmp_path / "report.json"
    monkeypatch.setattr(module, "REPORT", report)
    assert module.main() == 0
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert payload["exact_projection"] is True
    assert payload["source_commit"] == "799e0f3fd2766a32cbf0720384db11f066d8e9b8"
    assert payload["credential_authority"] == "TV/TVC"
    assert payload["non_tv_tvc_secret_or_token_used"] is False
    assert payload["render_production_authority"] is False
    assert payload["github_token_runtime_authority"] is False
    assert payload["hosted_ci_activation_authority"] is False
    assert payload["site_authority_effect"] == "TRANSPORT_MATERIALIZATION_ONLY"
    assert payload["physical_activation_owner"] == "StegVerse-Labs/StegOS#13"


def test_projected_activation_is_local_and_fail_closed_for_missing_inference():
    source = (ROOT / "stegos-bootstrap" / "stegos-bootstrap.js").read_text(encoding="utf-8")
    activation = source.split("function activateEcosystemChat()", 1)[1].split("function replayJournal()", 1)[0]
    assert "fetch(" not in activation
    assert "XMLHttpRequest" not in activation
    assert "local_node_runtime_ready: true" in activation
    assert "local_receipt_journal_ready: true" in activation
    assert "external_non_stegverse_machine_used_for_activation: false" in activation
    assert 'inference_actions_state: "FAIL_CLOSED_UNTIL_STEGVERSE_MODEL_EVIDENCE"' in activation
