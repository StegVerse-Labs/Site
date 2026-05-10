#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def safe_member(name: str) -> bool:
    if not name or name.endswith("/"):
        return False
    p = Path(name)
    return not p.is_absolute() and ".." not in p.parts


def read_bundle_text(zf: zipfile.ZipFile, name: str) -> str:
    try:
        return zf.read(name).decode("utf-8", errors="replace")
    except Exception:
        return ""


def load_bundle_manifest(zf: zipfile.ZipFile) -> dict[str, Any] | None:
    for candidate in ("bundle-manifest.json", "manifest.json", "data/bundle-manifest.json"):
        if candidate in zf.namelist():
            try:
                return json.loads(read_bundle_text(zf, candidate))
            except Exception:
                return None
    return None


def infer_purpose(bundle: Path, zf: zipfile.ZipFile, manifest: dict[str, Any] | None) -> str:
    pieces = [bundle.name]
    if manifest:
        for key in ("purpose", "formal_milestone", "bundle_id"):
            if manifest.get(key):
                pieces.append(str(manifest[key]))
    if "README.md" in zf.namelist():
        pieces.append(read_bundle_text(zf, "README.md")[:2000])
    return "\n".join(pieces).lower()


def classify_purpose(
    bundle: Path,
    safe_entries: list[str],
    manifest: dict[str, Any] | None,
    deprecation_policy: dict[str, Any],
) -> dict[str, Any]:
    try:
        with zipfile.ZipFile(bundle, "r") as zf:
            purpose_text = infer_purpose(bundle, zf, manifest)
    except Exception:
        purpose_text = bundle.name.lower()

    critical_matches = []
    for entry in safe_entries:
        low = entry.lower()
        for rule in deprecation_policy.get("critical_preservation_rules", []):
            needle = str(rule.get("match_path_contains", "")).lower()
            if needle and needle in low:
                critical_matches.append({
                    "path": entry,
                    "status": rule.get("status", "critical_even_if_old"),
                    "reason": rule.get("reason", "Critical preservation rule matched.")
                })

    if critical_matches:
        return {
            "purpose_status": "critical_even_if_old",
            "reason": "One or more entries match critical preservation rules.",
            "critical_matches": critical_matches,
            "matched_supersession_rule": None
        }

    for rule in deprecation_policy.get("known_supersession_rules", []):
        needle = str(rule.get("older_purpose_contains", "")).lower()
        if needle and needle in purpose_text:
            return {
                "purpose_status": rule.get("status", "unknown"),
                "reason": f"Purpose matched supersession rule: {needle}",
                "critical_matches": [],
                "matched_supersession_rule": rule
            }

    if manifest and manifest.get("purpose"):
        return {
            "purpose_status": "active",
            "reason": "Manifest declares a purpose and no supersession/deprecation rule matched.",
            "critical_matches": [],
            "matched_supersession_rule": None
        }

    return {
        "purpose_status": "unknown",
        "reason": "No manifest purpose or supersession rule allowed a confident purpose classification.",
        "critical_matches": [],
        "matched_supersession_rule": None
    }


