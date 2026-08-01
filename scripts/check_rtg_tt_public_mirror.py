#!/usr/bin/env python3
"""Validate the bounded RTG-TT public mirror package.

This validator checks package identity, canonical source bindings, ownership
separation, result mapping, authority flags, path isolation, and activation
posture. It does not establish mathematical completeness, execution authority,
publication authority, custody, or downstream ingestion.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "data" / "rtg-tt" / "rtg-tt-public-mirror.v0.1.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")

EXPECTED_COMMITS = {
    "rtg_tests": "2fd7099bb3b6d2d7aa8ce7d72f7f71f6dfd4566a",
    "transition_table": "19720bae935ef9881ce5b239e0b66423fcd8bfab",
    "validation_factory": "5ca6ac0442809c5902f9765d2f865e5fa03d9c60",
}

EXPECTED_MAPPING = {
    "RESOLUTION_SATISFIED": "ALLOW",
    "FAIL_CLOSED": "DENY",
    "QUARANTINE": "DEFER",
}

FORBIDDEN_CLAIM_PREFIXES = (
    "humans-as-interoperability-layer.html",
    "assets/hil-",
    "scripts/check_hil_",
)


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def load() -> dict[str, Any]:
    if not PACKAGE.exists():
        fail(f"package missing: {PACKAGE.relative_to(ROOT)}")
    try:
        payload = json.loads(PACKAGE.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON: {exc}")
    if not isinstance(payload, dict):
        fail("package root must be an object")
    return payload


def main() -> int:
    payload = load()

    if payload.get("package_id") != "rtg-tt-public-mirror-v0.1":
        fail("unexpected package_id")
    if payload.get("contract_version") != "rtg-tt-v0.1":
        fail("unexpected contract_version")
    if payload.get("site_issue") != 122:
        fail("site_issue must bind Site issue 122")

    sources = payload.get("canonical_sources")
    if not isinstance(sources, dict):
        fail("canonical_sources must be an object")

    for key, expected_commit in EXPECTED_COMMITS.items():
        source = sources.get(key)
        if not isinstance(source, dict):
            fail(f"missing canonical source: {key}")
        commit = source.get("commit")
        if commit != expected_commit or not SHA40.fullmatch(str(commit)):
            fail(f"{key} commit binding mismatch")

    factory = sources["validation_factory"]
    report_hash = factory.get("report_hash")
    if not isinstance(report_hash, str) or not SHA256.fullmatch(report_hash):
        fail("validation_factory report_hash must be canonical sha256")

    ae_index = sources.get("ae_public_index")
    if not isinstance(ae_index, dict):
        fail("missing ae_public_index binding")
    if ae_index.get("pull_request") != 5:
        fail("AE public index must bind PR 5")
    if not SHA40.fullmatch(str(ae_index.get("head_commit", ""))):
        fail("AE public index head_commit is invalid")

    if payload.get("mapping") != EXPECTED_MAPPING:
        fail("RTG-TT result mapping mismatch")

    ownership = payload.get("ownership")
    if not isinstance(ownership, dict):
        fail("ownership must be an object")
    required_owners = {"rtg_ae", "tt", "validation_factory", "site"}
    if set(ownership) != required_owners:
        fail("ownership boundary is incomplete or expanded")

    authority = payload.get("authority")
    if not isinstance(authority, dict) or not authority:
        fail("authority boundary missing")
    elevated = sorted(key for key, value in authority.items() if value is not False)
    if elevated:
        fail(f"authority flags must remain false: {elevated}")

    gates = payload.get("activation_gates")
    if not isinstance(gates, dict):
        fail("activation_gates must be an object")
    if gates.get("site_orchestrator_admitted") is not False:
        fail("candidate package may not self-declare orchestrator admission")
    if gates.get("site_package_merged") is not False:
        fail("unmerged candidate may not self-declare Site activation")

    claims = payload.get("claimed_paths")
    if not isinstance(claims, list) or not claims:
        fail("claimed_paths must be a non-empty list")
    for claim in claims:
        if not isinstance(claim, str):
            fail("claimed_paths entries must be strings")
        if any(claim.startswith(prefix) for prefix in FORBIDDEN_CLAIM_PREFIXES):
            fail(f"path collision with active HIL owner: {claim}")

    targets = payload.get("downstream_targets")
    expected_targets = {
        "StegVerse-Labs/admissibility-wiki",
        "StegVerse-002/stegguardian-wiki",
        "GCAT-BCAT-Engine/Publisher",
    }
    if set(targets or []) != expected_targets:
        fail("downstream target set mismatch")

    non_claims = payload.get("non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 5:
        fail("non_claim boundary is incomplete")

    result = {
        "status": "PASS",
        "package_id": payload["package_id"],
        "contract_version": payload["contract_version"],
        "site_issue": payload["site_issue"],
        "canonical_commits": EXPECTED_COMMITS,
        "authority_effect": False,
        "activation_effect": False,
        "orchestrator_admission_required": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
