from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MD = ROOT / "docs" / "SITE_ENTITY_SANDBOX_RUNNER_STATUS.md"
JS = ROOT / "docs" / "SITE_ENTITY_SANDBOX_RUNNER_STATUS.json"

REQUIRED_MD = [
    "StegGhost/entity-sandbox-runner",
    "admissibility_plane_activation_candidate",
    "installed_display_only",
    "pending_external_evidence",
    "Site does not certify runtime admissibility",
    "Site does not issue commit-time permission",
]

REQUIRED_JSON_KEYS = [
    "source_repo",
    "release_goal",
    "site_status",
    "release_activation_state",
    "source_packet_paths",
    "site_non_claims",
    "required_source_evidence",
]


def main() -> None:
    errors: list[str] = []

    if not MD.exists():
        errors.append(f"missing:{MD}")
    else:
        text = MD.read_text(encoding="utf-8")
        for token in REQUIRED_MD:
            if token not in text:
                errors.append(f"missing_md_token:{token}")

    if not JS.exists():
        errors.append(f"missing:{JS}")
    else:
        data = json.loads(JS.read_text(encoding="utf-8"))
        for key in REQUIRED_JSON_KEYS:
            if key not in data:
                errors.append(f"missing_json_key:{key}")
        if data.get("source_repo") != "StegGhost/entity-sandbox-runner":
            errors.append("source_repo_mismatch")
        if data.get("site_status") != "installed_display_only":
            errors.append("site_status_must_remain_display_only")
        if data.get("release_activation_state") != "pending_external_evidence":
            errors.append("release_activation_state_must_remain_pending_external_evidence")

    if errors:
        print(json.dumps({"status": "failed", "errors": errors}, indent=2))
        raise SystemExit(1)

    print(json.dumps({"status": "ok", "checked": [str(MD), str(JS)]}, indent=2))


if __name__ == "__main__":
    main()
