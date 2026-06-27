#!/usr/bin/env python3
"""Write a local completion receipt for Site repository-managed work."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT_MD = ROOT / "docs" / "SITE_LOCAL_COMPLETION_RECEIPT.md"
OUT_JSON = ROOT / "docs" / "SITE_LOCAL_COMPLETION_RECEIPT.json"

REQUIRED_PATHS = [
    "docs/SITE_MIRROR_HANDOFF.md",
    "docs/SITE_MANUAL_TASK_ELIMINATION.md",
    "docs/SITE_TASK_ELIMINATION_GUARD.md",
    "docs/SITE_EXTERNAL_EVIDENCE_STATE.md",
    "docs/SITE_EXTERNAL_EVIDENCE_STATE.json",
    "docs/SITE_FINAL_GOAL_STATUS.md",
    "docs/SITE_FINAL_GOAL_STATUS.json",
    "scripts/check_site_manual_task_elimination.py",
    "scripts/write_site_external_evidence_state.py",
    "scripts/update_site_final_goal_status.py",
    "scripts/check_site_final_goal_status.py",
    "scripts/check_site_final_activation_pending.py",
    ".github/workflows/site-autonomous-continuation.yml",
    ".github/workflows/site-task-elimination-guard.yml",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display_path(path: str) -> str:
    return path[1:] if path.startswith(".") else path


def build_receipt() -> dict[str, object]:
    artifacts = []
    missing = []
    for rel in REQUIRED_PATHS:
        path = ROOT / rel
        exists = path.exists()
        if not exists:
            missing.append(rel)
        artifacts.append({
            "path": rel,
            "ios_display_path": display_path(rel),
            "exists": exists,
            "sha256": sha256(path) if exists and path.is_file() else None,
        })

    local_complete = not missing
    return {
        "schema": "site_local_completion_receipt.v0.1",
        "repository": "StegVerse-Labs/Site",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "local_completion_state": "complete" if local_complete else "incomplete",
        "activation_state": "pending_external_evidence",
        "artifacts": artifacts,
        "missing": missing,
        "non_claims": [
            "This receipt does not activate the Site mirror.",
            "This receipt does not make Site proof authority.",
            "This receipt does not make Site source authority for Publisher, TT, or Governance Observatory records.",
            "This receipt does not grant commit-time permission.",
        ],
    }


def render_markdown(receipt: dict[str, object]) -> str:
    lines = [
        "# Site Local Completion Receipt",
        "",
        "## Status",
        "",
        "```text",
        f"local_completion_state: {receipt['local_completion_state']}",
        f"activation_state: {receipt['activation_state']}",
        f"generated_at: {receipt['generated_at']}",
        "repository: StegVerse-Labs/Site",
        "```",
        "",
        "## Artifacts",
        "",
        "| Path | iOS Display Path | Exists | SHA-256 |",
        "|---|---|---:|---|",
    ]
    for artifact in receipt["artifacts"]:  # type: ignore[index]
        lines.append(
            f"| `{artifact['path']}` | `{artifact['ios_display_path']}` | {str(artifact['exists']).lower()} | `{artifact['sha256'] or ''}` |"
        )
    lines.extend([
        "",
        "## Boundary",
        "",
        "This receipt confirms local repository-managed continuation surfaces exist. It does not activate the Site mirror, grant commit-time permission, or move source authority into Site.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    receipt = build_receipt()
    OUT_JSON.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_markdown(receipt), encoding="utf-8")
    print(json.dumps({"status": receipt["local_completion_state"], "activation_state": receipt["activation_state"]}, indent=2))
    return 0 if receipt["local_completion_state"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())
