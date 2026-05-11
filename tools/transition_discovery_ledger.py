#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FORMAL_MILESTONE = "MS-012K — Transition Discovery Ledger"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists() or not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def stable_hash(obj: Any) -> str:
    return sha_text(json.dumps(obj, sort_keys=True, separators=(",", ":")))


def receipt_hash_from_path(root: Path, path: str | None) -> str | None:
    if not path:
        return None
    p = root / path
    if p.exists() and p.is_file():
        return hashlib.sha256(p.read_bytes()).hexdigest()
    return None


def infer_transition_from_ingestion(receipt: dict[str, Any], policy: dict[str, Any]) -> tuple[str | None, str]:
    rules = policy.get("matching_rules", {})
    verdict = str(receipt.get("verdict", ""))
    route = str(receipt.get("route", ""))
    bundle_class = str(receipt.get("bundle_class", ""))
    reason = str(receipt.get("reason", ""))

    if verdict == "ALLOW" and route == "ingest":
        return rules.get("allow_ingest"), "allow_ingest"
    if "already" in verdict.lower() or "already" in reason.lower():
        return rules.get("already_seen"), "already_seen"
    if route == "sandbox_queue" or verdict == "SANDBOX_REQUIRED":
        if "bundle_ingest.py" in reason or "ingestion" in bundle_class:
            return rules.get("engine_mutation"), "engine_mutation"
        return rules.get("engine_mutation") if "engine" in bundle_class else (rules.get("incoming_zip"), "incoming_zip")
    if route == "privileged_queue" or verdict == "PRIVILEGED_EXECUTOR_REQUIRED" or "workflow" in bundle_class:
        return rules.get("workflow_mutation"), "workflow_mutation"
    if route == "failed_bundles" or "STALE" in verdict or "FAIL" in verdict:
        return rules.get("already_seen") if "already" in reason.lower() else (rules.get("unsafe_path"), "unsafe_or_failed")
    if route:
        return rules.get("incoming_zip"), "incoming_zip"
    return None, "unknown_ingestion_outcome"


def infer_action_from_ingestion(receipt: dict[str, Any]) -> str:
    verdict = str(receipt.get("verdict", ""))
    route = str(receipt.get("route", ""))
    bundle_class = str(receipt.get("bundle_class", ""))

    if verdict == "ALLOW" and route == "ingest":
        return "archive_installed_bundle"
    if route == "failed_bundles" or "STALE" in verdict or "FAIL" in verdict:
        return "quarantine_stale_or_failed"
    if route == "sandbox_queue" or verdict == "SANDBOX_REQUIRED":
        return "hold_for_sandbox"
    if route == "privileged_queue" or verdict == "PRIVILEGED_EXECUTOR_REQUIRED" or "workflow" in bundle_class:
        return "prepare_privileged_review"
    return "observe_state"


def infer_transition_from_sandbox(report: dict[str, Any], policy: dict[str, Any]) -> tuple[str | None, str]:
    rules = policy.get("matching_rules", {})
    classification = str(report.get("classification", ""))
    verdict = str(report.get("verdict", ""))
    reason = str(report.get("reason", ""))

    if classification == "repair_candidate_created" or verdict == "ALLOW_REENTRY":
        return rules.get("safe_unmanifested_sandbox"), "safe_unmanifested_sandbox"
    if classification == "privileged_review_required":
        return rules.get("privileged_review"), "privileged_review"
    if classification == "manual_review_required" and "bundle_ingest.py" in reason:
        return rules.get("engine_mutation"), "engine_mutation"
    if classification in {"unrepairable", "invalid_zip"}:
        return rules.get("unsafe_path"), "unsafe_path"
    return None, "unknown_sandbox_outcome"


def infer_action_from_sandbox(report: dict[str, Any]) -> str:
    classification = str(report.get("classification", ""))
    verdict = str(report.get("verdict", ""))

    if classification == "repair_candidate_created" or verdict == "ALLOW_REENTRY":
        return "construct_sandbox_candidate"
    if classification == "privileged_review_required":
        return "prepare_privileged_review"
    if classification in {"unrepairable", "invalid_zip"}:
        return "quarantine_stale_or_failed"
    return "observe_state"


def transition_exists(authority_map: dict[str, Any], transition_id: str | None) -> bool:
    return bool(transition_id and transition_id in authority_map.get("transition_elements", {}))


