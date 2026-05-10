#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"Missing JSON file: {path}")
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Invalid JSON file {path}: {exc}") from exc
    if not isinstance(obj, dict):
        raise SystemExit(f"Expected JSON object: {path}")
    return obj


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def text_blob(request: dict[str, Any]) -> str:
    return json.dumps(request, sort_keys=True).lower()


def classify_from_indicators(request: dict[str, Any], policy: dict[str, Any]) -> list[str]:
    blob = text_blob(request)
    hits = []
    for indicator in policy.get("deny_by_default_indicators", []):
        if str(indicator).lower() in blob:
            hits.append(str(indicator))
    return hits


def bool_path(request: dict[str, Any], key: str) -> bool:
    proposed = request.get("proposed_transition", {})
    if not isinstance(proposed, dict):
        return False
    return bool(proposed.get(key, False))


def metric(request: dict[str, Any], key: str, default: float = 0.0) -> float:
    metrics = request.get("gcat_bcat_metrics", {})
    if not isinstance(metrics, dict):
        return default
    try:
        return float(metrics.get(key, default))
    except Exception:
        return default


def evaluate(request: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []
    warnings: list[str] = []

    if request.get("schema") != "stegverse.execution_request.v1":
        return receipt(request, policy, "FAIL_CLOSED", "Malformed or unsupported execution request schema.", reasons)

    decision_class = str(request.get("decision_class", "unknown"))
    classes = policy.get("decision_classes", {})
    class_policy = classes.get(decision_class)

    if not class_policy:
        return receipt(request, policy, "FAIL_CLOSED", f"Unknown decision_class: {decision_class}", reasons)

    human_required = bool(class_policy.get("human_required", True))
    human = request.get("human_approval", {}) if isinstance(request.get("human_approval", {}), dict) else {}
    human_approved = bool(human.get("approved", False))

    indicators = classify_from_indicators(request, policy)
    if indicators:
        warnings.append("deny_by_default_indicators=" + ",".join(sorted(set(indicators))))

    # Structural flags from proposed transition.
    structural_denies = []
    if bool_path(request, "touches_workflows"):
        structural_denies.append("touches_workflows")
    if bool_path(request, "touches_milestones"):
        structural_denies.append("touches_milestones")
    if bool_path(request, "expands_authority"):
        structural_denies.append("expands_authority")
    if bool_path(request, "expands_recursive_automation"):
        structural_denies.append("expands_recursive_automation")
    if bool_path(request, "uses_schedule"):
        structural_denies.append("uses_schedule")
    if bool_path(request, "uses_workflow_run"):
        structural_denies.append("uses_workflow_run")
    if bool_path(request, "uses_self_trigger"):
        structural_denies.append("uses_self_trigger")

    if not bool_path(request, "has_stop_condition"):
        reasons.append("missing_stop_condition")
    if not bool_path(request, "emits_receipt"):
        reasons.append("missing_receipt_output")

    thresholds = policy.get("gcat_bcat_thresholds", {})
    observability = metric(request, "observability")
    receiptability = metric(request, "receiptability")
    unboundedness = metric(request, "unboundedness")
    authority_expansion = metric(request, "authority_expansion")
    recursive_capacity = metric(request, "recursive_capacity")
    workflow_mutation = metric(request, "workflow_mutation")
    milestone_promotion = metric(request, "milestone_promotion")

    if observability < float(thresholds.get("minimum_observability", 0.75)):
        reasons.append("observability_below_threshold")
    if receiptability < float(thresholds.get("minimum_receiptability", 0.85)):
        reasons.append("receiptability_below_threshold")
    if unboundedness > float(thresholds.get("maximum_unboundedness", 0.0)):
        reasons.append("unboundedness_above_threshold")
    if authority_expansion > float(thresholds.get("max_authority_expansion_without_human", 0.0)):
        structural_denies.append("authority_expansion_metric")
    if recursive_capacity > float(thresholds.get("max_recursive_capacity_without_human", 0.0)):
        structural_denies.append("recursive_capacity_metric")
    if workflow_mutation > float(thresholds.get("max_workflow_mutation_without_human", 0.0)):
        structural_denies.append("workflow_mutation_metric")
    if milestone_promotion > float(thresholds.get("max_milestone_promotion_without_human", 0.0)):
        structural_denies.append("milestone_promotion_metric")

    if structural_denies:
        reasons.append("structural_authority_boundary=" + ",".join(sorted(set(structural_denies))))

    if human_required and not human_approved:
        reasons.append("human_design_authority_required")

    # Human approval can satisfy human-required class, but it does not override missing receipt/stop condition.
    hard_fail = any(reason in {"missing_stop_condition", "missing_receipt_output"} for reason in reasons)

    if hard_fail:
        verdict = "FAIL_CLOSED"
    elif reasons:
        verdict = "DENY"
    else:
        verdict = "ALLOW"

    if warnings and verdict == "ALLOW":
        # Indicators are warnings only when explicit structured fields remain safe.
        reasons.extend(warnings)
    elif warnings:
        reasons.extend(warnings)

    return receipt(request, policy, verdict, "; ".join(reasons) if reasons else "GCAT/BCAT gate allowed bounded implementation detail.", reasons)


def receipt(request: dict[str, Any], policy: dict[str, Any], verdict: str, reason: str, reasons: list[str]) -> dict[str, Any]:
    metrics = request.get("gcat_bcat_metrics", {}) if isinstance(request.get("gcat_bcat_metrics", {}), dict) else {}
    decision_class = request.get("decision_class", "unknown")
    classes = policy.get("decision_classes", {}) if isinstance(policy.get("decision_classes", {}), dict) else {}
    class_policy = classes.get(decision_class, {}) if isinstance(classes.get(decision_class, {}), dict) else {}
    human_required = bool(class_policy.get("human_required", True))

    return {
        "generated_at": utc_now(),
        "schema": "stegverse.execution_gate_receipt.v1",
        "formal_milestone": "MS-012G — Human Design Authority + GCAT/BCAT Execution Gate",
        "request_id": request.get("request_id"),
        "title": request.get("title"),
        "decision_class": decision_class,
        "human_required": human_required,
        "human_approved": bool((request.get("human_approval", {}) or {}).get("approved", False)) if isinstance(request.get("human_approval", {}), dict) else False,
        "gcat_bcat_verdict": verdict,
        "execution_verdict": verdict,
        "reason": reason,
        "reason_codes": reasons,
        "observability": metrics.get("observability"),
        "receiptability": metrics.get("receiptability"),
        "unboundedness": metrics.get("unboundedness"),
        "authority_expansion": metrics.get("authority_expansion"),
        "recursive_capacity": metrics.get("recursive_capacity"),
        "workflow_mutation": metrics.get("workflow_mutation"),
        "milestone_promotion": metrics.get("milestone_promotion"),
        "policy_id": policy.get("policy_id"),
        "request": request
    }


def write_markdown(path: Path, result: dict[str, Any]) -> None:
    lines = [
        "# Execution Gate Report",
        "",
        f"Generated: `{result.get('generated_at')}`",
        f"Milestone: `{result.get('formal_milestone')}`",
        f"Request: `{result.get('request_id')}`",
        f"Decision class: `{result.get('decision_class')}`",
        f"Human required: `{str(result.get('human_required')).lower()}`",
        f"Human approved: `{str(result.get('human_approved')).lower()}`",
        f"Verdict: `{result.get('execution_verdict')}`",
        "",
        "## Reason",
        "",
        result.get("reason", ""),
        "",
        "## Metrics",
        "",
        f"- `observability`: `{result.get('observability')}`",
        f"- `receiptability`: `{result.get('receiptability')}`",
        f"- `unboundedness`: `{result.get('unboundedness')}`",
        f"- `authority_expansion`: `{result.get('authority_expansion')}`",
        f"- `recursive_capacity`: `{result.get('recursive_capacity')}`",
        f"- `workflow_mutation`: `{result.get('workflow_mutation')}`",
        f"- `milestone_promotion`: `{result.get('milestone_promotion')}`",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", required=True)
    parser.add_argument("--policy", default="data/gates/human-design-authority-policy-v1.json")
    parser.add_argument("--out-dir", default="execution_gate_reports")
    args = parser.parse_args()

    request = load_json(Path(args.request))
    policy = load_json(Path(args.policy))
    result = evaluate(request, policy)

    out = Path(args.out_dir)
    write_json(out / "execution-gate-receipt.json", result)
    write_markdown(out / "execution-gate-report.md", result)

    print(json.dumps({
        "request_id": result.get("request_id"),
        "decision_class": result.get("decision_class"),
        "verdict": result.get("execution_verdict"),
        "human_required": result.get("human_required"),
        "reason": result.get("reason"),
    }, indent=2))

    return 0 if result.get("execution_verdict") == "ALLOW" else 1


if __name__ == "__main__":
    raise SystemExit(main())
