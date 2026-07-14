#!/usr/bin/env python3
"""Fail closed when the activation-ledger continuation handoff drifts."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF = ROOT / "docs" / "SITE_ACTIVATION_LEDGER_MIRROR_HANDOFF.md"

REQUIRED_SNIPPETS = (
    "ACTIVATION_LEDGER_AND_ADVERSARIAL_GUARDS_INSTALLED_VALIDATION_OBSERVATION_PENDING",
    "docs/SITE_ACTIVATION_LEDGER.json",
    "scripts/check_site_activation_ledger.py",
    "scripts/test_site_activation_ledger.py",
    "scripts/check_site_workflow_inventory.py",
    "0227019aaaf2c9661238624216a5fa1f79bd9313",
    "1cd0a04dc1a7b08ee7ec227f2f21e59a5911f199",
    "8ccecf055fffa16175c5aa82321a5f2cd97c30f6",
    "checkpoint: SITE_PREPARATION_COMPLETE_ACTIVATION_BLOCKED",
    "contract_status: PREPARED_NOT_DEPLOYED",
    "activation_status: BLOCKED",
    "live_transport_enabled: false",
    "authority_granted: false",
    "custody_recorded: false",
    "release_authorized: false",
    "site_same_run_artifact_set: NOT_OBSERVED",
    "llm_adapter_current_main_validation: NOT_OBSERVED",
    "sdk_current_main_validation: NOT_OBSERVED",
    "same_origin_authenticated_deployment: NOT_OBSERVED",
    "live_endpoint_conformance: NOT_OBSERVED",
    "master_records_authenticated_custody: NOT_OBSERVED",
    "reconstructability: NOT_OBSERVED",
    "repository-local tests != current-main workflow evidence",
    "all gates verified != automatic activation",
    "Do not tag or release while activation remains BLOCKED.",
)

FORBIDDEN_SNIPPETS = (
    "activation_status: ACTIVE",
    "live_transport_enabled: true",
    "authority_granted: true",
    "custody_recorded: true",
    "release_authorized: true",
)


def main() -> int:
    if not HANDOFF.exists():
        print("SITE ACTIVATION LEDGER HANDOFF CHECK: FAIL")
        print(f"- missing {HANDOFF.relative_to(ROOT)}")
        return 1

    text = HANDOFF.read_text(encoding="utf-8")
    failures: list[str] = []

    for snippet in REQUIRED_SNIPPETS:
        if snippet not in text:
            failures.append(f"missing required handoff statement: {snippet}")

    for snippet in FORBIDDEN_SNIPPETS:
        if snippet in text:
            failures.append(f"forbidden activation claim present: {snippet}")

    print("SITE ACTIVATION LEDGER HANDOFF CHECK:", "FAIL" if failures else "PASS")
    for failure in failures:
        print(f"- {failure}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
