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
        "Activation state: pending_external_evidence",
        "github/workflows/site-autonomous-continuation.yml",
        "docs/SITE_FINAL_GOAL_STATUS.json",
    ],
    "final_goal": ["site_final_goal_status.v0.1", "pending_external_evidence"],
    "external": ["pending_external_evidence"],
}

FORBIDDEN = [
    "Activation state: activated",
    "ready_completion: ready",
    "Site is the TT source of truth",
    "Site is the Governance Observatory source of truth",
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
        missing = [term for term in REQUIRED[label] if term not in text]
        blocked = [term for term in FORBIDDEN if term in text]
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