def review_bundle(bundle: Path, deprecation_policy: dict[str, Any]) -> dict[str, Any]:
    with zipfile.ZipFile(bundle, "r") as zf:
        names = sorted(zf.namelist())
        safe_entries = [n for n in names if safe_member(n)]
        unsafe_entries = [n for n in names if n not in safe_entries]
        manifest = load_bundle_manifest(zf)

    has_manifest = manifest is not None
    workflow_like = [n for n in safe_entries if n.startswith("github/workflows/") or n.startswith(".github/workflows/")]
    root_reports = [
        n for n in safe_entries
        if n in {
            "page-contract-report.json",
            "page-contract-report.md",
            "transition-replay-report.json",
            "transition-replay-report.md",
        }
    ]

    purpose = classify_purpose(bundle, safe_entries, manifest, deprecation_policy)

    verdict = "ALLOW"
    recommendation = "ingest"
    repair_eligible = True
    regenerate_eligible = True

    if unsafe_entries:
        verdict = "HUMAN_REVIEW_REQUIRED"
        recommendation = "reject_or_rebuild"
        repair_eligible = False
        regenerate_eligible = False
    elif workflow_like:
        verdict = "PRIVILEGED_EXECUTOR_REQUIRED"
        recommendation = "route_to_privileged_queue"
        repair_eligible = False
        regenerate_eligible = False
    elif purpose["purpose_status"] in {"deprecated", "obsolete", "superseded"}:
        verdict = "DO_NOT_REINGEST"
        recommendation = "preserve_receipt_and_do_not_regenerate_unless_requested"
        repair_eligible = False
        regenerate_eligible = False
    elif purpose["purpose_status"] == "critical_even_if_old":
        verdict = "PRESERVE_AND_INDEX"
        recommendation = "preserve_as_historical_evidence"
        repair_eligible = False
        regenerate_eligible = False
    elif purpose["purpose_status"] == "unknown":
        verdict = "HUMAN_REVIEW_REQUIRED"
        recommendation = "human_review_purpose_before_repair"
        repair_eligible = False
        regenerate_eligible = False
    elif len([n for n in safe_entries if n != "README.md"]) > 5 and not has_manifest:
        verdict = "SANDBOX_REQUIRED"
        recommendation = "regenerate_with_manifest"
    elif root_reports:
        verdict = "ALLOW_WITH_ARTIFACT_ROUTING"
        recommendation = "ingest_with_artifact_routing"

    return {
        "generated_at": utc_now(),
        "schema": "stegverse.sandbox_bundle_review_report.v1",
        "formal_milestone": "MS-012F — Sandbox Repair and Candidate Construction",
        "bundle": str(bundle),
        "verdict": verdict,
        "recommendation": recommendation,
        "purpose_status": purpose["purpose_status"],
        "purpose_reason": purpose["reason"],
        "matched_supersession_rule": purpose["matched_supersession_rule"],
        "critical_matches": purpose["critical_matches"],
        "repair_eligible": repair_eligible,
        "regenerate_eligible": regenerate_eligible,
        "has_manifest": has_manifest,
        "safe_entries": safe_entries,
        "unsafe_entries": unsafe_entries,
        "workflow_like_entries": workflow_like,
        "root_report_artifacts": root_reports,
        "silent_repair_performed": False
    }


def write_markdown(report: dict[str, Any], path: Path) -> None:
    lines = [
        "# Sandbox Bundle Review Report",
        "",
        f"Generated: `{report['generated_at']}`",
        f"Bundle: `{report['bundle']}`",
        f"Verdict: `{report['verdict']}`",
        f"Recommendation: `{report['recommendation']}`",
        "",
        "## Purpose Classification",
        "",
        f"- `purpose_status`: `{report['purpose_status']}`",
        f"- `purpose_reason`: {report['purpose_reason']}",
        f"- `repair_eligible`: `{str(report['repair_eligible']).lower()}`",
        f"- `regenerate_eligible`: `{str(report['regenerate_eligible']).lower()}`",
        "",
        "## Shape Findings",
        "",
        f"- `has_manifest`: `{str(report['has_manifest']).lower()}`",
        f"- `unsafe_entries`: `{len(report['unsafe_entries'])}`",
        f"- `workflow_like_entries`: `{len(report['workflow_like_entries'])}`",
        f"- `root_report_artifacts`: `{len(report['root_report_artifacts'])}`",
        f"- `silent_repair_performed`: `{str(report['silent_repair_performed']).lower()}`",
        "",
    ]

    if report.get("matched_supersession_rule"):
        lines.extend([
            "## Matched Supersession Rule",
            "",
            "```json",
            json.dumps(report["matched_supersession_rule"], indent=2),
            "```",
            "",
        ])

    if report.get("critical_matches"):
        lines.extend(["## Critical Preservation Matches", ""])
        for item in report["critical_matches"]:
            lines.append(f"- `{item['path']}` — {item['reason']}")
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", required=True)
    parser.add_argument("--deprecation-policy", default="data/deprecation-policy-v1.json")
    parser.add_argument("--out-dir", default="sandbox_reports")
    args = parser.parse_args()

    deprecation_policy = load_json(Path(args.deprecation_policy), {"known_supersession_rules": [], "critical_preservation_rules": []})
    report = review_bundle(Path(args.bundle), deprecation_policy)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "sandbox-review-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    write_markdown(report, out_dir / "sandbox-review-report.md")

    print(json.dumps({
        "verdict": report["verdict"],
        "purpose_status": report["purpose_status"],
        "recommendation": report["recommendation"]
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
