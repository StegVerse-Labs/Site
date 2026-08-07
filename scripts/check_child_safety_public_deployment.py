#!/usr/bin/env python3
from __future__ import annotations
import json, os, ssl, sys, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "child-safety-public-deployment.report.json"
URL = os.environ.get("STEGVERSE_CHILD_SAFETY_PUBLIC_URL", "https://stegverse.org/child-safety-demo.html")
REQUIRED = (
    "Child Safety Governance — Live Public Demo",
    "StegVerse protective baseline",
    "REVIEW_REQUIRED",
    "retained_personal_data",
    "DEMO_BROWSER_ONLY",
)

def main() -> int:
    report = {
        "schema_version": "1.0.0",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "url": URL,
        "state": "BLOCKED",
        "http_status": None,
        "required_markers": list(REQUIRED),
        "missing_markers": [],
        "redirected_url": None,
        "tls_verified": False,
        "authority_effect": False,
        "activation_effect": False,
    }
    try:
        req = urllib.request.Request(URL, headers={"User-Agent":"StegVerse-Public-Deployment-Verifier/1.0"})
        with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as response:
            body = response.read(262144).decode("utf-8", errors="replace")
            report["http_status"] = response.status
            report["redirected_url"] = response.geturl()
            report["tls_verified"] = response.geturl().startswith("https://")
            report["missing_markers"] = [m for m in REQUIRED if m not in body]
            if response.status == 200 and report["tls_verified"] and not report["missing_markers"]:
                report["state"] = "VERIFIED_PUBLICLY_REACHABLE"
                report["activation_effect"] = "PUBLIC_INTERACTIVE_DEMO_ONLY"
    except Exception as exc:
        report["error"] = f"{type(exc).__name__}: {exc}"
    REPORT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if report["state"] == "VERIFIED_PUBLICLY_REACHABLE":
        print("CHILD_SAFETY_PUBLIC_DEPLOYMENT=PASS")
        print(f"PUBLIC_URL={report['redirected_url']}")
        print("AUTHORITY_GRANTED=false")
        print("ACTIVATION_EFFECT=PUBLIC_INTERACTIVE_DEMO_ONLY")
        return 0
    print("CHILD_SAFETY_PUBLIC_DEPLOYMENT=BLOCKED")
    print(json.dumps(report, sort_keys=True))
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
