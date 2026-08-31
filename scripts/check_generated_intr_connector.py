#!/usr/bin/env python3
"""Verify the checked-in browser InTr source projection without network access."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "assets/generated/site-browser-intr-connectors.js"
MANIFEST = ROOT / "assets/generated/site-browser-intr-connectors.manifest.json"
EXPECTED_PROFILES = [
    "evaluator-read-review",
    "hil-submission",
    "sv002-public-observe",
    "device-kv",
]


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    artifact = ARTIFACT.read_bytes()
    digest = "sha256:" + hashlib.sha256(artifact).hexdigest()
    if manifest.get("artifact_sha256") != digest:
        raise SystemExit("SITE_GENERATED_INTR_ARTIFACT_HASH_MISMATCH")
    if manifest.get("schema") != "stegverse.universal-intr.generated-artifact-manifest/v1":
        raise SystemExit("SITE_GENERATED_INTR_MANIFEST_SCHEMA_INVALID")
    if manifest.get("source_repository") != "StegVerse-Labs/StegOS":
        raise SystemExit("SITE_GENERATED_INTR_SOURCE_INVALID")
    if manifest.get("profiles") != EXPECTED_PROFILES:
        raise SystemExit("SITE_GENERATED_INTR_PROFILE_SET_INVALID")
    if set(manifest.get("profile_sha256") or {}) != set(EXPECTED_PROFILES):
        raise SystemExit("SITE_GENERATED_INTR_PROFILE_BINDING_INCOMPLETE")
    if manifest.get("credential_authority") != "TV/TVC":
        raise SystemExit("SITE_GENERATED_INTR_CREDENTIAL_AUTHORITY_INVALID")
    for key in (
        "pypi_dependency",
        "cdn_dependency",
        "github_runtime_dependency",
        "third_party_package_authority",
    ):
        if manifest.get(key) is not False:
            raise SystemExit("SITE_GENERATED_INTR_FORBIDDEN_DEPENDENCY:" + key)
    source = artifact.decode("utf-8")
    required = (
        "StegVerseGeneratedInTr",
        "buildIntent",
        "buildReceipt",
        "validateComplete",
        "buildMaterializationRequest",
        manifest["registry_sha256"],
    )
    if any(marker not in source for marker in required):
        raise SystemExit("SITE_GENERATED_INTR_EMBEDDED_PROVENANCE_INVALID")
    print("SITE_GENERATED_INTR_CONNECTOR_PASS")
    print("SITE_GENERATED_INTR_ARTIFACT=" + digest)
    print("SITE_GENERATED_INTR_CREDENTIAL_AUTHORITY=TV_TVC")
    print("SITE_GENERATED_INTR_RUNTIME_DEPENDENCY=NONE")
    print("SITE_GENERATED_INTR_AUTHORITY_EFFECT=NONE_SOURCE_PROJECTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
