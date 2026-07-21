#!/usr/bin/env python3
"""Adversarial regression tests for company-testbed artifact validation."""
from __future__ import annotations

import importlib.util
import io
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "scripts" / "check_site_company_testbed_artifacts.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("company_testbed_validator_under_test", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load company-testbed validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def padded(*terms: str) -> str:
    body = "\n".join(terms)
    return body + "\n" + ("bounded synthetic validation content\n" * 12)


def build_fixture(root: Path, validator) -> None:
    docs = root / "docs"
    scripts = root / "scripts"
    workflows = root / ".github" / "workflows"
    docs.mkdir(parents=True)
    scripts.mkdir(parents=True)
    workflows.mkdir(parents=True)

    for label, source_path in validator.REQUIRED_FILES.items():
        terms = validator.REQUIRED_TERMS[label]
        destination = docs / source_path.name
        destination.write_text(padded(*terms), encoding="utf-8")

    inventory_binding = (
        'COMPANY_TESTBED_VALIDATOR = ROOT / "scripts" / '
        '"check_site_company_testbed_artifacts.py"'
    )
    (scripts / "check_site_workflow_inventory.py").write_text(
        padded(inventory_binding), encoding="utf-8"
    )
    (workflows / "validate.yml").write_text("name: validate\n", encoding="utf-8")
    (workflows / "site-task-runner.yml").write_text("name: runner\n", encoding="utf-8")
    (workflows / "ecosystem-chat-activation-retention.yml").write_text(
        "name: retention\n", encoding="utf-8"
    )


def configure(validator, root: Path) -> None:
    validator.ROOT = root
    validator.REQUIRED_FILES = {
        "handoff": root / "docs" / "COMPANY_TESTBED_MIRROR_HANDOFF.md",
        "readme": root / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_TESTBED_README.md",
        "audit_template": root / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_AUDIT_TEMPLATE.md",
        "intake": root / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_INTAKE_QUESTIONNAIRE.md",
        "sample": root / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_SAMPLE_AUDIT.md",
        "target_template": root / "docs" / "STEGVERSE_COMPANY_TESTBED_TARGET_LIST_TEMPLATE.md",
    }


def expect_pass(validator) -> None:
    output = io.StringIO()
    with redirect_stdout(output):
        validator.main()
    text = output.getvalue()
    if "COMPANY TESTBED ARTIFACT VALIDATION PASSED" not in text:
        raise AssertionError("baseline fixture did not pass")


def expect_failure(validator, expected_fragment: str) -> None:
    try:
        with redirect_stdout(io.StringIO()):
            validator.main()
    except SystemExit as exc:
        if expected_fragment not in str(exc):
            raise AssertionError(
                f"expected failure containing {expected_fragment!r}, got {str(exc)!r}"
            ) from exc
        return
    raise AssertionError(f"expected validator failure containing {expected_fragment!r}")


def run_case(name: str, mutate, expected_fragment: str | None) -> None:
    validator = load_validator()
    with tempfile.TemporaryDirectory(prefix="site-company-testbed-") as tmp:
        root = Path(tmp)
        build_fixture(root, validator)
        configure(validator, root)
        mutate(root, validator)
        if expected_fragment is None:
            expect_pass(validator)
        else:
            expect_failure(validator, expected_fragment)
    print(f"PASS: {name}")


def no_mutation(root: Path, validator) -> None:
    del root, validator


def remove_required_term(root: Path, validator) -> None:
    path = root / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_SAMPLE_AUDIT.md"
    missing = "final_decision: FAIL_CLOSED"
    path.write_text(path.read_text(encoding="utf-8").replace(missing, ""), encoding="utf-8")


def add_forbidden_claim(root: Path, validator) -> None:
    del validator
    path = root / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_TESTBED_README.md"
    path.write_text(
        path.read_text(encoding="utf-8") + "\nStegVerse has deployed with Example Corp.\n",
        encoding="utf-8",
    )


def add_additional_workflow(root: Path, validator) -> None:
    del validator
    (root / ".github" / "workflows" / "extra.yml").write_text(
        "name: governed additional workflow\n", encoding="utf-8"
    )


def remove_canonical_workflow(root: Path, validator) -> None:
    del validator
    (root / ".github" / "workflows" / "validate.yml").unlink()


def remove_inventory_binding(root: Path, validator) -> None:
    del validator
    path = root / "scripts" / "check_site_workflow_inventory.py"
    path.write_text("bounded content\n" * 20, encoding="utf-8")


def truncate_artifact(root: Path, validator) -> None:
    del validator
    path = root / "docs" / "STEGVERSE_EXECUTION_BOUNDARY_INTAKE_QUESTIONNAIRE.md"
    path.write_text("incomplete\n", encoding="utf-8")


def main() -> int:
    cases = (
        ("baseline complete artifact set", no_mutation, None),
        (
            "missing required fail-closed result",
            remove_required_term,
            "sample missing required term: final_decision: FAIL_CLOSED",
        ),
        (
            "unsupported deployment claim",
            add_forbidden_claim,
            "forbidden unsupported positive claim present: StegVerse has deployed with",
        ),
        (
            "additional governed workflow permitted",
            add_additional_workflow,
            None,
        ),
        (
            "required canonical workflow removed",
            remove_canonical_workflow,
            "missing canonical operational workflows",
        ),
        (
            "validator binding removed",
            remove_inventory_binding,
            "validator is not bound through scripts/check_site_workflow_inventory.py",
        ),
        (
            "truncated intake artifact",
            truncate_artifact,
            "file is unexpectedly incomplete",
        ),
    )

    for name, mutate, expected in cases:
        run_case(name, mutate, expected)
    print("COMPANY TESTBED ARTIFACT ADVERSARIAL TESTS PASSED")
    print(f"- cases: {len(cases)}")
    print("- authority effect: NONE")
    print("- release authority: NOT GRANTED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
