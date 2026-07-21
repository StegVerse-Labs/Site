#!/usr/bin/env python3
"""Fail-closed validation for the StegVerse company-testbed documentation set."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "handoff": ROOT / "docs" / "COMPANY_TESTBED_MIRROR_HANDOFF.md",
    "readme": ROOT / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_TESTBED_README.md",
    "audit_template": ROOT / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_AUDIT_TEMPLATE.md",
    "intake": ROOT / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_INTAKE_QUESTIONNAIRE.md",
    "sample": ROOT / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_SAMPLE_AUDIT.md",
    "target_template": ROOT / "docs" / "STEGVERSE_COMPANY_TESTBED_TARGET_LIST_TEMPLATE.md",
}

REQUIRED_TERMS = {
    "handoff": (
        "AI governance becomes a policy document while execution remains probabilistic.",
        "ALLOW only when both pass.",
        "FAIL_CLOSED when either cannot be proven sufficiently.",
        "docs/STEGVERSE_COMPANY_TESTBED_TARGET_LIST_TEMPLATE.md",
        "release tagging is not yet authorized",
    ),
    "readme": (
        "StegVerse Execution Boundary Audit",
        "non-production",
        "authority",
        "admissibility",
        "receipt",
    ),
    "audit_template": (
        "governed point of irreversibility",
        "ALLOW only when actor authority and state-transition admissibility both hold.",
        "FAIL_CLOSED",
        "mutation_committed",
        "reconstructability",
    ),
    "intake": (
        "One organization or lab.",
        "governed point of irreversibility",
        "confidentiality_preference",
        "No public claim or publication is permitted",
        "Minimum Acceptance Rule",
    ),
    "sample": (
        "non-production treasury-payment agent workflow",
        "authority_result: PASS",
        "state_freshness_result: FAIL",
        "admissibility_result: FAIL",
        "final_decision: FAIL_CLOSED",
        "execution_attempted: false",
        "mutation_committed: false",
        "cryptographic_verifiability: PARTIAL",
    ),
    "target_template": (
        "stegverse.company_testbed.target.v1",
        "execution_boundary_fit_hypothesis",
        "non_production_scope_plausibility",
        "authority_question",
        "state_transition_question",
        "permission_state",
        "next_permitted_action",
        "Prospective research candidate identified from public information.",
        "No record may transition directly from research to partner",
        "partners_claimed: 0",
    ),
}

FORBIDDEN_POSITIVE_CLAIMS = (
    "StegVerse has deployed with",
    "StegVerse is certified by",
    "StegVerse is endorsed by",
    "StegVerse customer:",
    "confirmed production integration",
    "authenticated Master-Records custody is complete",
    "release tagging is authorized",
)

CANONICAL_WORKFLOWS = {
    "ecosystem-chat-activation-retention.yml",
    "site-task-runner.yml",
    "validate.yml",
}


def fail(message: str) -> None:
    raise SystemExit(f"COMPANY TESTBED ARTIFACT VALIDATION FAILED: {message}")


def main() -> None:
    texts: dict[str, str] = {}
    for label, path in REQUIRED_FILES.items():
        if not path.is_file():
            fail(f"missing required file: {path.relative_to(ROOT)}")
        text = path.read_text(encoding="utf-8")
        if len(text.strip()) < 200:
            fail(f"file is unexpectedly incomplete: {path.relative_to(ROOT)}")
        texts[label] = text

    for label, terms in REQUIRED_TERMS.items():
        text = texts[label]
        for term in terms:
            if term not in text:
                fail(f"{label} missing required term: {term}")

    corpus = "\n".join(texts.values())
    for claim in FORBIDDEN_POSITIVE_CLAIMS:
        if claim in corpus:
            fail(f"forbidden unsupported positive claim present: {claim}")

    workflow_dir = ROOT / ".github" / "workflows"
    workflows = {path.name for path in workflow_dir.glob("*.yml")}
    missing_canonical = sorted(CANONICAL_WORKFLOWS - workflows)
    if missing_canonical:
        fail(f"missing canonical operational workflows: {missing_canonical}")

    inventory_check = (ROOT / "scripts" / "check_site_workflow_inventory.py").read_text(encoding="utf-8")
    binding = 'COMPANY_TESTBED_VALIDATOR = ROOT / "scripts" / "check_site_company_testbed_artifacts.py"'
    if binding not in inventory_check:
        fail("validator is not bound through scripts/check_site_workflow_inventory.py")

    retained = sorted(workflows - CANONICAL_WORKFLOWS)
    print("COMPANY TESTBED ARTIFACT VALIDATION PASSED")
    for label, path in REQUIRED_FILES.items():
        print(f"- {label}: {path.relative_to(ROOT)}")
    print("- canonical workflows present:", ", ".join(sorted(CANONICAL_WORKFLOWS)))
    print("- retained noncanonical workflows:", ", ".join(retained) or "none")
    print("- authority effect: NONE")
    print("- release authority: NOT GRANTED")


if __name__ == "__main__":
    main()
