#!/usr/bin/env python3
"""Check Site mirror activation evidence required by docs/SITE_MIRROR_HANDOFF.md."""

from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = REPO_ROOT / "docs" / "SITE_MIRROR_HANDOFF.md"
MANIFEST_PATH = REPO_ROOT / "papers" / "papers_manifest.json"
STATUS_PATH = REPO_ROOT / "docs" / "SITE_MIRROR_LIVE_VERIFICATION_STATUS.md"

REQUIRED_HANDOFF_TERMS = [
    "Goal: Site mirror activation hardening",
    "Repository: StegVerse-Labs/Site",
    "Source repository: GCAT-BCAT-Engine/Publisher",
    "Source path: papers",
    "Target path: papers",
    "Activation state: ready_for_live_mirror_verification",
    "Publisher dry-run workflow URL",
    "Publisher live dispatch workflow URL",
    "Site mirror workflow URL",
    "papers/papers_manifest.json source_repository",
    "Publisher verification tracker activation commit",
]

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

EXPECTED_MANIFEST_VALUES = {
    "source_repository": "GCAT-BCAT-Engine/Publisher",
    "source_path": "papers",
    "source_of_truth": "GCAT-BCAT-Engine/Publisher/papers",
    "target_repository": "StegVerse-Labs/Site",
    "target_path": "papers",
}

REQUIRED_ALIAS_PATHS = [
    Path("Papers.html"),
    Path("papers.html"),
    Path("papers/index.html"),
    Path("publisher/papers.html"),
    Path("publisher/papers/index.html"),
]


def result(name: str, status: str, detail: str) -> dict:
    return {"name": name, "status": status, "detail": detail}


def check_handoff() -> list[dict]:
    out: list[dict] = []
    if not HANDOFF_PATH.exists():
        return [result("handoff_exists", "fail", str(HANDOFF_PATH))]
    text = HANDOFF_PATH.read_text(encoding="utf-8")
    out.append(result("handoff_exists", "pass", str(HANDOFF_PATH)))
    for term in REQUIRED_HANDOFF_TERMS:
        out.append(result(f"handoff_term::{term}", "pass" if term in text else "fail", term))
    return out


def check_manifest() -> list[dict]:
    out: list[dict] = []
    if not MANIFEST_PATH.exists():
        return [result("manifest_exists", "fail", str(MANIFEST_PATH))]
    out.append(result("manifest_exists", "pass", str(MANIFEST_PATH)))
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return out + [result("manifest_json_valid", "fail", str(exc))]
    out.append(result("manifest_json_valid", "pass", str(MANIFEST_PATH)))

    for field in REQUIRED_MANIFEST_FIELDS:
        out.append(result(f"manifest_field::{field}", "pass" if field in manifest else "fail", field))
    for field, expected in EXPECTED_MANIFEST_VALUES.items():
        out.append(result(f"manifest_value::{field}", "pass" if manifest.get(field) == expected else "fail", f"expected {expected!r}, found {manifest.get(field)!r}"))
    if "entries" in manifest and "count" in manifest:
        entries = manifest.get("entries")
        out.append(result("manifest_count_matches_entries", "pass" if isinstance(entries, list) and manifest.get("count") == len(entries) else "fail", "count must equal len(entries)"))
    return out


def check_aliases() -> list[dict]:
    out: list[dict] = []
    for path in REQUIRED_ALIAS_PATHS:
        out.append(result(f"alias_exists::{path.as_posix()}", "pass" if (REPO_ROOT / path).exists() else "fail", path.as_posix()))
    return out


def write_status(results: list[dict]) -> None:
    passed = sum(1 for item in results if item["status"] == "pass")
    failed = sum(1 for item in results if item["status"] == "fail")
    blocked = failed > 0
    lines = [
        "# Site Mirror Live Verification Status",
        "",
        "## Summary",
        "",
        "```text",
        f"checks_passed: {passed}",
        f"checks_failed: {failed}",
        f"activation_blocked: {str(blocked).lower()}",
        "```",
        "",
        "## Findings",
        "",
    ]
    for item in results:
        lines.append(f"- `{item['status']}` — `{item['name']}` — {item['detail']}")
    lines.append("")
    lines.append("## Source of Truth")
    lines.append("")
    lines.append("`docs/SITE_MIRROR_HANDOFF.md` remains the current handoff and task source of truth.")
    lines.append("")
    STATUS_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    results = []
    results.extend(check_handoff())
    results.extend(check_manifest())
    results.extend(check_aliases())
    write_status(results)
    failed = [item for item in results if item["status"] == "fail"]
    if failed:
        print(f"site mirror activation evidence check failed: {len(failed)} failing checks")
        return 1
    print("valid: Site mirror activation evidence")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
