#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TT_STATUS = ROOT / "docs" / "SITE_TT_CODE_REPRESENTATION_STATUS.json"
GOV_STATUS = ROOT / "docs" / "SITE_GOVERNANCE_OBSERVATORY_STATUS.json"
LOCAL_RECEIPT = ROOT / "docs" / "SITE_LOCAL_COMPLETION_RECEIPT.json"
SYSTEM_BOUNDARY_STATUS = ROOT / "data" / "governance" / "system-boundary-status.v0.1.json"
OUT_JSON = ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.json"
OUT_MD = ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.md"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {"missing": True, "path": str(path.relative_to(ROOT))}
    return json.loads(path.read_text(encoding="utf-8"))


def synchronize_system_boundary_status() -> None:
    subprocess.run(
        [sys.executable, "scripts/sync_system_boundary_status.py"],
        cwd=ROOT,
        check=True,
    )


def main() -> int:
    synchronize_system_boundary_status()
    generated_at = datetime.now(timezone.utc).isoformat()
    tt = read_json(TT_STATUS)
    gov = read_json(GOV_STATUS)
    local_receipt = read_json(LOCAL_RECEIPT)
    system_boundary = read_json(SYSTEM_BOUNDARY_STATUS)

    tt_ready = tt.get("status") == "PASS" and tt.get("fail_closed") is False
    gov_ready = gov.get("schema") == "site_governance_observatory_status.v0.1" and gov.get("mirror_status") == "active_public_status_surface"
    local_receipt_ready = local_receipt.get("schema") == "site_local_completion_receipt.v0.1" and local_receipt.get("local_completion_state") == "complete" and local_receipt.get("activation_state") == "pending_external_evidence"
    system_boundary_verified = system_boundary.get("activation_state") == "VERIFIED" and system_boundary.get("verified") is True and system_boundary.get("downstream_propagation_allowed") is True
    ready = tt_ready and gov_ready and local_receipt_ready and system_boundary_verified

    status = {
        "schema": "site_final_goal_status.v0.1",
        "repository": "StegVerse-Labs/Site",
        "generated_at": generated_at,
        "goal_status": "ready" if ready else "pending_external_evidence",
        "gates": {
            "tt_bundle_fed_status_ready": tt_ready,
            "governance_observatory_status_ready": gov_ready,
            "local_completion_receipt_ready": local_receipt_ready,
            "system_boundary_status_verified": system_boundary_verified,
        },
        "source_boundaries": {
            "publisher": "GCAT-BCAT-Engine/Publisher remains paper source of truth.",
            "tt": "Admissible-Existence/TT remains TT source of truth.",
            "governance_observatory": "StegVerse-Labs/governance-observatory remains source-intake source of truth.",
            "system_boundary": "StegVerse-org/StegVerse-SDK remains system-boundary activation-status source of truth.",
        },
        "non_claims": [
            "This status file does not define a StegVerse formalism.",
            "This status file does not prove transition admissibility.",
            "This status file does not issue commit-time permission.",
            "System-boundary verification does not enable production binding or release authority.",
            "This status file does not make Site the source repository for Publisher, TT, Governance Observatory, or SDK records.",
        ],
    }

    markdown = "\n".join([
        "# Site Final Goal Status",
        "",
        "## Status",
        "",
        "```text",
        f"goal_status: {status['goal_status']}",
        f"generated_at: {generated_at}",
        "repository: StegVerse-Labs/Site",
        "```",
        "",
        "## Gates",
        "",
        "```text",
        f"tt_bundle_fed_status_ready: {str(tt_ready).lower()}",
        f"governance_observatory_status_ready: {str(gov_ready).lower()}",
        f"local_completion_receipt_ready: {str(local_receipt_ready).lower()}",
        f"system_boundary_status_verified: {str(system_boundary_verified).lower()}",
        "```",
        "",
        "## Source Boundaries",
        "",
        "```text",
        "GCAT-BCAT-Engine/Publisher remains paper source of truth.",
        "Admissible-Existence/TT remains TT source of truth.",
        "StegVerse-Labs/governance-observatory remains source-intake source of truth.",
        "StegVerse-org/StegVerse-SDK remains system-boundary activation-status source of truth.",
        "```",
        "",
        "## Non-Claims",
        "",
        "```text",
        *status["non_claims"],
        "```",
        "",
    ])

    OUT_JSON.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    print(json.dumps({"goal_status": status["goal_status"], "tt_ready": tt_ready, "gov_ready": gov_ready, "local_receipt_ready": local_receipt_ready, "system_boundary_status_verified": system_boundary_verified}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
