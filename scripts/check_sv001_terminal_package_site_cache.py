#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "stegos-bootstrap" / "workercoordinator-portable-sv001.json"
SERVICE_WORKER = ROOT / "stegos-bootstrap" / "service-worker.js"
HANDOFF = ROOT / "docs" / "SV001_TERMINAL_PACKAGE_SITE_CACHE_MIRROR_HANDOFF.md"
LEGACY_VALIDATOR = ROOT / "scripts" / "check_stegos_ipod_bootstrap_projection.py"

CANONICAL_PACKAGE_BLOB = "1483eb45263e2f7745e8c3e76dc19492efd44cf1"
PREDECESSOR_SERVICE_WORKER_BLOB = "99d652dc961855b0b89d093a3f5ad2e027352849"
TERMINAL_SERVICE_WORKER_BLOB = "048ae96f211e28314fa91c6a34cbc29ec13a2a26"
CANONICAL_CYCLE = "sha256:81a078eeeacffb8fc86d287d7aaa8a9904c6f53973471dad7f6d7c3fa6818a35"
RESET_DUPLICATE = "sha256:7b66f6cf260a46fcb8555d207cd868eaf2d31aa67372f0701841f91c648d00d4"


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit("FAIL: " + message)


def main() -> int:
    pkg = json.loads(PACKAGE.read_text(encoding="utf-8"))
    sw = SERVICE_WORKER.read_text(encoding="utf-8")
    handoff = HANDOFF.read_text(encoding="utf-8")
    legacy = LEGACY_VALIDATOR.read_text(encoding="utf-8")

    require(git_blob(PACKAGE) == CANONICAL_PACKAGE_BLOB, "terminal package is not exact canonical blob")
    require(git_blob(SERVICE_WORKER) == TERMINAL_SERVICE_WORKER_BLOB, "service worker is not exact v10 successor blob")
    require('var CACHE_NAME = "stegos-web-bootstrap-v10";' in sw, "cache generation did not advance to v10")
    require('var CACHE_NAME = "stegos-web-bootstrap-v9";' not in sw, "stale v9 cache generation remains")
    require('"./master-records-sv001-custody.js"' in sw, "Master Records custody module was not preserved")
    require('MASTER_RECORDS_SV001_PATH = "/stegos-bootstrap/master-records/sv001"' in sw, "Master Records endpoint was not preserved")
    require('PORTABLE_WC_PACKAGE_URL = new URL("./workercoordinator-portable-sv001.json", self.location.href).toString();' in sw, "portable package cache binding drift")
    require('return caches.match(PORTABLE_WC_PACKAGE_URL)' in sw, "portable package no longer loads from cache")

    require(pkg["task"]["state"] == "COMPLETED", "SV001 package is not terminal")
    require(pkg["task"]["admission"]["claim_state"] == "TERMINAL_NO_FURTHER_CLAIM", "terminal claim state missing")
    require(pkg["task"]["admission"]["fresh_fence_required"] is False, "terminal package still requests fresh fence")
    require(pkg["execution_authorized"] is False, "terminal package still authorizes execution")
    require(pkg["terminal_reexecution_allowed"] is False, "terminal reexecution widened")
    require(pkg["downstream_retry_after_terminal"] is True, "downstream retry was accidentally disabled")
    require(pkg["credential_authority"] == "TV/TVC", "credential authority drift")
    require(pkg["github_token_runtime_authority"] == "NONE", "GitHub runtime authority widened")
    require(pkg["heartbeat_grants_execution_authority"] is False, "HB authority widened")
    require(pkg["external_non_stegverse_machine_required"] is False, "second-machine dependency introduced")

    terminal = pkg["terminal_execution"]
    require(terminal["canonical_cycle_receipt_sha256"] == CANONICAL_CYCLE, "canonical first G23 custody source drift")
    require(terminal["canonical_custody_eligible"] is True, "canonical first G23 lost custody eligibility")
    duplicates = terminal["duplicates_retained_non_custodial"]
    reset = next((row for row in duplicates if row.get("cycle_receipt_sha256") == RESET_DUPLICATE), None)
    require(reset is not None, "reset-lineage duplicate evidence not retained")
    require(reset["custody_eligible"] is False, "reset-lineage duplicate became custody eligible")

    require(TERMINAL_SERVICE_WORKER_BLOB in legacy, "legacy validator does not admit exact v10 successor")
    require(PREDECESSOR_SERVICE_WORKER_BLOB in legacy, "legacy validator lost historical v9 identity")
    require(CANONICAL_PACKAGE_BLOB in handoff and TERMINAL_SERVICE_WORKER_BLOB in handoff, "handoff exact source pins missing")
    require("Master Records custody" in handoff and "SV002" in handoff, "runtime completion boundary missing")

    print("SV001_TERMINAL_SITE_CACHE_PASS")
    print("terminal_package_blob=" + CANONICAL_PACKAGE_BLOB)
    print("service_worker_blob=" + TERMINAL_SERVICE_WORKER_BLOB)
    print("canonical_custody_source=" + CANONICAL_CYCLE)
    print("reset_duplicate_custody_eligible=false")
    print("credential_authority=TV/TVC")
    print("github_token_runtime_authority=NONE")
    print("second_machine_required=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
