#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
ECOSYSTEM = ROOT / "docs" / "SITE_ECOSYSTEM_MANAGEMENT_HANDOFF.md"
MIRROR_ECOSYSTEM = ROOT / "docs" / "SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md"
MIRROR = ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
FINAL_GOAL = ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.json"
EXTERNAL = ROOT / "docs" / "SITE_EXTERNAL_EVIDENCE_STATE.json"

REQUIRED = {
    "ecosystem": [
        "Activation state: pending_external_evidence",
        "Management state: ecosystem-managed continuation ready after this packet and checker pass",
        "docs/SITE_MIRROR_ECOSYSTEM_MANAGEMENT_HANDOFF.md",
        "docs/SITE_FINAL_GOAL_STATUS.json remains pending until TT bundle-fed status is PASS",
        "Site-local display pages alone do not make the final goal ready",
        "prior chat thread",
    ],
    "mirror_ecosystem": [
        "management_state: self_managed_handoff_ready",
        "site_state: autonomous_continuation_ready",
        "final goal status reports ready",
        "thread_archive_ready: true",
    ],
    "mirror": [
        ".github/workflows/validate.yml",
        ".github/workflows/site-task-runner.yml",
        "SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED",
        "PREPARED_NOT_DEPLOYED",
        "No release tag is authorized",
    ],
    # SITE_FINAL_GOAL_STATUS.json records Site-local completion gates. Once all
    # three local gates pass, its valid state is ready. External activation
    # evidence remains governed independently by SITE_EXTERNAL_EVIDENCE_STATE.json.
    "final_goal": ["site_final_goal_status.v0.1", '"goal_status": "ready"'],
    "external": ["pending_external_evidence"],
}

# These are concrete positive state declarations. Source-of-truth phrases are not
# checked as raw substrings because the canonical mirror handoff intentionally
# includes them inside an explicit non-claims section.
FORBIDDEN = [
    "Activation state: activated",
    "ready_completion: ready",
    "site_state: activated",
    "contract_status: DEPLOYED",
    "live_transport_enabled: true",
]

FILES = {
    "ecosystem": ECOSYSTEM,
    "mirror_ecosystem": MIRROR_ECOSYSTEM,
    "mirror": MIRROR,
    "final_goal": FINAL_GOAL,
    "external": EXTERNAL,
}


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
    print("OK: Site ecosystem management handoff validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