def action_is_unlocked(authority_map: dict[str, Any], transition_id: str | None, action_class: str | None) -> bool:
    if not transition_id or not action_class:
        return False
    transition = authority_map.get("transition_elements", {}).get(transition_id, {})
    return action_class in transition.get("unlocked_action_classes", [])


def action_requires_human(authority_map: dict[str, Any], action_class: str | None) -> bool:
    if not action_class:
        return False
    action = authority_map.get("action_classes", {}).get(action_class, {})
    return bool(action.get("human_approval_required", False))


def sandbox_required(authority_map: dict[str, Any], action_class: str | None) -> bool:
    if not action_class:
        return False
    action = authority_map.get("action_classes", {}).get(action_class, {})
    return bool(action.get("sandbox_required", False))


def make_entry(
    *,
    source_report: str,
    source_kind: str,
    observed_path: str | None,
    event_type: str,
    tool_invoked: str,
    transition_id: str | None,
    match_reason: str,
    action_class: str,
    route: str | None,
    result: str | None,
    receipt_path: str | None,
    root: Path,
    authority_map: dict[str, Any],
) -> dict[str, Any]:
    entry = {
        "schema": "stegverse.transition_discovery_entry.v1",
        "formal_milestone": FORMAL_MILESTONE,
        "observed_at": utc_now(),
        "source_report": source_report,
        "source_kind": source_kind,
        "observed_path": observed_path,
        "event_type": event_type,
        "tool_invoked": tool_invoked,
        "transition_element_matched": transition_id,
        "transition_match_reason": match_reason,
        "action_class_unlocked": action_class,
        "action_class_is_unlocked_by_transition": action_is_unlocked(authority_map, transition_id, action_class),
        "authority_level": authority_map.get("action_classes", {}).get(action_class, {}).get("authority_level"),
        "route": route,
        "result": result,
        "receipt_path": receipt_path,
        "receipt_hash": receipt_hash_from_path(root, receipt_path),
        "human_approval_required": action_requires_human(authority_map, action_class),
        "sandbox_required": sandbox_required(authority_map, action_class),
        "transition_exists": transition_exists(authority_map, transition_id),
    }
    entry["entry_hash"] = stable_hash({k: v for k, v in entry.items() if k != "entry_hash"})
    return entry


