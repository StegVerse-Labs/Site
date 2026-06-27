#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TT_STATUS = ROOT / "docs" / "SITE_TT_CODE_REPRESENTATION_STATUS.json"
GOV_STATUS = ROOT / "docs" / "SITE_GOVERNANCE_OBSERVATORY_STATUS.json"
OUT_JSON = ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.json"
OUT_MD = ROOT / "docs" / "SITE_FINAL_GOAL_STATUS.md"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {"missing": True, "path": str(path.relative_to(ROOT))}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    generated_at = datetime.now(timezone.utc).isoformat()
    tt = read_json(TT_STATUS)
    gov = read_json(GOV_STATUS)

    tt_ready = tt.get("status") == "PASS" and tt.get("fail_closed") is False
    gov_ready = gov.get("schema") == "site_governance_observatory_status.v0.1" and gov.get("mirror_status") == "active_public_status_surface"
    ready = tt_ready and gov_ready

    status = {
        "schema": "site_final_goal_status.v0.1",
        "repository": "StegVerse-Labs/Site",
        "generated_at": generated_at,
        "goal_status": "ready" if ready else "pending_external_evidence",
        "gates": {
            "tt_bundle_fed_status_ready": tt_ready,
            "governance_observatory_status_ready": gov_ready
        },
        "source_boundaries": {
            "publisher": "GCAT-BCAT-Engine/Publisher remains paper source of truth.",
            "tt": "Admissible-Existence/TT remains TT source of truth.",
            "governance_observatory": "StegVerse-Labs/governance-observatory remains source-intake source of truth."
        },
        "non_claims": [
            "This status file does not define a StegVerse formalism.",
            "This status file does not prove transition admissibility.",
            "This status file does not issue commit-time permission.",
            "This status file does not make Site the source repository for Publisher, TT, or Governance Observatory records."
        ]
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
        "```",
        "",
        "## Source Boundaries",
        "",
        "```text",
        "GCAT-BCAT-Engine/Publisher remains paper source of truth.",
        "Admissible-Existence/TT remains TT source of truth.",
        "StegVerse-Labs/governance-observatory remains source-intake source of truth.",
        "```",
        "",
        "## Non-Claims",
        "",
        "```text",
        *status["non_claims"],
        "```",
        ""
    ])

    OUT_JSON.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    print(json.dumps({"goal_status": status["goal_status"], "tt_ready": tt_ready, "gov_ready": gov_ready}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
