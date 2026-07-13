#!/usr/bin/env python3
"""Verify a downloaded Site validation result/receipt/manifest bundle.

This verifier is read-only. It proves artifact integrity and identity consistency;
it does not prove deployment, endpoint liveness, custody, admissibility, release,
or RECORDED standing.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

RESULT = "site_application_validation.result.json"
RECEIPT = "site_current_main_validation.receipt.json"
MANIFEST = "site_current_main_validation.manifest.json"
HEX = set("0123456789abcdef")


def fail(message: str) -> None:
    raise SystemExit(f"SITE_VALIDATION_BUNDLE_FAIL: {message}")


def load(path: Path) -> dict:
    if not path.is_file():
        fail(f"missing {path.name}")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON in {path.name}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.name} must contain a JSON object")
    return value


def digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def valid_sha(value: object) -> bool:
    return isinstance(value, str) and len(value) == 40 and all(ch in HEX for ch in value.lower())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle_dir", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.bundle_dir).resolve()

    result_path = root / RESULT
    receipt_path = root / RECEIPT
    manifest_path = root / MANIFEST
    result = load(result_path)
    receipt = load(receipt_path)
    manifest = load(manifest_path)

    if result.get("passed") is not True or result.get("output") != "ECOSYSTEM_CHAT_APPLICATION_PASS":
        fail("canonical result is not passing")
    if receipt.get("schema") != "stegverse.site.current_main_validation_receipt.v1":
        fail("receipt schema mismatch")
    if receipt.get("state") != "VERIFIED" or receipt.get("conclusion") != "success":
        fail("receipt is not verified success")
    if manifest.get("schema") != "stegverse.site.current_main_validation_artifact_manifest.v1":
        fail("manifest schema mismatch")
    if manifest.get("state") != "COMPLETE":
        fail("manifest is not complete")

    file_entries = manifest.get("files")
    if not isinstance(file_entries, list) or len(file_entries) != 2:
        fail("manifest must bind exactly result and receipt")
    expected_paths = {RESULT: result_path, RECEIPT: receipt_path}
    seen: set[str] = set()
    for entry in file_entries:
        if not isinstance(entry, dict):
            fail("manifest file entry must be an object")
        rel = entry.get("path")
        if rel not in expected_paths or rel in seen:
            fail("manifest file set mismatch")
        seen.add(rel)
        if entry.get("media_type") != "application/json":
            fail(f"unexpected media type for {rel}")
        if entry.get("sha256") != digest(expected_paths[rel]):
            fail(f"hash mismatch for {rel}")
    if seen != set(expected_paths):
        fail("manifest omitted required file")

    if receipt.get("result_artifact") != RESULT:
        fail("receipt result path mismatch")
    if receipt.get("result_sha256") != digest(result_path):
        fail("receipt result hash mismatch")
    if receipt.get("repository") != "StegVerse-Labs/Site":
        fail("repository identity mismatch")
    if not valid_sha(receipt.get("commit_sha")):
        fail("invalid receipt commit SHA")
    for field in ("repository", "commit_sha", "workflow", "job", "run_id", "run_attempt", "validated_at"):
        if manifest.get(field) != receipt.get(field):
            fail(f"manifest/receipt identity mismatch: {field}")
    if not isinstance(receipt.get("run_id"), int) or receipt["run_id"] < 1:
        fail("invalid run id")
    if not isinstance(receipt.get("run_attempt"), int) or receipt["run_attempt"] < 1:
        fail("invalid run attempt")

    receipt_boundaries = receipt.get("authority_boundaries", {})
    manifest_boundaries = manifest.get("authority_boundaries", {})
    if any(value is not False for value in receipt_boundaries.values()):
        fail("receipt exceeded authority boundary")
    if any(value is not False for value in manifest_boundaries.values()):
        fail("manifest exceeded authority boundary")

    print("SITE_VALIDATION_ARTIFACT_BUNDLE_VERIFIED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
