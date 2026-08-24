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
    assert module.EXPECTED["stegos-bootstrap/device-local-autostart.js"] == "3927e2aa650f3267c53af73f3ef8bea2379805b9"


def test_projection_validator_passes(tmp_path, monkeypatch):
    report = tmp_path / "report.json"
    monkeypatch.setattr(module, "REPORT", report)
    assert module.main() == 0
    payload = json.loads(report.read_text(encoding="utf-8"))
    assert payload["status"] == "PASS"
    assert payload["exact_projection"] is True
    assert payload["source_commit"] == "fc23a8b1cb2f350ba44c73dd868738f2fd6cb73d"
    assert payload["credential_authority"] == "TV/TVC"
    assert payload["non_tv_tvc_secret_or_token_used"] is False
    assert payload["render_production_authority"] is False
    assert payload["github_token_runtime_authority"] is False
    assert payload["hosted_ci_activation_authority"] is False
    assert payload["site_authority_effect"] == "TRANSPORT_MATERIALIZATION_ONLY"
    assert payload["cross_context_device_root_creation_atomic"] is True
    assert payload["duplicate_root_receipt_on_lost_race_allowed"] is False


def test_cross_context_device_root_creation_is_create_if_absent_and_reuses_winner():
    source = (ROOT / "stegos-bootstrap" / "device-local-autostart.js").read_text(encoding="utf-8")
    assert "function addMetaIfAbsent(db, key, value)" in source
    assert 'objectStore(META_STORE).add({ key: key, value: value })' in source
    assert 'req.error.name === "ConstraintError"' in source
    assert "then(function (wonCreate)" in source
    assert "if (!wonCreate)" in source
    assert "return getMeta(db, DEVICE_ROOT_KEY)" in source
    assert "device continuity root race lost without persisted winner" in source

    winning_branch = source.split("then(function (wonCreate)", 1)[1]
    losing_branch = winning_branch.split("return appendReceipt(db", 1)[0]
    assert "appendReceipt" not in losing_branch
    assert "getMeta(db, DEVICE_ROOT_KEY)" in losing_branch


def test_projected_activation_is_local_and_fail_closed_for_missing_inference():
    source = (ROOT / "stegos-bootstrap" / "stegos-bootstrap.js").read_text(encoding="utf-8")
    activation = source.split("function activateEcosystemChat()", 1)[1].split("function replayJournal()", 1)[0]
    assert "fetch(" not in activation
    assert "XMLHttpRequest" not in activation
    assert "local_node_runtime_ready: true" in activation
    assert "local_receipt_journal_ready: true" in activation
    assert "external_non_stegverse_machine_used_for_activation: false" in activation
    assert 'inference_actions_state: "FAIL_CLOSED_UNTIL_STEGVERSE_MODEL_EVIDENCE"' in activation
