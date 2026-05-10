#!/usr/bin/env python3
"""
Deterministic MS-012 transition replay checker.

This checker recomputes selected receipt-backed claims from public fixtures.
It intentionally uses only Python standard library.
"""

from __future__ import annotations

import argparse
import json
import hashlib
from pathlib import Path
from typing import Any


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def sha256_obj(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def verify_t13(fixture: dict[str, Any]) -> dict[str, Any]:
    pre_hash = sha256_obj(fixture["pre_state"])
    action_hash = sha256_obj(fixture["action"])
    post_hash = sha256_obj(fixture["post_state"])
    receipt_material = {
        "pre_state_hash": pre_hash,
        "action_hash": action_hash,
        "post_state_hash": post_hash,
    }
    receipt_hash = sha256_obj(receipt_material)

    expected = fixture["expected"]
    passed = (
        pre_hash == expected["pre_state_hash"]
        and action_hash == expected["action_hash"]
        and post_hash == expected["post_state_hash"]
        and receipt_hash == expected["receipt_material_hash"]
        and expected["verdict"] == "ALLOW"
    )

    return {
        "id": fixture["id"],
        "element": "T13",
        "check": "receipt_binding_replay",
        "passed": passed,
        "computed": {
            "pre_state_hash": pre_hash,
            "action_hash": action_hash,
            "post_state_hash": post_hash,
            "receipt_material_hash": receipt_hash,
        },
        "expected": expected,
        "verdict": "ALLOW" if passed else "DENY",
    }


def verify_t14(fixture: dict[str, Any]) -> dict[str, Any]:
    observed_hash = sha256_obj(fixture["observed_end_state"])
    reconstructed_hash = sha256_obj(fixture["reconstructed_end_state"])
    packet = {
        "pre_state_hash": sha256_obj(fixture["pre_state"]),
        "action_hash": sha256_obj(fixture["action"]),
        "observed_end_state_hash": observed_hash,
        "reconstructed_end_state_hash": reconstructed_hash,
    }
    packet_hash = sha256_obj(packet)

    expected = fixture["expected"]
    passed = (
        observed_hash == expected["observed_end_state_hash"]
        and reconstructed_hash == expected["reconstructed_end_state_hash"]
        and packet_hash == expected["reconstruction_packet_hash"]
        and observed_hash == reconstructed_hash
        and expected["verdict"] == "ALLOW"
    )

    return {
        "id": fixture["id"],
        "element": "T14",
        "check": "reconstruction_replay",
        "passed": passed,
        "computed": {
            "observed_end_state_hash": observed_hash,
            "reconstructed_end_state_hash": reconstructed_hash,
            "reconstruction_packet_hash": packet_hash,
        },
        "expected": expected,
        "verdict": "ALLOW" if passed else "DENY",
    }


def run_replay(fixtures_path: Path) -> dict[str, Any]:
    payload = json.loads(fixtures_path.read_text(encoding="utf-8"))
    results = []

    for fixture in payload.get("fixtures", []):
        element = fixture.get("element")
        if element == "T13":
            results.append(verify_t13(fixture))
        elif element == "T14":
            results.append(verify_t14(fixture))
        else:
            results.append({
                "id": fixture.get("id", "unknown"),
                "element": element,
                "check": "unsupported_fixture",
                "passed": False,
                "verdict": "DENY",
            })

    passed = all(row["passed"] for row in results)
    return {
        "schema": "stegverse.transition_replay_check_report.v1",
        "fixture_file": str(fixtures_path),
        "formal_milestone": payload.get("formal_milestone"),
        "selected_elements": payload.get("scope", {}).get("selected_elements", []),
        "verdict": "ALLOW" if passed else "DENY",
        "passed": passed,
        "results": results,
    }


def write_reports(report: dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "transition-replay-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "# Transition Replay Report",
        "",
        f"Result: **{'PASS' if report['passed'] else 'FAIL'}**",
        "",
        f"Verdict: `{report['verdict']}`",
        f"Formal milestone: `{report.get('formal_milestone')}`",
        f"Selected elements: `{', '.join(report.get('selected_elements', []))}`",
        "",
        "## Checks",
        "",
    ]

    for row in report["results"]:
        icon = "✅" if row["passed"] else "❌"
        lines.append(f"- {icon} `{row['element']}` `{row['id']}` `{row['check']}` → `{row['verdict']}`")

    (out_dir / "transition-replay-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay MS-012 selected receipt-backed transition fixtures.")
    parser.add_argument("--fixtures", default="data/transition-replay-fixtures-v1.json")
    parser.add_argument("--out-dir", default="transition_replay_reports")
    args = parser.parse_args()

    report = run_replay(Path(args.fixtures))
    write_reports(report, Path(args.out_dir))

    if not report["passed"]:
        print("FAIL: transition replay check returned DENY.")
        return 1

    print("PASS: transition replay check returned ALLOW.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
