#!/usr/bin/env python3
"""Validate Site third-party dependency inventory and provider-coupling coverage."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "data" / "third-party-dependency-inventory.json"

CLASSIFICATIONS = {
    "REQUIRED_CURRENTLY", "OPTIONAL_FALLBACK", "HISTORICAL_ONLY",
    "NEGATIVE_ASSERTION_ONLY", "REPLACEABLE_BUILD_INPUT",
    "UNAVOIDABLE_EXTERNAL_INTEROP", "UNKNOWN_PENDING_INVENTORY",
}
EVENTS = [
    "DISCOVERED", "CLASSIFIED", "REPLACEMENT_DESIGNED",
    "SOVEREIGN_COPY_OR_RUNTIME_READY", "DUAL_RUN_VERIFIED",
    "PROVIDER_FAILURE_PROVEN", "CUTOVER_COMPLETE", "CREDENTIALS_REVOKED",
    "ORPHAN_RESOURCE_RETIRED", "REGRESSION_GUARDED",
]
PATTERNS = {
    "vercel": [r"\bvercel\b", r"\.vercel\.app\b"],
    "render": [r"\brender\b", r"\.onrender\.com\b"],
    "cloudflare": [r"\bcloudflare\b", r"\.trycloudflare\.com\b"],
    "github": [r"\bgithub\b", r"\.github\.io\b", r"raw\.githubusercontent\.com"],
    "python-packages": [r"\bpip(?:3)?\s+install\b", r"pypi\.org"],
    "npm-packages": [r"\bnpm\s+(?:ci|install)\b", r"registry\.npmjs\.org"],
    "container-registry": [r"\bghcr\.io/", r"\bdocker\.io/", r"\bquay\.io/"],
}
SKIP = {".git", "node_modules", "__pycache__", ".venv", "venv"}
TEXT = {".md", ".txt", ".json", ".jsonl", ".yml", ".yaml", ".py", ".js", ".ts",
        ".tsx", ".html", ".css", ".sh", ".toml", ".ini", ".cfg", ".xml", ".tex"}
SELF = "scripts/check_third_party_dependency_invariant.py"


def read_inventory():
    return json.loads(INVENTORY.read_text(encoding="utf-8"))


def provider_key(node):
    joined = " ".join([
        str(node.get("id", "")), str(node.get("provider", "")),
        *[str(x) for x in node.get("classes", [])],
    ]).lower()
    for key, needles in {
        "vercel": ["vercel"], "render": ["render"], "cloudflare": ["cloudflare"],
        "github": ["github"], "python-packages": ["pypi", "python package"],
        "npm-packages": ["npm", "javascript package"],
        "container-registry": ["container registry", "base_image"],
    }.items():
        if any(n in joined for n in needles):
            return key
    return None


def allowed_paths(inv):
    result = {k: set() for k in PATTERNS}
    for node in inv.get("providers", []):
        key = provider_key(node)
        if key in result:
            for path in node.get("evidence_paths", []):
                result[key].add(str(path).replace("\\", "/").lstrip("./"))
    return result


def path_is_allowed(path, entries):
    if path == SELF:
        return True
    for entry in entries:
        if entry.endswith("/") and path.startswith(entry):
            return True
        if path == entry:
            return True
    return False


def validate(inv):
    errors = []
    if inv.get("schema") != "stegverse.site.third_party_dependency_inventory.v1":
        errors.append("unexpected inventory schema")
    if inv.get("goal_id") != "SITE-497-THIRD-PARTY-DEPENDENCY-ERADICATION":
        errors.append("inventory goal_id is not Site #497")
    if set(inv.get("allowed_classifications", [])) != CLASSIFICATIONS:
        errors.append("classification set differs from canonical policy")
    if inv.get("event_sequence") != EVENTS:
        errors.append("event sequence differs from canonical policy")

    seen = set()
    for i, node in enumerate(inv.get("providers", [])):
        p = f"providers[{i}]"
        ident = node.get("id")
        if not ident or ident in seen:
            errors.append(f"{p}: missing or duplicate id")
        seen.add(ident)
        cls = node.get("classification")
        if cls not in CLASSIFICATIONS:
            errors.append(f"{p}: invalid classification {cls}")
        if node.get("current_event") not in EVENTS or node.get("next_event") not in EVENTS:
            errors.append(f"{p}: invalid event state")
        if node.get("authority_effect") is True:
            errors.append(f"{p}: third-party authority_effect cannot be true")
        if cls == "HISTORICAL_ONLY" and node.get("current_required_use") is not False:
            errors.append(f"{p}: historical node must not be currently required")
        if cls == "REQUIRED_CURRENTLY":
            if node.get("current_required_use") is not True:
                errors.append(f"{p}: required node must set current_required_use=true")
            if not node.get("blockers"):
                errors.append(f"{p}: required node needs replacement blockers")
        if not node.get("evidence_paths"):
            errors.append(f"{p}: evidence_paths must not be empty")
    return errors


def scan(inv):
    allow = allowed_paths(inv)
    compiled = {k: [re.compile(x, re.I) for x in v] for k, v in PATTERNS.items()}
    findings = {k: [] for k in PATTERNS}
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(x in SKIP for x in path.relative_to(ROOT).parts):
            continue
        if path.suffix.lower() not in TEXT and path.name not in {
            "Dockerfile", "CNAME", "Procfile", "requirements.txt",
            "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
        }:
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        try:
            body = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for key, regexes in compiled.items():
            if path_is_allowed(rel, allow[key]):
                continue
            lines = [n for n, line in enumerate(body.splitlines(), 1)
                     if any(rx.search(line) for rx in regexes)]
            if lines:
                findings[key].append({"path": rel, "lines": lines[:10]})
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict-scan", action="store_true")
    ap.add_argument("--report", default="")
    args = ap.parse_args()

    inv = read_inventory()
    errors = validate(inv)
    findings = scan(inv)
    pending = sum(len(v) for v in findings.values())
    result = "FAIL" if errors or (args.strict_scan and pending) else (
        "PASS_WITH_INVENTORY_PENDING" if pending else "PASS"
    )
    report = {
        "schema": "stegverse.site.third_party_dependency_invariant_report.v1",
        "goal_id": inv.get("goal_id"),
        "structure_pass": not errors,
        "strict_scan_requested": args.strict_scan,
        "unclassified_reference_file_count": pending,
        "unclassified_references": findings,
        "errors": errors,
        "result": result,
    }
    if args.report:
        out = ROOT / args.report
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if result == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
