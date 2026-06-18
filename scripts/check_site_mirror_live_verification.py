#!/usr/bin/env python3
"""Check Site paper mirror live-verification evidence.

This verifier is intentionally conservative. It does not activate the mirror.
It reports whether the checked-in Site manifest has the metadata expected after
Publisher-to-Site live mirror dispatch.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_MANIFEST_FIELDS = [
    "source_repository",
    "source_ref",
    "source_path",
    "source_of_truth",
    "target_repository",
    "target_path",
    "display_policy",
    "mirror_protocol",
    "workflow",
    "generated_utc",
    "count",
    "aliases",
    "entries",
]

LEGACY_FIELDS = ["source", "target"]

REQUIRED_ALIASES = [
    "Papers.html",
    "papers.html",
    "papers/index.html",
    "publisher/papers.html",
    "publisher/papers/index.html",
]

EXPECTED_SOURCE_REPOSITORY = "GCAT-BCAT-Engine/Publisher"
EXPECTED_SOURCE_PATH = "papers"
EXPECTED_TARGET_REPOSITORY = "StegVerse-Labs/Site"
EXPECTED_TARGET_PATH = "papers"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return data


def check_manifest(manifest: dict[str, Any]) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    missing = [field for field in REQUIRED_MANIFEST_FIELDS if field not in manifest]
    if missing:
        failures.append("missing required manifest fields: " + ", ".join(missing))

    present_legacy = [field for field in LEGACY_FIELDS if field in manifest]
    if present_legacy:
        warnings.append("legacy manifest fields still present: " + ", ".join(present_legacy))

    if manifest.get("source_repository") not in (None, EXPECTED_SOURCE_REPOSITORY):
        failures.append("source_repository does not match Publisher")
    if manifest.get("source_path") not in (None, EXPECTED_SOURCE_PATH):
        failures.append("source_path does not match papers")
    if manifest.get("target_repository") not in (None, EXPECTED_TARGET_REPOSITORY):
        failures.append("target_repository does not match Site")
    if manifest.get("target_path") not in (None, EXPECTED_TARGET_PATH):
        failures.append("target_path does not match papers")

    aliases = manifest.get("aliases")
    if isinstance(aliases, list):
        missing_aliases = [alias for alias in REQUIRED_ALIASES if alias not in aliases]
        if missing_aliases:
            failures.append("missing required aliases: " + ", ".join(missing_aliases))
    elif "aliases" in manifest:
        failures.append("aliases must be a list")

    entries = manifest.get("entries")
    count = manifest.get("count")
    if isinstance(entries, list) and isinstance(count, int):
        if count != len(entries):
            failures.append(f"count {count} does not equal entries length {len(entries)}")
    elif "entries" in manifest or "count" in manifest:
        failures.append("entries must be a list and count must be an integer")

    return failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default="papers/papers_manifest.json")
    parser.add_argument("--json", action="store_true", help="emit machine-readable result")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    result: dict[str, Any] = {
        "check": "site_mirror_live_verification",
        "manifest": str(manifest_path),
        "activation_state": "unknown",
        "failures": [],
        "warnings": [],
    }

    if not manifest_path.exists():
        result["activation_state"] = "blocked_missing_manifest"
        result["failures"].append(f"manifest not found: {manifest_path}")
    else:
        manifest = load_json(manifest_path)
        failures, warnings = check_manifest(manifest)
        result["failures"] = failures
        result["warnings"] = warnings
        result["activation_state"] = "ready_for_activation_receipt" if not failures else "ready_for_live_mirror_verification"

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"check: {result['check']}")
        print(f"manifest: {result['manifest']}")
        print(f"activation_state: {result['activation_state']}")
        if result["warnings"]:
            print("warnings:")
            for warning in result["warnings"]:
                print(f"- {warning}")
        if result["failures"]:
            print("failures:")
            for failure in result["failures"]:
                print(f"- {failure}")

    return 0 if not result["failures"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
