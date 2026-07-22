#!/usr/bin/env python3
"""Fail-closed validator for reciprocal framework evaluation projections."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "data/framework-evaluations/index.json"
SCHEMA = ROOT / "data/schemas/framework-evaluation.schema.json"
PAGE = ROOT / "framework-evaluations.html"
REQUIRED_FRAMEWORKS = {"stegverse", "ta-14"}
RESULT_CLASSES = {"PASS", "PARTIAL", "FAIL", "ERROR", "REFUSE", "NOT_TESTED", "INCONCLUSIVE", "DISPUTED"}
OBSERVATION_CLASSES = {"DECLARED", "OBSERVED", "DERIVED", "RECONSTRUCTED", "DISPUTED"}


def load(path: Path) -> dict:
    if not path.is_file():
        raise AssertionError(f"missing required file: {path.relative_to(ROOT)}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AssertionError(f"invalid JSON in {path.relative_to(ROOT)}: {exc}") from exc


def require(value: object, message: str) -> None:
    if not value:
        raise AssertionError(message)


def validate_record(path: Path, expected_id: str) -> None:
    record = load(path)
    require(record.get("schema_version") == "1.0.0", f"{path.name}: unsupported schema_version")
    require(record.get("evaluation_id"), f"{path.name}: missing evaluation_id")

    framework = record.get("framework") or {}
    require(framework.get("framework_id") == expected_id, f"{path.name}: framework_id mismatch")
    require(framework.get("name"), f"{path.name}: missing framework name")
    require(str(framework.get("canonical_url", "")).startswith("https://"), f"{path.name}: canonical_url must use HTTPS")

    declaration = record.get("self_declaration") or {}
    require(declaration.get("source") == "SELF", f"{path.name}: self declaration source must be SELF")
    for field in ("claim_id", "scope", "functions", "limitations", "evidence_refs"):
        require(declaration.get(field), f"{path.name}: self_declaration missing {field}")
    confidence = declaration.get("confidence")
    require(isinstance(confidence, (int, float)) and 0 <= confidence <= 1, f"{path.name}: invalid declaration confidence")

    for determination in record.get("determinations", []):
        require(determination.get("source") == "EVALUATOR", f"{path.name}: determination source must be EVALUATOR")
        require(determination.get("observation_class") in OBSERVATION_CLASSES, f"{path.name}: invalid observation class")
        require(determination.get("determination_id"), f"{path.name}: missing determination_id")
        require(determination.get("evaluator_id"), f"{path.name}: missing evaluator_id")

    for run in record.get("test_runs", []):
        require(run.get("result") in RESULT_CLASSES, f"{path.name}: invalid test result")
        for field in ("run_id", "test_case_id", "executor_id", "started_at", "event_refs", "evidence_refs"):
            require(field in run, f"{path.name}: test run missing {field}")

    publication = record.get("publication") or {}
    require(publication.get("projection_authority") == "NONE", f"{path.name}: projection must grant no authority")
    require(publication.get("record_hash"), f"{path.name}: missing record_hash status")
    require(publication.get("reconstruction_status") in {"PASS", "PARTIAL", "FAIL", "NOT_TESTED"}, f"{path.name}: invalid reconstruction status")


def main() -> int:
    index = load(INDEX)
    load(SCHEMA)
    require(PAGE.is_file(), "missing framework-evaluations.html")
    html = PAGE.read_text(encoding="utf-8")
    for marker in ("Neutral public test", "Reciprocal architectural evaluation", "data/framework-evaluations/index.json"):
        require(marker in html, f"framework-evaluations.html missing marker: {marker}")

    entries = index.get("frameworks") or []
    ids = {entry.get("framework_id") for entry in entries}
    require(REQUIRED_FRAMEWORKS <= ids, "registry must contain StegVerse and TA-14")
    require(index.get("authority") == {"comparison": False, "admissibility": False, "certification": False, "execution": False, "custody": False}, "registry authority boundary changed")

    seen_paths: set[str] = set()
    for entry in entries:
        framework_id = entry.get("framework_id")
        evaluation_path = entry.get("evaluation_path")
        require(framework_id and evaluation_path, "registry entry missing framework_id or evaluation_path")
        require(evaluation_path not in seen_paths, f"duplicate evaluation_path: {evaluation_path}")
        seen_paths.add(evaluation_path)
        validate_record(ROOT / "data/framework-evaluations" / evaluation_path, framework_id)

    print("RECIPROCAL FRAMEWORK EVALUATIONS: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
