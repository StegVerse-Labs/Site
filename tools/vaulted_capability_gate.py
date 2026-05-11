#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists() or not path.is_file():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Could not read JSON {path}: {exc}") from exc


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2), encoding="utf-8")


def stable_hash(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def missing_fields(obj: dict[str, Any], fields: list[str]) -> list[str]:
    return [field for field in fields if field not in obj or obj.get(field) in (None, "", {})]


def evaluate(request: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
    reasons: list[str] = []

    if request.get("schema") != "stegverse.vaulted_capability_request.v1":
        return "FAIL_CLOSED", ["unsupported request schema"]

    missing = missing_fields(request, policy.get("required_fields", []))
    if missing:
        return "FAIL_CLOSED", [f"missing required fields: {', '.join(missing)}"]

    capability_type = request.get("capability_type")
    if capability_type in policy.get("denied_capability_types", []):
        return "DENY", [f"denied capability type: {capability_type}"]

    if capability_type not in policy.get("allowed_capability_types", []):
        return "HOLD_FOR_VAULT_REVIEW", [f"capability type not explicitly allowed: {capability_type}"]

    if request.get("secret_material") not in (None, "", {}):
        return "DENY", ["request contains secret_material; raw secret exposure is not allowed"]

    authority_basis = request.get("authority_basis", {})
    missing_authority = missing_fields(authority_basis, policy.get("required_authority_basis", []))
    if missing_authority:
        return "FAIL_CLOSED", [f"missing authority basis: {', '.join(missing_authority)}"]

    scope = request.get("scope", {})
    missing_scope = missing_fields(scope, policy.get("required_scope_fields", []))
    if missing_scope:
        return "FAIL_CLOSED", [f"missing scope fields: {', '.join(missing_scope)}"]

    owner_claim = request.get("owner_claim", {})
    pricing_basis = request.get("pricing_basis", {})
    revocation_policy = request.get("revocation_policy", {})

    if not revocation_policy.get("revocable", False):
        return "DENY", ["capability is not revocable"]

    if not revocation_policy.get("reuse_requires_revalidation", False):
        return "DENY", ["capability reuse does not require revalidation"]

    if pricing_basis.get("tvc_required") is True and not owner_claim.get("verified", False):
        return "HOLD_FOR_VAULT_REVIEW", ["TVC/value-bearing claim requires verified ownership before release"]

    if owner_claim.get("verified", False) is not True:
        reasons.append("owner claim is not verified; release limited to non-secret pointer receipt or hold")

    if pricing_basis.get("basis_type") == "not_priced_demo":
        reasons.append("demo pricing basis only; no real TVC issuance or settlement")

    release_policy = policy.get("release_policy", {})
    if not release_policy.get("allow_release_without_real_secret", False):
        return "HOLD_FOR_VAULT_REVIEW", ["policy does not allow pointer receipt release"]

    if reasons:
        return "HOLD_FOR_VAULT_REVIEW", reasons

    return "ALLOW_POINTER_RECEIPT", ["request satisfies current non-secret vaulted capability policy"]


def make_receipt(request: dict[str, Any], policy: dict[str, Any], verdict: str, reasons: list[str]) -> dict[str, Any]:
    receipt_type = {
        "ALLOW_POINTER_RECEIPT": "vaulted_capability_release_receipt",
        "DENY": "vaulted_capability_denial_receipt",
        "HOLD_FOR_VAULT_REVIEW": "vault_review_packet",
        "FAIL_CLOSED": "vaulted_capability_fail_closed_receipt",
    }.get(verdict, "vaulted_capability_receipt")

    public_request = dict(request)
    public_request.pop("secret_material", None)

    receipt = {
        "generated_at": utc_now(),
        "schema": "stegverse.vaulted_capability_receipt.v1",
        "formal_milestone": "MS-013 — Vaulted Capability Transition Layer",
        "receipt_type": receipt_type,
        "request_id": request.get("request_id"),
        "capability_type": request.get("capability_type"),
        "verdict": verdict,
        "reasons": reasons,
        "authority_basis": request.get("authority_basis"),
        "scope": request.get("scope"),
        "owner_claim": request.get("owner_claim"),
        "pricing_basis": request.get("pricing_basis"),
        "revocation_policy": request.get("revocation_policy"),
        "capability_pointer": None,
        "tvc_issued": False,
        "secret_material_exposed": False,
        "raw_secret_release": False,
        "policy_id": policy.get("policy_id"),
        "request_hash": stable_hash(public_request),
    }

    if verdict == "ALLOW_POINTER_RECEIPT":
        receipt["capability_pointer"] = {
            "pointer_id": "capability-pointer-" + stable_hash(public_request)[:16],
            "materialized_secret": False,
            "scope_bound": True,
            "revocable": True,
            "reuse_requires_revalidation": True
        }

    receipt["receipt_hash"] = stable_hash(receipt)
    return receipt


def write_markdown(path: Path, receipt: dict[str, Any]) -> None:
    lines = [
        "# Vaulted Capability Gate Report",
        "",
        f"Generated: `{receipt.get('generated_at')}`",
        f"Request: `{receipt.get('request_id')}`",
        f"Capability type: `{receipt.get('capability_type')}`",
        f"Verdict: `{receipt.get('verdict')}`",
        f"Receipt type: `{receipt.get('receipt_type')}`",
        f"Receipt hash: `{receipt.get('receipt_hash')}`",
        "",
        "## Reasons",
        "",
    ]
    for reason in receipt.get("reasons", []):
        lines.append(f"- {reason}")

    lines.extend([
        "",
        "## Safety",
        "",
        f"- TVC issued: `{receipt.get('tvc_issued')}`",
        f"- Secret material exposed: `{receipt.get('secret_material_exposed')}`",
        f"- Raw secret release: `{receipt.get('raw_secret_release')}`",
        "",
    ])

    pointer = receipt.get("capability_pointer")
    if pointer:
        lines.extend([
            "## Capability Pointer",
            "",
            "```json",
            json.dumps(pointer, indent=2),
            "```",
            "",
        ])

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--policy", default="data/vault/vaulted-capability-policy-v1.json")
    parser.add_argument("--request", default="")
    parser.add_argument("--out-dir", default="vault_reports")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    policy = load_json(root / args.policy, None)
    if not isinstance(policy, dict):
        raise SystemExit(f"Missing or invalid policy: {args.policy}")

    request_path = root / (args.request or policy.get("request_path", "data/vault/example-vaulted-capability-request-v1.json"))
    request = load_json(request_path, None)
    if not isinstance(request, dict):
        raise SystemExit(f"Missing or invalid request: {request_path}")

    verdict, reasons = evaluate(request, policy)
    receipt = make_receipt(request, policy, verdict, reasons)

    out = root / args.out_dir
    write_json(out / "vaulted-capability-gate-report.json", receipt)
    write_markdown(out / "vaulted-capability-gate-report.md", receipt)

    print(json.dumps({
        "request_id": receipt.get("request_id"),
        "verdict": verdict,
        "receipt_type": receipt.get("receipt_type"),
        "receipt_hash": receipt.get("receipt_hash")
    }, indent=2))

    return 0 if verdict in {"ALLOW_POINTER_RECEIPT", "HOLD_FOR_VAULT_REVIEW", "DENY"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
