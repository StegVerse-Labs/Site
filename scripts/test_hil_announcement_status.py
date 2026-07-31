#!/usr/bin/env python3
"""Deterministic tests for machine-derived HIL announcement status."""
from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path

from derive_hil_announcement_status import MANAGED_COMPONENTS, canonical_json, derive_status


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def fixture_root(base: Path) -> Path:
    root = base / "repo"
    paper = b"%PDF-1.4\nfixture\n%%EOF\n"
    paper_hash = hashlib.sha256(paper).hexdigest()
    (root / "data").mkdir(parents=True)
    (root / "data/HIL_Canonical_Paper_v1_1.pdf").write_bytes(paper)
    write_json(
        root / "data/hil-linkedin-launch-readiness.json",
        {
            "experiment_version": "v1.1",
            "canonical_primary": {
                "path": "data/HIL_Canonical_Paper_v1_1.pdf",
                "filename": "HIL_Canonical_Paper_v1_1.pdf",
                "size_bytes": len(paper),
                "sha256": paper_hash,
            },
            "canonical_prompt": {"version": "HIL-PROMPT-v1.1", "sha256": "a" * 64},
        },
    )
    write_json(
        root / "data/hil-pilot-ledger.json",
        {
            "canonical_primary": {"version": "v1.1", "sha256": paper_hash},
            "canonical_prompt": {"version": "HIL-PROMPT-v1.1", "sha256": "a" * 64},
            "authority_effect": False,
            "custody_effect": False,
            "publication_effect": False,
        },
    )
    write_json(
        root / "data/hil-participant-readiness.json",
        {
            "state": "NOT_YET_VERIFIED",
            "participant_ready": False,
            "upload_button_authorized": False,
        },
    )
    write_json(root / "data/hil-receiver-deployment-latest.json", {"deployed": False, "ready": False})
    write_json(
        root / "data/hil-controlled-cycle-latest.json",
        {"passed": False, "conclusion": "failure"},
    )
    for relative in MANAGED_COMPONENTS:
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("fixture\n", encoding="utf-8")
    return root


def main() -> int:
    cases = 0
    with tempfile.TemporaryDirectory(prefix="hil-announcement-") as directory:
        root = fixture_root(Path(directory))
        managed = derive_status(root)
        assert managed["announcement_state"] == "ANNOUNCEMENT_READY_WITH_MANAGED_RETURN"
        assert managed["participant_intake_state"] == "OPEN_MANAGED_RETURN"
        assert managed["announcement_permitted"] is True
        assert managed["production_receiver"]["ready"] is False
        cases += 1

        output = root / "data/hil-announcement-status.json"
        output.write_text(canonical_json(managed), encoding="utf-8")
        assert output.read_text(encoding="utf-8") == canonical_json(derive_status(root))
        cases += 1

        (root / "hil-managed-return.html").unlink()
        blocked = derive_status(root)
        assert blocked["announcement_state"] == "ANNOUNCEMENT_NOT_READY"
        assert blocked["announcement_permitted"] is False
        cases += 1
        (root / "hil-managed-return.html").write_text("fixture\n", encoding="utf-8")

        write_json(root / "data/hil-receiver-deployment-latest.json", {"deployed": True, "ready": True})
        write_json(
            root / "data/hil-controlled-cycle-latest.json",
            {"passed": True, "conclusion": "success"},
        )
        write_json(
            root / "data/hil-participant-readiness.json",
            {
                "state": "TEST_PARTICIPANT_PACKET_PASSED",
                "participant_ready": True,
                "upload_button_authorized": True,
            },
        )
        write_json(
            root / "data/hil-restart-persistence-latest.json",
            {"passed": True, "conclusion": "success"},
        )
        production = derive_status(root)
        assert production["announcement_state"] == "ANNOUNCEMENT_READY_WITH_PRODUCTION_RECEIVER"
        assert production["participant_intake_state"] == "OPEN_GOVERNED_RECEIVER"
        assert production["production_receiver"]["ready"] is True
        assert production["claims_withheld"] == ["PUBLICATION_COMPLETE"]
        cases += 1

        paper_path = root / "data/HIL_Canonical_Paper_v1_1.pdf"
        paper_path.write_bytes(b"corrupt")
        corrupt = derive_status(root)
        assert corrupt["announcement_state"] == "ANNOUNCEMENT_NOT_READY"
        assert corrupt["derivation"]["checks"]["canonical_pdf_sha256_valid"] is False
        cases += 1

    print(f"PASS: {cases} deterministic HIL announcement derivation cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
