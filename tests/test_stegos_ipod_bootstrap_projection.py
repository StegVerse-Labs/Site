import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# The checker is a wrapper that execs its implementation with
# __name__ == "__main__", so importing it runs `raise SystemExit(main())`.
# A SystemExit escaping import aborts collection for the entire repository,
# not just this file. Exec the wrapper here and absorb that exit, then read
# the implementation's globals out of the namespace the wrapper built. This
# keeps the fix inside this test: scripts/check_stegos_ipod_bootstrap_projection.py
# is claimed by other active work and is not ours to change.


class _Module:
    def __init__(self, namespace):
        self.__dict__ = namespace


def _load_checker(relative):
    path = ROOT / "scripts" / relative
    outer = {"__name__": "__checker_wrapper__", "__file__": str(path)}
    try:
        exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), outer)
    except SystemExit:
        pass
    inner = outer.get("namespace")
    assert isinstance(inner, dict), f"{relative} did not expose its implementation namespace"
    return _Module(inner)


module = _load_checker("check_stegos_ipod_bootstrap_projection.py")


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
