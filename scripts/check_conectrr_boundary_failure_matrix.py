#!/usr/bin/env python3
"""Exercise every declared Conectrr overreach and under-specification failure class."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BASE_FIXTURE = ROOT / "data" / "conectrr-minimum-handoff.fixture.json"
MATRIX_FIXTURE = ROOT / "data" / "conectrr-boundary-failure-matrix.fixture.json"
VALIDATOR = ROOT / "scripts" / "check_conectrr_minimum_handoff.py"


def load_failure():
    spec = importlib.util.spec_from_file_location("conectrr_minimum_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load minimum-handoff validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.failure


def set_path(record: dict[str, Any], dotted_path: str, value: Any) -> None:
    parts = dotted_path.split(".")
    target: Any = record
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value


def main() -> int:
    base_payload = json.loads(BASE_FIXTURE.read_text(encoding="utf-8"))
    matrix = json.loads(MATRIX_FIXTURE.read_text(encoding="utf-8"))
    valid_case = next(case for case in base_payload["cases"] if case["case_id"] == "valid-minimum")
    failure = load_failure()
    errors: list[str] = []

    if failure(copy.deepcopy(valid_case["record"])) is not None:
        errors.append("base valid record no longer passes minimum-handoff validation")

    seen_failures: set[str] = set()
    for case in matrix.get("cases", []):
        record = copy.deepcopy(valid_case["record"])
        for path, value in case.get("mutation", {}).items():
            set_path(record, path, value)
        observed = failure(record)
        expected = case.get("expected_failure")
        if observed != expected:
            errors.append(f"{case.get('case_id')}: expected {expected}, observed {observed}")
        if observed:
            seen_failures.add(observed)

    required = {
        "OVERREACH_CONSENT", "OVERREACH_AUTHORITY", "OVERREACH_ADMISSIBILITY",
        "OVERREACH_COMMITMENT", "OVERREACH_EXECUTION", "UNDER_SPECIFIED_INTENT",
        "UNDER_SPECIFIED_REASONING", "UNDER_SPECIFIED_UNCERTAINTY",
        "UNRESOLVED_DEPENDENCY_HIDDEN", "UNSTABLE_HANDOFF_ID",
    }
    missing = required - seen_failures
    if missing:
        errors.append("missing exercised failure classes: " + ",".join(sorted(missing)))

    if errors:
        print("CONECTRR_BOUNDARY_FAILURE_MATRIX_CHECK=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("CONECTRR_BOUNDARY_FAILURE_MATRIX_CHECK=PASS")
    print(f"cases={len(matrix.get('cases', []))}")
    print("overreach_classes=consent,authority,admissibility,commitment,execution")
    print("under_specification_classes=intent,reasoning,uncertainty,hidden_dependency,unstable_id")
    print("authority_effect=none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
