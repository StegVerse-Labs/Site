#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

TARGETS_PATH = Path("data/site-color-preserving-wiring-targets.json")
REPORT_PATH = Path("reports/site_color_preserving_bulk_wiring_report.json")
RECEIPTS_PATH = Path("receipts/site_color_preserving_bulk_wiring_receipts.jsonl")
CSS_LINE = '<link rel="stylesheet" href="assets/css/stegverse-color-preserving-wiring.css">'
JS_LINE = '<script src="assets/js/stegverse-color-preserving-wiring.js"></script>'
STATUS_MOUNT = '<div data-sv-status-mount></div>'

def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def digest(obj: dict) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def insert_before_head_close(html: str):
    if CSS_LINE in html:
        return html, False
    pattern = re.compile(r"</head\s*>", re.IGNORECASE)
    if pattern.search(html):
        return pattern.sub(CSS_LINE + "\n</head>", html, count=1), True
    return CSS_LINE + "\n" + html, True

def insert_before_body_close(html: str):
    if JS_LINE in html:
        return html, False
    pattern = re.compile(r"</body\s*>", re.IGNORECASE)
    if pattern.search(html):
        return pattern.sub(JS_LINE + "\n</body>", html, count=1), True
    return html + "\n" + JS_LINE + "\n", True

def insert_status_mount_after_body(html: str):
    if "data-sv-status-mount" in html:
        return html, False
    pattern = re.compile(r"(<body\b[^>]*>)", re.IGNORECASE)
    if pattern.search(html):
        return pattern.sub(r"\1\n" + STATUS_MOUNT, html, count=1), True
    return STATUS_MOUNT + "\n" + html, True

def wire_file(path: Path):
    original = path.read_text(encoding="utf-8")
    updated = original
    updated, css_added = insert_before_head_close(updated)
    updated, status_added = insert_status_mount_after_body(updated)
    updated, js_added = insert_before_body_close(updated)
    changed = updated != original
    if changed:
        path.write_text(updated, encoding="utf-8")
    return {
        "path": str(path),
        "exists": True,
        "changed": changed,
        "css_added": css_added,
        "status_mount_added": status_added,
        "script_added": js_added,
        "before_sha256": sha256_text(original),
        "after_sha256": sha256_text(updated)
    }

def main() -> int:
    payload = json.loads(TARGETS_PATH.read_text(encoding="utf-8"))
    results = []
    for target in payload.get("targets", []):
        path = Path(target)
        if not path.exists():
            results.append({"path": target, "exists": False, "changed": False, "reason": "target file missing"})
            continue
        results.append(wire_file(path))

    changed_count = sum(1 for item in results if item.get("changed"))
    missing_count = sum(1 for item in results if not item.get("exists"))
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RECEIPTS_PATH.parent.mkdir(parents=True, exist_ok=True)

    report = {
        "schema": "stegverse_site_color_preserving_bulk_wiring_report.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "success": True,
        "mode": "color_preserving_bulk_wiring",
        "target_count": len(results),
        "changed_count": changed_count,
        "missing_count": missing_count,
        "results": results,
        "visual_policy": {
            "sets_body_colors": False,
            "sets_body_background": False,
            "sets_font_family": False,
            "preserve_existing_site_color_scheme": True
        },
        "site_is_proof_authority": False
    }
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    receipt = {
        "schema": "stegverse_site_color_preserving_bulk_wiring_receipt.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "decision": "ALLOW_BULK_COLOR_PRESERVING_WIRING",
        "basis": "Inserted shared state/navigation wiring without setting page-level colors or theme.",
        "changed_count": changed_count,
        "missing_count": missing_count,
        "site_is_proof_authority": False
    }
    receipt["receipt_hash"] = digest(receipt)
    RECEIPTS_PATH.write_text(json.dumps(receipt, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
