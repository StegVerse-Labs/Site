#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS_MD = ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.md"
STATUS_JSON = ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.json"

REQUIRED_JSON_KEYS = {
    "schema",
    "repository",
    "generated_at",
    "goal_status",
    "gates",
    "source_boundaries",
    "non_claims",
}

ALLOWED_GOAL_STATUS = {"ready", "pending_external_evidence"}

REQUIRED_MD_TERMS = {
    "# Site Final Goal Status",
    "goal_status:",
    "tt_bundle_fed_status_ready:",
    "governance_observatory_status_ready:",
    "local_completion_receipt_ready:",
    "StegVerse-Labs/Site",
    "Admissible-Existence/TT remains TT source of truth.",
    "StegVerse-Labs/governance-observatory remains source-intake source of truth.",
}

REQUIRED_GATES = {
    "tt_bundle_fed_status_ready",
    "governance_observatory_status_ready",
    "local_completion_receipt_ready",
}

FORBIDDEN_TERMS = {
    "Site is the TT source of truth",
    "Site is the Governance Observatory source of truth",
    "issues commit-time permission",
    "proves transition admissibility",
}


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def read(path: Path) -> str:
    if not path.exists():
        fail(f"missing file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def main() -> int:
    md = read(STATUS_MD)
    raw = read(STATUS_JSON)
    data = json.loads(raw)

    missing_keys = sorted(REQUIRED_JSON_KEYS - set(data))
    if missing_keys:
        fail("missing JSON keys: " + ", ".join(missing_keys))

    if data.get("schema") != "site_final_goal_status.v0.1":
        fail("schema mismatch")
    if data.get("repository") != "StegVerse-Labs/Site":
        fail("repository mismatch")
    if data.get("goal_status") not in ALLOWED_GOAL_STATUS:
        fail("invalid goal_status")

    gates = data.get("gates", {})
    for gate in REQUIRED_GATES:
        if gate not in gates or not isinstance(gates[gate], bool):
            fail(f"invalid gate: {gate}")

    if data.get("goal_status") == "ready" and not all(gates.values()):
        fail("goal_status ready requires all gates true")
    if data.get("goal_status") == "pending_external_evidence" and all(gates.values()):
        fail("all gates true should not remain pending_external_evidence")

    if not data.get("non_claims"):
        fail("missing non_claims")

    for term in REQUIRED_MD_TERMS:
        if term not in md:
            fail(f"status markdown missing: {term}")

    combined = md + "\n" + raw
    for term in FORBIDDEN_TERMS:
        if term in combined:
            fail(f"forbidden term present: {term}")

    print("OK: Site final goal status validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
