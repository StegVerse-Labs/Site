#!/usr/bin/env python3
"""Derive the HIL announcement posture from repository-owned machine evidence."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

DEFAULT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = Path("data/hil-announcement-status.json")

MANAGED_COMPONENTS = (
    "hil-study-announcement.html",
    "hil-study-launch.html",
    "hil-managed-return.html",
    "scripts/ingest_hil_pilot_return.py",
    "scripts/validate_hil_pilot_ledger.py",
    "data/schemas/hil-managed-receiving-acknowledgment.schema.json",
)

MANAGED_AVAILABLE_NOW = (
    "canonical paper download",
    "exact prompt",
    "local PDF signature validation",
    "SHA-256 response binding",
    "participant metadata capture",
    "publication-consent capture",
    "downloadable return package",
    "downloadable local preparation receipt",
)

MANAGED_PENDING = (
    "persistent governed HTTPS receiver",
    "automatic durable custody",
    "automatic registry commit",
    "automatic reconstruction",
    "automatic publication disposition",
)

MANAGED_WITHHELD = (
    "SERVER_SUBMISSION_COMPLETE",
    "DURABLE_CUSTODY_COMPLETE",
    "REGISTRY_COMMIT_COMPLETE",
    "PUBLICATION_COMPLETE",
)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def source_record(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    return {"path": relative, "present": path.is_file()}


def read_optional_json(root: Path, relative: str) -> dict[str, Any] | None:
    path = root / relative
    if not path.exists():
        return None
    return load_json(path)


def derive_status(root: Path = DEFAULT_ROOT) -> dict[str, Any]:
    ledger = load_json(root / "data/hil-pilot-ledger.json")
    linkedin = load_json(root / "data/hil-linkedin-launch-readiness.json")
    participant = load_json(root / "data/hil-participant-readiness.json")
    deployment = load_json(root / "data/hil-receiver-deployment-latest.json")
    controlled = load_json(root / "data/hil-controlled-cycle-latest.json")
    restart = read_optional_json(root, "data/hil-restart-persistence-latest.json")

    canonical_primary = linkedin["canonical_primary"]
    canonical_prompt = linkedin["canonical_prompt"]
    primary_relative = canonical_primary["path"]
    primary_path = root / primary_relative
    primary_payload = primary_path.read_bytes() if primary_path.exists() else b""
    actual_primary_hash = sha256_bytes(primary_payload) if primary_payload else None

    paper_signature_valid = primary_payload.startswith(b"%PDF-")
    paper_size_valid = len(primary_payload) == canonical_primary["size_bytes"]
    paper_hash_valid = actual_primary_hash == canonical_primary["sha256"]
    ledger_identity_valid = (
        ledger.get("canonical_primary", {}).get("version") == linkedin.get("experiment_version")
        and ledger.get("canonical_primary", {}).get("sha256") == canonical_primary["sha256"]
        and ledger.get("canonical_prompt", {}).get("version") == canonical_prompt["version"]
        and ledger.get("canonical_prompt", {}).get("sha256") == canonical_prompt["sha256"]
    )
    ledger_boundary_valid = (
        ledger.get("authority_effect") is False
        and ledger.get("custody_effect") is False
        and ledger.get("publication_effect") is False
    )
    managed_components = {relative: (root / relative).is_file() for relative in MANAGED_COMPONENTS}
    managed_return_ready = all(
        (
            paper_signature_valid,
            paper_size_valid,
            paper_hash_valid,
            ledger_identity_valid,
            ledger_boundary_valid,
            all(managed_components.values()),
        )
    )

    deployment_ready = deployment.get("deployed") is True and deployment.get("ready") is True
    controlled_cycle_passed = (
        controlled.get("passed") is True
        and controlled.get("conclusion") in {"success", "passed", "PASS"}
    )
    participant_ready = (
        participant.get("state") == "TEST_PARTICIPANT_PACKET_PASSED"
        and participant.get("participant_ready") is True
        and participant.get("upload_button_authorized") is True
    )
    restart_persistence_passed = bool(
        restart
        and restart.get("passed") is True
        and restart.get("conclusion") in {"success", "passed", "PASS"}
    )
    production_receiver_ready = all(
        (
            managed_return_ready,
            deployment_ready,
            controlled_cycle_passed,
            participant_ready,
            restart_persistence_passed,
        )
    )

    claims_withheld = list(MANAGED_WITHHELD)
    pending_capabilities = list(MANAGED_PENDING)
    participant_warning_required = True
    temporary_return_mode = {
        "mode": "PARTICIPANT_MANAGED_DIRECT_RETURN",
        "instructions": (
            "Preserve the response PDF unchanged and return it together with the generated package JSON "
            "through the direct channel identified in the experiment announcement."
        ),
        "server_custody_established": False,
        "registry_commit_established": False,
        "publication_established": False,
    }

    if production_receiver_ready:
        announcement_state = "ANNOUNCEMENT_READY_WITH_PRODUCTION_RECEIVER"
        participant_intake_state = "OPEN_GOVERNED_RECEIVER"
        participant_warning_required = False
        temporary_return_mode["mode"] = "PARTICIPANT_MANAGED_DIRECT_RETURN_FALLBACK"
        temporary_return_mode["server_custody_established"] = True
        temporary_return_mode["registry_commit_established"] = True
        claims_withheld = ["PUBLICATION_COMPLETE"]
        pending_capabilities = ["automatic publication disposition"]
    elif managed_return_ready:
        announcement_state = "ANNOUNCEMENT_READY_WITH_MANAGED_RETURN"
        participant_intake_state = "OPEN_MANAGED_RETURN"
    else:
        announcement_state = "ANNOUNCEMENT_NOT_READY"
        participant_intake_state = "CLOSED"

    announcement_permitted = managed_return_ready or production_receiver_ready

    evidence_paths = [
        "data/hil-pilot-ledger.json",
        "data/hil-linkedin-launch-readiness.json",
        "data/hil-participant-readiness.json",
        "data/hil-receiver-deployment-latest.json",
        "data/hil-controlled-cycle-latest.json",
        primary_relative,
        *MANAGED_COMPONENTS,
    ]
    if restart is not None:
        evidence_paths.append("data/hil-restart-persistence-latest.json")

    return {
        "schema_version": "HIL-ANNOUNCEMENT-STATUS-v2",
        "study": "Humans as the Interoperability Layer",
        "announcement_state": announcement_state,
        "participant_intake_state": participant_intake_state,
        "canonical_primary": {
            "version": linkedin["experiment_version"],
            "path": primary_relative,
            "filename": canonical_primary["filename"],
            "size_bytes": canonical_primary["size_bytes"],
            "sha256": canonical_primary["sha256"],
            "observed_sha256": actual_primary_hash,
        },
        "canonical_prompt": {
            "version": canonical_prompt["version"],
            "sha256": canonical_prompt["sha256"],
        },
        "available_now": list(MANAGED_AVAILABLE_NOW) if announcement_permitted else [],
        "temporary_return_mode": temporary_return_mode,
        "production_receiver": {
            "ready": production_receiver_ready,
            "deployment_ready": deployment_ready,
            "controlled_cycle_passed": controlled_cycle_passed,
            "participant_readiness_passed": participant_ready,
            "restart_persistence_passed": restart_persistence_passed,
        },
        "pending_capabilities": pending_capabilities,
        "claims_withheld": claims_withheld,
        "announcement_permitted": announcement_permitted,
        "participant_warning_required": participant_warning_required,
        "derivation": {
            "mode": "MACHINE_DERIVED_FAIL_CLOSED",
            "managed_return_ready": managed_return_ready,
            "checks": {
                "canonical_pdf_signature_valid": paper_signature_valid,
                "canonical_pdf_size_valid": paper_size_valid,
                "canonical_pdf_sha256_valid": paper_hash_valid,
                "canonical_ledger_identity_valid": ledger_identity_valid,
                "pilot_ledger_authority_boundary_valid": ledger_boundary_valid,
                "managed_return_components_present": all(managed_components.values()),
            },
            "managed_components": managed_components,
            "sources": [source_record(root, path) for path in sorted(set(evidence_paths))],
        },
        "authority_effect": False,
    }


def canonical_json(value: dict[str, Any]) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="fail unless output matches derived state")
    args = parser.parse_args()

    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    derived = derive_status(root)
    rendered = canonical_json(derived)

    if args.check:
        if not output.exists():
            raise SystemExit(f"missing derived announcement status: {output}")
        current = output.read_text(encoding="utf-8")
        if current != rendered:
            raise SystemExit(
                "HIL announcement status is stale; run scripts/derive_hil_announcement_status.py"
            )
        if derived["announcement_permitted"] is not True:
            raise SystemExit("HIL announcement is not permitted by current machine evidence")
        print(f"PASS: {derived['announcement_state']} is current and machine-derived")
        return 0

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"WROTE: {output}")
    print(f"STATE: {derived['announcement_state']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