def collect_ingestion_entries(root: Path, policy: dict[str, Any], authority_map: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for rel in policy.get("inputs", {}).get("ingestion_reports", []):
        obj = load_json(root / rel, None)
        if not isinstance(obj, dict):
            continue

        reports = obj.get("reports")
        if not isinstance(reports, list):
            reports = [obj]

        for report in reports:
            if not isinstance(report, dict):
                continue

            receipt = report.get("receipt", {})
            if not isinstance(receipt, dict):
                receipt = {}

            transition_id, match_reason = infer_transition_from_ingestion(receipt, policy)
            action_class = infer_action_from_ingestion(receipt)
            bundle = receipt.get("bundle_name") or receipt.get("file_name")
            route = receipt.get("route")
            verdict = receipt.get("verdict")

            receipt_path = "ingestion_reports/bundle-queue-report.json" if "queue" in rel else "ingestion_reports/bundle-ingestion-report.json"

            entries.append(make_entry(
                source_report=rel,
                source_kind="ingestion",
                observed_path=f"incoming/{bundle}" if bundle else None,
                event_type=str(verdict or "ingestion_report"),
                tool_invoked="tools/bundle_ingest.py",
                transition_id=transition_id,
                match_reason=match_reason,
                action_class=action_class,
                route=str(route) if route else None,
                result=str(verdict) if verdict else None,
                receipt_path=receipt_path,
                root=root,
                authority_map=authority_map,
            ))

    return entries


def collect_sandbox_entries(root: Path, policy: dict[str, Any], authority_map: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    sandbox_dir = root / policy.get("inputs", {}).get("sandbox_report_dir", "sandbox_reports")
    if not sandbox_dir.exists():
        return entries

    for path in sorted(sandbox_dir.glob("*.json")):
        obj = load_json(path, None)
        if not isinstance(obj, dict):
            continue

        reports = obj.get("reports") if obj.get("schema") == "stegverse.ephemeral_sandbox_queue_report.v1" else [obj]
        if not isinstance(reports, list):
            continue

        for report in reports:
            if not isinstance(report, dict):
                continue

            transition_id, match_reason = infer_transition_from_sandbox(report, policy)
            action_class = infer_action_from_sandbox(report)
            bundle = report.get("bundle_name")
            classification = report.get("classification")
            verdict = report.get("verdict")

            entries.append(make_entry(
                source_report=path.as_posix(),
                source_kind="sandbox",
                observed_path=f"sandbox_queue/{bundle}" if bundle else None,
                event_type=str(classification or verdict or "sandbox_report"),
                tool_invoked="tools/ephemeral_sandbox_runner.py",
                transition_id=transition_id,
                match_reason=match_reason,
                action_class=action_class,
                route="incoming" if report.get("candidate_path") else None,
                result=str(verdict or classification),
                receipt_path=path.as_posix(),
                root=root,
                authority_map=authority_map,
            ))

    return entries


def collect_authority_entries(root: Path, policy: dict[str, Any], authority_map: dict[str, Any]) -> list[dict[str, Any]]:
    rel = policy.get("inputs", {}).get("authority_audit_report", "transition_authority_reports/transition-authority-audit-report.json")
    obj = load_json(root / rel, None)
    if not isinstance(obj, dict):
        return []

    entries = []
    for audit in obj.get("audits", []):
        if not isinstance(audit, dict):
            continue

        action_class = audit.get("action_class") or "observe_state"
        result = audit.get("verdict")
        transition_id = None
        match_reason = "authority_audit_observation"

        if result == "EXCEEDS_UNLOCKED_AUTHORITY":
            transition_id = policy.get("matching_rules", {}).get("authority_expansion")
            match_reason = "action_exceeds_unlocked_authority"

        entries.append(make_entry(
            source_report=rel,
            source_kind="authority_audit",
            observed_path=None,
            event_type=str(result or "authority_audit"),
            tool_invoked="tools/transition_authority_audit.py",
            transition_id=transition_id,
            match_reason=match_reason,
            action_class=str(action_class),
            route=None,
            result=str(result),
            receipt_path=rel,
            root=root,
            authority_map=authority_map,
        ))

    return entries


def candidate_needed(entry: dict[str, Any], policy: dict[str, Any]) -> bool:
    rules = policy.get("candidate_rules", {})
    if rules.get("new_candidate_when_no_transition_match", True) and not entry.get("transition_element_matched"):
        return True
    if rules.get("new_candidate_when_action_exceeds_unlocked_authority", True) and not entry.get("action_class_is_unlocked_by_transition"):
        if not entry.get("human_approval_required"):
            return True
    if rules.get("new_candidate_when_unknown_route", True) and entry.get("route") in {"unknown", None} and entry.get("source_kind") in {"ingestion", "sandbox"}:
        if entry.get("result") not in {"ALLOW", "ALLOW_REENTRY"}:
            return True
    return False


def build_candidates(entries: list[dict[str, Any]], policy: dict[str, Any]) -> list[dict[str, Any]]:
    candidates = []
    seen = set()
    for entry in entries:
        if not candidate_needed(entry, policy):
            continue

        key = (
            entry.get("source_kind"),
            entry.get("event_type"),
            entry.get("action_class_unlocked"),
            entry.get("transition_match_reason"),
        )
        if key in seen:
            continue
        seen.add(key)

        candidate = {
            "schema": "stegverse.transition_element_candidate.v1",
            "candidate_id": "TEC-" + stable_hash(key)[:12],
            "generated_at": utc_now(),
            "reason": "Observed outcome is not fully covered by current transition/action mapping.",
            "source_kind": entry.get("source_kind"),
            "event_type": entry.get("event_type"),
            "suggested_action_class": entry.get("action_class_unlocked"),
            "transition_match_reason": entry.get("transition_match_reason"),
            "evidence_entry_hash": entry.get("entry_hash"),
            "human_review_required": True,
            "authority_granted": False,
            "next_step": "Review candidate before adding it to the authority map."
        }
        candidates.append(candidate)
    return candidates


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def write_summary_md(path: Path, summary: dict[str, Any], entries: list[dict[str, Any]], candidates: list[dict[str, Any]]) -> None:
    lines = [
        "# Transition Discovery Summary",
        "",
        f"Generated: `{summary.get('generated_at')}`",
        f"Policy: `{summary.get('policy_id')}`",
        "",
        "## Counts",
        "",
    ]
    for key, value in summary.get("counts", {}).items():
        lines.append(f"- `{key}`: `{value}`")

    lines.extend(["", "## Recent Entries", ""])
    for entry in entries[-20:]:
        lines.append(
            f"- `{entry.get('source_kind')}` `{entry.get('event_type')}` → "
            f"`{entry.get('transition_element_matched')}` / `{entry.get('action_class_unlocked')}` "
            f"unlocked=`{entry.get('action_class_is_unlocked_by_transition')}`"
        )

    lines.extend(["", "## Candidate Elements", ""])
    if not candidates:
        lines.append("No new transition element candidates produced.")
    else:
        for candidate in candidates:
            lines.append(
                f"- `{candidate.get('candidate_id')}` `{candidate.get('event_type')}` "
                f"action=`{candidate.get('suggested_action_class')}` — {candidate.get('reason')}"
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_candidates_md(path: Path, candidates: list[dict[str, Any]]) -> None:
    lines = ["# Transition Element Candidates", ""]
    if not candidates:
        lines.append("No new transition element candidates produced.")
    else:
        for candidate in candidates:
            lines.extend([
                f"## {candidate.get('candidate_id')}",
                "",
                f"- Source kind: `{candidate.get('source_kind')}`",
                f"- Event type: `{candidate.get('event_type')}`",
                f"- Suggested action class: `{candidate.get('suggested_action_class')}`",
                f"- Evidence entry hash: `{candidate.get('evidence_entry_hash')}`",
                f"- Human review required: `{candidate.get('human_review_required')}`",
                f"- Authority granted: `{candidate.get('authority_granted')}`",
                f"- Reason: {candidate.get('reason')}",
                "",
            ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--policy", default="data/transition-table/transition-discovery-policy-v1.json")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    policy = load_json(root / args.policy, None)
    if not isinstance(policy, dict):
        raise SystemExit(f"Missing or invalid policy: {args.policy}")

    authority_map_path = policy.get("inputs", {}).get("authority_map", "data/transition-table/transition-element-action-authority-map-v1.json")
    authority_map = load_json(root / authority_map_path, None)
    if not isinstance(authority_map, dict):
        raise SystemExit(f"Missing or invalid authority map: {authority_map_path}")

    entries = []
    entries.extend(collect_ingestion_entries(root, policy, authority_map))
    entries.extend(collect_sandbox_entries(root, policy, authority_map))
    entries.extend(collect_authority_entries(root, policy, authority_map))

    # De-duplicate by entry hash.
    deduped = []
    seen_hashes = set()
    for entry in entries:
        h = entry.get("entry_hash")
        if h in seen_hashes:
            continue
        seen_hashes.add(h)
        deduped.append(entry)

    candidates = build_candidates(deduped, policy)

    outputs = policy.get("outputs", {})
    ledger_jsonl = root / outputs.get("ledger_jsonl", "transition_discovery_reports/transition-discovery-ledger.jsonl")
    ledger_json = root / outputs.get("ledger_json", "transition_discovery_reports/transition-discovery-ledger.json")
    candidates_json = root / outputs.get("candidate_elements_json", "transition_discovery_reports/transition-element-candidates.json")
    candidates_md = root / outputs.get("candidate_elements_md", "transition_discovery_reports/transition-element-candidates.md")
    summary_json = root / outputs.get("summary_json", "transition_discovery_reports/transition-discovery-summary.json")
    summary_md = root / outputs.get("summary_md", "transition_discovery_reports/transition-discovery-summary.md")

    write_jsonl(ledger_jsonl, deduped)
    write_json(ledger_json, {"schema": "stegverse.transition_discovery_ledger.v1", "generated_at": utc_now(), "entries": deduped})
    write_json(candidates_json, {"schema": "stegverse.transition_element_candidates.v1", "generated_at": utc_now(), "candidates": candidates})
    write_candidates_md(candidates_md, candidates)

    counts = {
        "entries_total": len(deduped),
        "candidate_elements": len(candidates),
        "entries_with_transition_match": sum(1 for e in deduped if e.get("transition_element_matched")),
        "entries_unlocked_by_transition": sum(1 for e in deduped if e.get("action_class_is_unlocked_by_transition")),
        "human_approval_required": sum(1 for e in deduped if e.get("human_approval_required")),
        "sandbox_required": sum(1 for e in deduped if e.get("sandbox_required")),
    }
    summary = {
        "schema": "stegverse.transition_discovery_summary.v1",
        "generated_at": utc_now(),
        "policy_id": policy.get("policy_id"),
        "formal_milestone": FORMAL_MILESTONE,
        "counts": counts,
        "outputs": outputs,
    }
    write_json(summary_json, summary)
    write_summary_md(summary_md, summary, deduped, candidates)

    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
