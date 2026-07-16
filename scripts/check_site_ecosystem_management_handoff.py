#!/usr/bin/env python3
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
ECOSYSTEM = ROOT / "docs" / "SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md"
MIRROR_ECOSYSTEM = ROOT / "docs" / "SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md"
MIRROR = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
FINAL_GOAL = ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.json"
EXTERNAL = ROOT / "docs" / "SITE_EXTERNAL_EVIDENCE_STATE.json"

REQUIRED = {
    "ecosystem": [
        "SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED",
        "Contract status: PREPARED_NOT_DEPLOYED",
        "Management state: ecosystem-managed continuation ready after this packet and checker pass",
        ".github/workflows/validate.yml",
        ".github/workflows/site-task-runner.yml",
        "repository-local goal gates: ready",
        "live governed activation: blocked pending external evidence",
        "No release tag is authorized",
        "prior chat thread",
    ],
    "mirror_ecosystem": [
        "management_state: self_managed_handoff_ready",
        "site_state: autonomous_continuation_ready",
        "local_goal_status: ready",
        "activation_checkpoint: SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED",
        "contract_status: PREPARED_NOT_DEPLOYED",
        "live_transport_enabled: false",
        "final goal status reports ready",
        "thread_archive_ready: true",
        ".github/workflows/validate.yml",
        ".github/workflows/site-task-runner.yml",
    ],
    "mirror": [
        ".github/workflows/validate.yml",
        ".github/workflows/site-task-runner.yml",
        "SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED",
        "PREPARED_NOT_DEPLOYED",
        "No release tag is authorized",
        "live_transport_enabled: false",
        "Master-Records custody",
        "reconstructability PASS",
    ],
    "final_goal": ["site_final_goal_status.v0.1"],
    "external": ['"state": "external_evidence_present"', '"local_build_state": "repository_managed"'],
}

FORBIDDEN = [
    "Activation state: activated",
    "ready_completion: ready",
    "site_state: activated",
    "contract_status: DEPLOYED",
    "live_transport_enabled: true",
    "custody_recorded: true",
    "authority_granted: true",
    "release tag authorized",
]

FILES = {
    "ecosystem": ECOSYSTEM,
    "mirror_ecosystem": MIRROR_ECOSYSTEM,
    "mirror": MIRROR,
    "final_goal": FINAL_GOAL,
    "external": EXTERNAL,
}

ALLOWED_FINAL_GOAL_STATES = {"ready", "pending_external_evidence"}


def main() -> int:
    for label, path in FILES.items():
        if not path.exists():
            print(f"missing {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
        text = path.read_text(encoding="utf-8")
        folded = text.casefold()
        missing = [term for term in REQUIRED[label] if term.casefold() not in folded]
        blocked = [term for term in FORBIDDEN if term.casefold() in folded]
        if missing or blocked:
            print(f"{label} ecosystem handoff check failed", file=sys.stderr)
            for term in missing:
                print(f"missing: {term}", file=sys.stderr)
            for term in blocked:
                print(f"forbidden: {term}", file=sys.stderr)
            return 1

    final_goal = json.loads(FINAL_GOAL.read_text(encoding="utf-8"))
    final_state = final_goal.get("goal_status")
    if final_state not in ALLOWED_FINAL_GOAL_STATES:
        print(f"final_goal ecosystem handoff check failed: invalid goal_status {final_state!r}", file=sys.stderr)
        return 1
    gates = final_goal.get("gates")
    if not isinstance(gates, dict) or not gates:
        print("final_goal ecosystem handoff check failed: gates object required", file=sys.stderr)
        return 1
    if final_state == "ready" and not all(value is True for value in gates.values()):
        print("final_goal ecosystem handoff check failed: ready requires all gates true", file=sys.stderr)
        return 1
    if final_state == "pending_external_evidence" and all(value is True for value in gates.values()):
        print("final_goal ecosystem handoff check failed: pending state requires an unresolved gate", file=sys.stderr)
        return 1

    print(f"OK: Site ecosystem management handoff validated ({final_state})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
